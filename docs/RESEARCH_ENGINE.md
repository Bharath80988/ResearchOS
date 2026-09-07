# ResearchOS — Deep Research Engine Specification

## 1. Multi-Stage Pipeline Lifecycle

The Research Engine operates as a goal-directed autonomous orchestrator executing the following lifecycle:

1. **Intent Classification**: Analyzes query nuances to determine domain, required sources (web, academic, code, community), required depth, and freshness constraints.
2. **Research Planning**: Decomposes high-level questions into prioritized subtasks with clear acceptance criteria.
3. **Query Expansion & Search**: Issues targeted, varied search strategies (broad, precise, limitation, contradictory, benchmark, implementation).
4. **Content Extraction & Document Processing**: Crawls URLs and parses PDFs, preserving section hierarchy, page numbers, and publication metadata.
5. **Hybrid Retrieval**: Combines pgvector semantic similarity with BM25 lexical keyword matching, reranked by cross-encoders.
6. **Evidence Extraction & Verification**: Maps granular claims to exact supporting passages with confidence scores.
7. **Contradiction Discovery**: Actively looks for conflicting claims and documents methodological differences (e.g. dataset variances, evaluation metrics).
8. **Coverage & Stopping Evaluation**: Iteratively checks if all subtasks possess sufficient evidence and source diversity before stopping.
9. **Research Gap & Novelty Analysis**: Clusters limitations and unaddressed problem formulations.
10. **Report Synthesis & Citation Validation**: Produces structured markdown reports with verified traceable references.
