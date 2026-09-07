import json
import time
import threading
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, Response
from pydantic import ValidationError

from ...database.base import SessionLocal
from ...database.models import ResearchRun, ResearchTask, ResearchEvent
from ...api.schemas.research import ResearchCreateRequest, ResearchRunResponse, ResearchEventSchema
from ...utils import logger

research_bp = Blueprint("research", __name__)


def _simulate_phase1_research_progress(research_id: str, question: str, depth: str):
    """
    Phase 1 asynchronous research stage simulator.
    In Phase 1, initializes tasks and steps through the pipeline stages with realistic research events,
    ensuring real-time visual progress on both REST and SSE stream endpoints.
    Subsequent phases integrate live LLM planners and search tools.
    """
    db = SessionLocal()
    try:
        run = db.query(ResearchRun).filter(ResearchRun.id == research_id).first()
        if not run:
            return

        # Stage 1: Intent Classification & Planning
        time.sleep(0.6)
        run.status = "planning"
        run.current_stage = "Classifying intent & decomposing subtasks"
        run.progress_percentage = 15
        
        # Subtasks generation based on depth & prompt
        tasks_data = [
            {"title": "Clarify definitions & core taxonomy", "purpose": "Establish foundational concepts", "priority": 1, "sources": ["web", "academic"]},
            {"title": "Survey empirical benchmarks & state-of-the-art", "purpose": "Gather performance metrics", "priority": 2, "sources": ["academic"]},
            {"title": "Identify technical limitations & trade-offs", "purpose": "Evaluate failure modes and bottlenecks", "priority": 3, "sources": ["web", "academic", "github"]},
            {"title": "Map candidate research gaps & underexplored directions", "purpose": "Synthesize future directions", "priority": 4, "sources": ["academic", "reddit"]},
        ]
        
        created_tasks = []
        for t_info in tasks_data:
            task = ResearchTask(
                research_run_id=research_id,
                title=t_info["title"],
                purpose=t_info["purpose"],
                priority=t_info["priority"],
                status="in_progress" if t_info["priority"] == 1 else "pending",
                source_types=t_info["sources"],
                coverage_score=0.0
            )
            db.add(task)
            created_tasks.append(task)
            
        evt1 = ResearchEvent(
            research_run_id=research_id,
            event_type="plan_created",
            stage="planning",
            message="Generated research plan with 4 prioritized subtasks and source constraints.",
            payload={"subtasks_count": 4, "depth": depth}
        )
        db.add(evt1)
        db.commit()

        # Stage 2: Searching Sources
        time.sleep(0.8)
        run.status = "searching"
        run.current_stage = "Parallel querying academic, web, and technical indexes"
        run.progress_percentage = 35
        evt2 = ResearchEvent(
            research_run_id=research_id,
            event_type="search_started",
            stage="searching",
            message=f"Dispatched search queries across OpenAlex, arXiv, and web adapters for: '{question[:60]}...'",
            payload={"sources_targeted": ["academic", "web", "github"]}
        )
        db.add(evt2)
        db.commit()

        # Stage 3: Ingestion & Hybrid Retrieval
        time.sleep(1.0)
        run.status = "analyzing"
        run.current_stage = "Extracting evidence passages & building evidence ledger"
        run.progress_percentage = 65
        evt3 = ResearchEvent(
            research_run_id=research_id,
            event_type="evidence_found",
            stage="analyzing",
            message="Extracted high-confidence evidence passages across candidate documents.",
            payload={"extracted_claims": 8, "evidence_passages": 14}
        )
        db.add(evt3)
        db.commit()

        # Stage 4: Synthesis & Completion
        time.sleep(0.8)
        run.status = "completed"
        run.current_stage = "Research completed"
        run.progress_percentage = 100
        run.summary = f"Comprehensive research completed for '{question}'. Found multiple supporting sources with traceable evidence."
        
        # Mark tasks completed
        for t in created_tasks:
            t.status = "completed"
            t.coverage_score = 0.95

        evt4 = ResearchEvent(
            research_run_id=research_id,
            event_type="research_completed",
            stage="completed",
            message="Deep research completed successfully. Findings compiled into evidence ledger.",
            payload={"status": "success", "duration_sec": 3.2}
        )
        db.add(evt4)
        db.commit()

    except Exception as e:
        logger.error(f"Error executing research run {research_id}: {e}", exc_info=True)
        if run:
            run.status = "failed"
            run.error_message = str(e)
            db.commit()
    finally:
        db.close()


@research_bp.route("/research", methods=["POST"])
def create_research_run():
    """Initiates a new research run."""
    raw_data = request.get_json() or {}
    try:
        validated = ResearchCreateRequest(**raw_data)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.errors()}), 422

    db = SessionLocal()
    try:
        run = ResearchRun(
            question=validated.question,
            intent=validated.intent,
            depth=validated.depth,
            project_id=validated.project_id,
            user_id=validated.user_id,
            options=validated.options or {},
            status="queued",
            current_stage="Research initiated",
            progress_percentage=0,
            stats={"sources_count": 0, "claims_count": 0, "tokens": 0}
        )
        db.add(run)
        db.flush()

        # Emit initial event
        init_event = ResearchEvent(
            research_run_id=run.id,
            event_type="research_started",
            stage="queued",
            message=f"Research queued: '{validated.question}'",
            payload={"depth": validated.depth, "intent": validated.intent}
        )
        db.add(init_event)
        db.commit()

        research_id = run.id
        created_at = run.created_at

        # Launch asynchronous research workflow
        threading.Thread(
            target=_simulate_phase1_research_progress,
            args=(research_id, validated.question, validated.depth),
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
    """Retrieves full details and subtasks for a specific research run."""
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
            "created_at": run.created_at.isoformat() if run.created_at else None,
            "updated_at": run.updated_at.isoformat() if run.updated_at else None,
            "tasks": tasks_list
        }), 200
    finally:
        db.close()


@research_bp.route("/research/<research_id>/events", methods=["GET"])
def get_research_events(research_id: str):
    """Retrieves all chronological events for a research run."""
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
                    # Fetch events created after the last one seen
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

            time.sleep(0.5)

    return Response(
        event_generator(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive"
        }
    )
