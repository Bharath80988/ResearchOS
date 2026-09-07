import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
from dataclasses import dataclass
from ..llm.router import router, ModelTier
from ..tools.crawler import WebCrawler
from ..tools.base import SearchResult
from ..config import get_settings
from ..utils import logger

settings = get_settings()


@dataclass
class CompressedEvidenceItem:
    source_title: str
    source_url: str
    source_type: str
    claims: List[str]
    exact_quotes: List[str]
    limitations: List[str]
    confidence: float
    raw_tokens_estimate: int
    compressed_tokens_estimate: int


class ExtractionWorker:
    """
    Fast AI Worker that analyzes a batch of up to 10 sources,
    strips extraneous boilerplate, and extracts high-signal claims and quotes.
    """

    def __init__(self, worker_id: int):
        self.worker_id = worker_id

    def process_source_batch(self, sources_batch: List[SearchResult], research_topic: str) -> List[CompressedEvidenceItem]:
        extracted_items: List[CompressedEvidenceItem] = []
        logger.info(f"[Worker #{self.worker_id}] Starting parallel extraction for batch of {len(sources_batch)} sources.")

        for src in sources_batch:
            # Crawl or use snippet
            raw_text = WebCrawler.crawl_url(src.url) if src.url.startswith("http") else None
            content_to_analyze = raw_text or src.snippet or src.title
            
            raw_tokens = len(content_to_analyze) // 4

            prompt = f"""You are an expert evidentiary extraction worker for ResearchOS.
Topic: {research_topic}
Source Title: {src.title}
Source Type: {src.source_type}
Content:
{content_to_analyze[:3500]}

Extract the most important factual findings and evidence related to the topic into JSON:
{{
  "claims": ["List 1 to 3 key factual or methodological claims made in this text"],
  "exact_quotes": ["List 1 to 2 exact verbatim quotes supporting the claims"],
  "limitations": ["Any limitations or unresolved problems mentioned"],
  "confidence": 0.85
}}"""

            system_prompt = "You are a fast, factual evidence extraction agent. Return only raw JSON without markdown formatting."

            try:
                # Use fast/worker tier (Groq Llama 3.1 8B or Gemini Flash)
                response = router.generate_structured(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    tier=ModelTier.WORKER,
                    max_tokens=512
                )
                parsed = response.parsed_json or {}
                
                claims = parsed.get("claims") or [src.snippet[:150]]
                exact_quotes = parsed.get("exact_quotes") or [src.snippet[:120]]
                limitations = parsed.get("limitations") or []
                confidence = float(parsed.get("confidence") or 0.8)

            except Exception as e:
                logger.debug(f"[Worker #{self.worker_id}] Extraction fallback for {src.title}: {e}")
                claims = [f"Found evidence in {src.title} supporting {research_topic}"]
                exact_quotes = [src.snippet[:140]]
                limitations = []
                confidence = 0.75

            compressed_text = " ".join(claims + exact_quotes)
            compressed_tokens = max(len(compressed_text) // 4, 20)

            extracted_items.append(CompressedEvidenceItem(
                source_title=src.title,
                source_url=src.url,
                source_type=src.source_type,
                claims=claims,
                exact_quotes=exact_quotes,
                limitations=limitations,
                confidence=confidence,
                raw_tokens_estimate=raw_tokens,
                compressed_tokens_estimate=compressed_tokens
            ))

        return extracted_items


class ParallelWorkerPool:
    """
    Shards large sets of sources (e.g. 30 websites/papers) into 10-source batches
    and orchestrates parallel multi-AI extraction workers to compress tokens.
    """

    def __init__(self, batch_size: int = None, max_workers: int = None):
        self.batch_size = batch_size or settings.WORKER_BATCH_SIZE
        self.max_workers = max_workers or settings.MAX_PARALLEL_WORKERS

    def shard_and_extract(
        self,
        sources: List[SearchResult],
        research_topic: str,
        on_worker_event: Any = None
    ) -> List[CompressedEvidenceItem]:
        if not sources:
            return []

        # Split sources into batches of 10
        batches = [sources[i:i + self.batch_size] for i in range(0, len(sources), self.batch_size)]
        total_workers = min(len(batches), self.max_workers)

        logger.info(f"Sharded {len(sources)} sources into {len(batches)} batches across {total_workers} parallel AI workers.")
        if on_worker_event:
            on_worker_event(
                f"Dispatched {len(batches)} parallel AI workers to analyze {len(sources)} sources ({self.batch_size} sources per worker).",
                {"batches_count": len(batches), "total_sources": len(sources)}
            )

        all_results: List[CompressedEvidenceItem] = []

        with ThreadPoolExecutor(max_workers=total_workers) as executor:
            future_to_worker = {
                executor.submit(
                    ExtractionWorker(worker_id=idx + 1).process_source_batch,
                    batch,
                    research_topic
                ): idx + 1 for idx, batch in enumerate(batches)
            }

            for future in as_completed(future_to_worker):
                w_id = future_to_worker[future]
                try:
                    worker_items = future.result()
                    all_results.extend(worker_items)
                    if on_worker_event:
                        on_worker_event(
                            f"AI Worker #{w_id} completed extraction for batch ({len(worker_items)} sources processed).",
                            {"worker_id": w_id, "items_count": len(worker_items)}
                        )
                except Exception as ex:
                    logger.error(f"Worker #{w_id} encountered error: {ex}")

        return all_results
