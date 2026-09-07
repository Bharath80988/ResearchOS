import pytest
from app import create_app
from app.agents.worker_pool import ParallelWorkerPool
from app.agents.synthesizer import SynthesizerAgent
from app.tools.base import SearchResult


def test_worker_pool_sharding():
    pool = ParallelWorkerPool(batch_size=5, max_workers=3)
    
    # Generate 15 simulated sources
    test_sources = [
        SearchResult(
            title=f"Study {i}: Empirical Validation of RAG",
            url=f"https://openalex.org/W{i}",
            source_type="academic",
            domain="openalex.org",
            snippet=f"Methodology {i} shows high accuracy and factual alignment on benchmark datasets.",
            author=f"Author {i}",
            published_at="2025"
        )
        for i in range(15)
    ]

    events_captured = []
    def record_evt(msg, payload):
        events_captured.append((msg, payload))

    compressed = pool.shard_and_extract(
        sources=test_sources,
        research_topic="RAG architectures",
        on_worker_event=record_evt
    )

    assert len(compressed) == 15
    assert len(events_captured) >= 1  # Verify worker dispatch event emitted
    assert all(item.compressed_tokens_estimate > 0 for item in compressed)


def test_synthesizer_token_compression():
    synthesizer = SynthesizerAgent()
    pool = ParallelWorkerPool(batch_size=5)

    test_sources = [
        SearchResult(
            title="Multimodal RAG for Clinical Decision Support",
            url="https://arxiv.org/abs/2401.12345",
            source_type="academic",
            domain="arxiv.org",
            snippet="We observe 24.5% improvement in diagnostic retrieval across multimodal patient records.",
            author="Medical AI Lab",
            published_at="2025"
        )
    ]

    compressed = pool.shard_and_extract(test_sources, "Clinical RAG")
    result = synthesizer.synthesize("Clinical RAG", compressed)

    assert "summary" in result
    assert "citations" in result
    assert "savings_percentage" in result
    assert len(result["citations"]) == 1
