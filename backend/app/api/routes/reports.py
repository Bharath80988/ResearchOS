from flask import Blueprint, jsonify, Response
from ...database.base import SessionLocal
from ...database.models import ResearchRun, ResearchReport, Citation
from ...reports.exporters import ReportExporter
from ...utils import logger

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/research/<research_id>/export/markdown", methods=["GET"])
def export_markdown(research_id: str):
    """Exports full research publication as formatted Markdown."""
    db = SessionLocal()
    try:
        run = db.query(ResearchRun).filter(ResearchRun.id == research_id).first()
        if not run:
            return jsonify({"error": "Research run not found"}), 404

        report = db.query(ResearchReport).filter(ResearchReport.research_run_id == research_id).first()
        sec_json = report.sections_json if report else {}
        citations = sec_json.get("citations", [])
        chapters = sec_json.get("chapters", [])
        findings = sec_json.get("key_findings", [])
        gaps = sec_json.get("discovered_gaps", [])

        md_text = ReportExporter.to_markdown(
            question=run.question,
            summary=run.summary or "No summary available.",
            citations=citations,
            chapters=chapters,
            findings=findings,
            gaps=gaps
        )
        return Response(
            md_text,
            mimetype="text/markdown",
            headers={"Content-Disposition": f"attachment; filename=research_publication_{research_id[:8]}.md"}
        )
    finally:
        db.close()


@reports_bp.route("/research/<research_id>/export/csv", methods=["GET"])
def export_csv(research_id: str):
    """Exports structured evidence ledger as CSV (Excel compatible)."""
    db = SessionLocal()
    try:
        run = db.query(ResearchRun).filter(ResearchRun.id == research_id).first()
        if not run:
            return jsonify({"error": "Research run not found"}), 404

        report = db.query(ResearchReport).filter(ResearchReport.research_run_id == research_id).first()
        sec_json = report.sections_json if report else {}
        citations = sec_json.get("citations", [])

        csv_text = ReportExporter.to_csv_evidence_ledger(
            question=run.question,
            citations=citations
        )
        return Response(
            csv_text,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename=evidence_ledger_{research_id[:8]}.csv"}
        )
    finally:
        db.close()


@reports_bp.route("/research/<research_id>/export/presentation", methods=["GET"])
def export_presentation(research_id: str):
    """Exports standalone animated PPT HTML presentation player."""
    db = SessionLocal()
    try:
        run = db.query(ResearchRun).filter(ResearchRun.id == research_id).first()
        if not run:
            return jsonify({"error": "Research run not found"}), 404

        report = db.query(ResearchReport).filter(ResearchReport.research_run_id == research_id).first()
        sec_json = report.sections_json if report else {}
        chapters = sec_json.get("chapters", [])
        findings = sec_json.get("key_findings", [])
        gaps = sec_json.get("discovered_gaps", [])

        html_deck = ReportExporter.to_animated_presentation_html(
            question=run.question,
            summary=run.summary or "",
            chapters=chapters,
            findings=findings,
            gaps=gaps
        )
        return Response(html_deck, mimetype="text/html")
    finally:
        db.close()


@reports_bp.route("/research/<research_id>/export/pdf", methods=["GET"])
def export_pdf(research_id: str):
    """Exports publication-grade printable research paper / PDF."""
    db = SessionLocal()
    try:
        run = db.query(ResearchRun).filter(ResearchRun.id == research_id).first()
        if not run:
            return jsonify({"error": "Research run not found"}), 404

        report = db.query(ResearchReport).filter(ResearchReport.research_run_id == research_id).first()
        sec_json = report.sections_json if report else {}
        citations = sec_json.get("citations", [])
        chapters = sec_json.get("chapters", [])
        findings = sec_json.get("key_findings", [])

        html_text = ReportExporter.to_printable_html(
            question=run.question,
            summary=run.summary or "",
            citations=citations,
            chapters=chapters,
            findings=findings
        )
        return Response(html_text, mimetype="text/html")
    finally:
        db.close()
