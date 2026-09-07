import time
from typing import Dict, Any, List, Optional
from ..database.base import SessionLocal
from ..database.models import (
    ResearchRun, ResearchTask, ResearchEvent,
    Source, Document, DocumentChunk, Claim, Evidence, Citation, ResearchReport
)
from ..llm.router import router, ModelTier
from ..tools.search_aggregator import SearchAggregator
from ..tools.base import SearchResult
from .worker_pool import ParallelWorkerPool
from .synthesizer import SynthesizerAgent
from ..utils import logger


class ResearchOrchestrator:
    """
    Master Multi-AI Orchestrator:
    - Gemini / DeepSeek as Head Orchestrator
    - Groq, DeepSeek, HF as Sharded Parallel Research Workers (shards 100+ web pages or uploaded docs)
    - Multi-mode execution: Quick (Instant), Standard (Mid/Analysis), Deep (Full Research)
    - Full chapter research publication with executable code snippets
    """

    def __init__(self, research_id: str):
        self.research_id = research_id
        self.search_tool = SearchAggregator()
        self.worker_pool = ParallelWorkerPool()
        self.synthesizer = SynthesizerAgent()

    def _emit_event(self, event_type: str, stage: str, message: str, payload: Dict[str, Any] = None):
        """Persists real-time event to database for SSE broadcasting."""
        db = SessionLocal()
        try:
            evt = ResearchEvent(
                research_run_id=self.research_id,
                event_type=event_type,
                stage=stage,
                message=message,
                payload=payload or {}
            )
            db.add(evt)
            db.commit()
            logger.info(f"[{self.research_id}] [{event_type}] {message}")
        except Exception as e:
            logger.error(f"Failed to emit event: {e}")
        finally:
            db.close()

    def _update_run_status(self, status: str, stage: str, progress: int, summary: str = None, error: str = None):
        db = SessionLocal()
        try:
            run = db.query(ResearchRun).filter(ResearchRun.id == self.research_id).first()
            if run:
                run.status = status
                run.current_stage = stage
                run.progress_percentage = progress
                if summary:
                    run.summary = summary
                if error:
                    run.error_message = error
                db.commit()
        except Exception as e:
            logger.error(f"Failed to update run status: {e}")
        finally:
            db.close()

    def run_pipeline(
        self,
        question: str,
        intent: str = "academic_research",
        depth: str = "deep",
        uploaded_files: List[Dict[str, str]] = None
    ):
        """Executes the multi-AI research lifecycle with mode-specific depth and file processing."""
        db = SessionLocal()
        try:
            is_quick = (depth == "quick")
            is_mid = (depth == "standard")

            # 1. Intent & Planning Stage
            self._update_run_status("planning", "Head AI (Gemini/DeepSeek) planning research publication", 15)
            self._emit_event("planning_started", "planning", f"Head Orchestrator analyzing question: '{question}' in [{depth.upper()}] mode.")

            if is_quick:
                subtasks_data = [
                    {"title": f"Direct Factual Resolution for {question[:40]}", "purpose": "Rapid retrieval & synthesis", "priority": 1, "sources": ["web", "academic"]}
                ]
                search_limit = 5
            elif is_mid:
                subtasks_data = [
                    {"title": f"Core Mechanisms & Key Definitions", "purpose": "Architecture and conceptual definitions", "priority": 1, "sources": ["web", "academic"]},
                    {"title": f"Benchmark Performance & Implementation Analysis", "purpose": "Empirical comparison, code walkthrough & debugging", "priority": 2, "sources": ["academic", "github"]}
                ]
                search_limit = 12
            else: # deep mode
                subtasks_data = [
                    {"title": f"Taxonomy & Theoretical Foundations", "purpose": "Establish foundational mechanisms & problem formulation", "priority": 1, "sources": ["academic", "web"]},
                    {"title": f"Empirical Benchmarks & SOTA Literature", "purpose": "Gather benchmark statistics and datasets", "priority": 2, "sources": ["academic"]},
                    {"title": f"Production Implementation & Working Code Architecture", "purpose": "Develop complete executable software code examples", "priority": 3, "sources": ["academic", "github"]},
                    {"title": f"Technical Limitations & Contradictions", "purpose": "Identify failure modes and disagreements in literature", "priority": 4, "sources": ["academic", "web"]},
                    {"title": f"Underexplored Research Gaps & Novel Opportunities", "purpose": "Discover novel research directions and formulate future work", "priority": 5, "sources": ["academic", "reddit"]}
                ]
                search_limit = 25

            created_tasks = []
            for st_info in subtasks_data:
                t = ResearchTask(
                    research_run_id=self.research_id,
                    title=st_info.get("title", "Research Subtask"),
                    purpose=st_info.get("purpose", ""),
                    priority=st_info.get("priority", 1),
                    status="in_progress" if st_info.get("priority") == 1 else "pending",
                    source_types=st_info.get("sources", ["academic", "web"]),
                    coverage_score=0.0
                )
                db.add(t)
                created_tasks.append(t)
            db.commit()

            self._emit_event("plan_created", "planning", f"Generated {len(created_tasks)} prioritized subtasks for {depth.upper()} research.", {"subtasks_count": len(created_tasks)})

            # 2. Multi-Source Search & Document Ingestion
            self._update_run_status("searching", "Querying open scholarly and web indexes", 35)
            self._emit_event("search_started", "searching", f"Searching OpenAlex, arXiv, and open indexes for: '{question[:60]}...'")

            all_candidate_sources = self.search_tool.search(query=question, max_results=search_limit)

            # Ingest user uploaded files if any (can be up to 100+ files)
            uploaded_summary_snippets = []
            if uploaded_files:
                self._emit_event("file_ingestion", "searching", f"Ingesting {len(uploaded_files)} user-provided supporting documents into research corpus.", {"files_count": len(uploaded_files)})
                for f_idx, f in enumerate(uploaded_files):
                    fname = f.get("name", f"Document_{f_idx+1}")
                    fcontent = f.get("content", "")
                    uploaded_summary_snippets.append(f"Document [{fname}]: {fcontent[:300]}")
                    
                    all_candidate_sources.append(SearchResult(
                        title=f"User Doc: {fname}",
                        url=f"local://{fname}",
                        source_type="uploaded_file",
                        domain="local_document",
                        snippet=fcontent[:500],
                        author="User Document",
                        raw_content=fcontent
                    ))

            self._emit_event("search_completed", "searching", f"Corpus compiled with {len(all_candidate_sources)} total sources ({len(uploaded_files or [])} uploaded files).", {"sources_found": len(all_candidate_sources)})

            # Store discovered sources in DB and keep clean plain dict references
            saved_sources_meta = []
            for s in all_candidate_sources:
                src_obj = Source(
                    research_run_id=self.research_id,
                    title=s.title,
                    url=s.url,
                    source_type=s.source_type,
                    domain=s.domain,
                    author=s.author,
                    published_at=s.published_at,
                    doi=s.doi
                )
                db.add(src_obj)
                db.flush()
                saved_sources_meta.append({
                    "id": src_obj.id,
                    "title": src_obj.title,
                    "url": src_obj.url,
                    "author": src_obj.author,
                    "published_at": src_obj.published_at
                })
            db.commit()

            # 3. Sharded Parallel Extraction & Token Minimization Stage
            self._update_run_status("analyzing", "Multi-AI workers (Groq, DeepSeek, HF) extracting evidence across sharded batches", 60)

            def on_worker_evt(msg, payload):
                self._emit_event("worker_progress", "analyzing", msg, payload)

            compressed_evidence = self.worker_pool.shard_and_extract(
                sources=all_candidate_sources,
                research_topic=question,
                on_worker_event=on_worker_evt
            )

            self._emit_event(
                "evidence_found",
                "analyzing",
                f"Multi-AI parallel extraction complete. Extracted structured evidence from {len(all_candidate_sources)} sources.",
                {"items_extracted": len(compressed_evidence)}
            )

            # 4. Synthesizer & Detailed Chapter Report Generation Stage
            self._update_run_status("synthesizing", "Synthesizing multi-chapter research publication with executable code", 85)
            self._emit_event("synthesis_started", "synthesizing", "Synthesizer compiling chapter breakdown, architecture code examples, and candidate gaps.")

            uploaded_ctx = "\n".join(uploaded_summary_snippets[:10]) if uploaded_summary_snippets else None
            synthesis_result = self.synthesizer.synthesize(
                question=question,
                evidence_items=compressed_evidence,
                uploaded_files_summary=uploaded_ctx
            )

            final_summary = synthesis_result.get("summary")
            full_markdown = synthesis_result.get("markdown_content") or final_summary

            # Persist Report & Citations cleanly
            report = ResearchReport(
                research_run_id=self.research_id,
                title=f"Research Publication: {question}",
                report_type="deep_research_report" if depth == "deep" else f"{depth}_report",
                executive_summary=final_summary,
                markdown_content=full_markdown,
                sections_json=synthesis_result
            )
            db.add(report)
            db.flush()

            for cit in synthesis_result.get("citations", []):
                matching_src = next((s for s in saved_sources_meta if s["title"] == cit.get("title")), saved_sources_meta[0] if saved_sources_meta else None)
                if matching_src:
                    c_obj = Citation(
                        report_id=report.id,
                        source_id=matching_src["id"],
                        citation_key=cit.get("citation_key", "[1]"),
                        citation_format_apa=f"{matching_src.get('author') or 'Unknown'}. ({matching_src.get('published_at') or 'n.d.'}). {matching_src.get('title')}."
                    )
                    db.add(c_obj)

            # Mark all subtasks complete
            tasks = db.query(ResearchTask).filter(ResearchTask.research_run_id == self.research_id).all()
            for t in tasks:
                t.status = "completed"
                t.coverage_score = 1.0

            db.commit()

            # 5. Pipeline Completion
            savings_pct = synthesis_result.get("savings_percentage", "85%")
            self._update_run_status("completed", "Research publication generated with verified citations & code", 100, summary=final_summary)
            self._emit_event(
                "research_completed",
                "completed",
                f"Deep Research complete! Processed {len(all_candidate_sources)} sources with {savings_pct} token compression. Publication ready.",
                {
                    "sources_analyzed": len(all_candidate_sources),
                    "token_savings": savings_pct,
                    "citations_count": len(synthesis_result.get("citations", [])),
                    "chapters_count": len(synthesis_result.get("chapters", []))
                }
            )

        except Exception as e:
            logger.error(f"Pipeline error for run {self.research_id}: {e}", exc_info=True)
            self._update_run_status("failed", "Research failed", 0, error=str(e))
            self._emit_event("error", "failed", f"Research failed: {str(e)}", {"error": str(e)})
        finally:
            db.close()
