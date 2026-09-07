import json
import time
import threading
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, Response
from pydantic import ValidationError

from ...database.base import SessionLocal
from ...database.models import ResearchRun, ResearchTask, ResearchEvent
from ...api.schemas.research import ResearchCreateRequest, ResearchRunResponse, ResearchEventSchema
from ...agents.orchestrator import ResearchOrchestrator
from ...utils import logger

research_bp = Blueprint("research", __name__)


def _execute_orchestrated_research(research_id: str, question: str, intent: str, depth: str, uploaded_files: list = None):
    """Executes the autonomous ResearchOS multi-AI orchestrator pipeline in background."""
    orchestrator = ResearchOrchestrator(research_id=research_id)
    orchestrator.run_pipeline(
        question=question,
        intent=intent,
        depth=depth,
        uploaded_files=uploaded_files
    )


@research_bp.route("/research", methods=["POST"])
def create_research_run():
    """Initiates a new research run with autonomous multi-AI orchestration & file support."""
    raw_data = request.get_json() or {}
    try:
        validated = ResearchCreateRequest(**raw_data)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.errors()}), 422

    db = SessionLocal()
    try:
        files_data = [f.model_dump() for f in validated.files] if validated.files else []
        options = validated.options or {}
        if files_data:
            options["uploaded_files_count"] = len(files_data)

        run = ResearchRun(
            question=validated.question,
            intent=validated.intent or "academic_research",
            depth=validated.depth or "deep",
            project_id=validated.project_id,
            user_id=validated.user_id,
            options=options,
            status="queued",
            current_stage=f"Research initialized ({len(files_data)} documents attached)" if files_data else "Research initialized in worker queue",
            progress_percentage=0,
            stats={"sources_count": len(files_data), "claims_count": 0, "tokens": 0}
        )
        db.add(run)
        db.flush()

        init_event = ResearchEvent(
            research_run_id=run.id,
            event_type="research_started",
            stage="queued",
            message=f"Research inquiry queued: '{validated.question}' ({len(files_data)} attached docs)",
            payload={"depth": validated.depth, "intent": validated.intent, "files_count": len(files_data)}
        )
        db.add(init_event)
        db.commit()

        research_id = run.id
        created_at = run.created_at

        # Launch multi-AI orchestrator pipeline in background thread
        threading.Thread(
            target=_execute_orchestrated_research,
            args=(research_id, validated.question, validated.intent, validated.depth, files_data),
            daemon=True
        ).start()

        return jsonify({
            "research_id": research_id,
            "question": validated.question,
            "status": "queued",
            "created_at": created_at.isoformat(),
            "stream_url": f"/api/research/{research_id}/stream"
        }), 202

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create research run: {e}")
        return jsonify({"error": "Failed to create research run", "message": str(e)}), 500
    finally:
        db.close()


@research_bp.route("/research", methods=["GET"])
def list_research_runs():
    """Lists research runs with pagination."""
    limit = min(int(request.args.get("limit", 20)), 100)
    offset = max(int(request.args.get("offset", 0)), 0)

    db = SessionLocal()
    try:
        runs = (
            db.query(ResearchRun)
            .order_by(ResearchRun.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        results = []
        for r in runs:
            results.append({
                "id": r.id,
                "question": r.question,
                "intent": r.intent,
                "depth": r.depth,
                "status": r.status,
                "progress_percentage": r.progress_percentage,
                "current_stage": r.current_stage,
                "summary": r.summary,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            })
        return jsonify({"items": results, "count": len(results)}), 200
    finally:
        db.close()


@research_bp.route("/research/<research_id>", methods=["GET"])
def get_research_run(research_id: str):
    """Retrieves full details, subtasks, and findings for a research run."""
    db = SessionLocal()
    try:
        run = db.query(ResearchRun).filter(ResearchRun.id == research_id).first()
        if not run:
            return jsonify({"error": "Research run not found"}), 404

        tasks_list = []
        for t in run.tasks:
            tasks_list.append({
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "purpose": t.purpose,
                "priority": t.priority,
                "status": t.status,
                "source_types": t.source_types,
                "coverage_score": t.coverage_score
            })

        # Fetch report details if present
        report_data = {}
        if run.reports and len(run.reports) > 0:
            rep = run.reports[0]
            report_data = {
                "id": rep.id,
                "title": rep.title,
                "markdown_content": rep.markdown_content,
                "sections": rep.sections_json or {}
            }

        return jsonify({
            "id": run.id,
            "question": run.question,
            "intent": run.intent,
            "depth": run.depth,
            "status": run.status,
            "progress_percentage": run.progress_percentage,
            "current_stage": run.current_stage,
            "summary": run.summary,
            "error_message": run.error_message,
            "plan": run.plan,
            "stats": run.stats,
            "options": run.options,
            "report": report_data,
            "created_at": run.created_at.isoformat() if run.created_at else None,
            "updated_at": run.updated_at.isoformat() if run.updated_at else None,
            "tasks": tasks_list
        }), 200
    finally:
        db.close()


@research_bp.route("/research/<research_id>", methods=["DELETE"])
def delete_research_run(research_id: str):
    """Deletes a past research run."""
    db = SessionLocal()
    try:
        run = db.query(ResearchRun).filter(ResearchRun.id == research_id).first()
        if not run:
            return jsonify({"error": "Research run not found"}), 404
        db.delete(run)
        db.commit()
        return jsonify({"message": "Research run deleted successfully", "id": research_id}), 200
    finally:
        db.close()


@research_bp.route("/research/<research_id>/events", methods=["GET"])
def get_research_events(research_id: str):
    """Retrieves chronological events for a research run."""
    db = SessionLocal()
    try:
        events = (
            db.query(ResearchEvent)
            .filter(ResearchEvent.research_run_id == research_id)
            .order_by(ResearchEvent.created_at.asc())
            .all()
        )
        
        output = []
        for e in events:
            output.append({
                "id": e.id,
                "research_run_id": e.research_run_id,
                "event_type": e.event_type,
                "stage": e.stage,
                "message": e.message,
                "payload": e.payload,
                "created_at": e.created_at.isoformat() if e.created_at else None
            })
        return jsonify({"events": output, "count": len(output)}), 200
    finally:
        db.close()


@research_bp.route("/research/<research_id>/stream", methods=["GET"])
def stream_research_events(research_id: str):
    """Server-Sent Events (SSE) streaming endpoint."""
    def event_generator():
        last_seen_event_id = None
        consecutive_completed_checks = 0

        while True:
            db = SessionLocal()
            try:
                run = db.query(ResearchRun).filter(ResearchRun.id == research_id).first()
                if not run:
                    yield f"event: error\ndata: {json.dumps({'error': 'Research run not found'})}\n\n"
                    break

                query = db.query(ResearchEvent).filter(ResearchEvent.research_run_id == research_id)
                if last_seen_event_id:
                    last_event = db.query(ResearchEvent).filter(ResearchEvent.id == last_seen_event_id).first()
                    if last_event:
                        query = query.filter(ResearchEvent.created_at > last_event.created_at)

                events = query.order_by(ResearchEvent.created_at.asc()).all()
                for e in events:
                    last_seen_event_id = e.id
                    event_data = {
                        "id": e.id,
                        "research_run_id": e.research_run_id,
                        "event_type": e.event_type,
                        "stage": e.stage,
                        "message": e.message,
                        "payload": e.payload,
                        "status": run.status,
                        "progress_percentage": run.progress_percentage,
                        "current_stage": run.current_stage,
                        "created_at": e.created_at.isoformat() if e.created_at else None
                    }
                    yield f"event: {e.event_type}\ndata: {json.dumps(event_data)}\n\n"

                if run.status in ["completed", "failed"]:
                    consecutive_completed_checks += 1
                    if consecutive_completed_checks >= 2:
                        final_msg = {
                            "status": run.status,
                            "progress_percentage": run.progress_percentage,
                            "summary": run.summary,
                            "error_message": run.error_message
                        }
                        yield f"event: done\ndata: {json.dumps(final_msg)}\n\n"
                        break
            except Exception as ex:
                logger.error(f"Error in SSE stream for {research_id}: {ex}")
                yield f"event: error\ndata: {json.dumps({'error': str(ex)})}\n\n"
                break
            finally:
                db.close()

            time.sleep(0.4)

    return Response(
        event_generator(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive"
        }
    )
