# ResearchOS — Architectural Specification

ResearchOS is engineered with a modular, decoupled architecture adhering to clean separation of concerns and provider-agnostic extensibility.

---

## 1. High-Level System Layers

```
+-------------------------------------------------------------------------+
|                  Workstation Presentation Layer (React + Vite)          |
|  - Multi-pane Research Workspace      - Real-time Event Stream / SSE   |
|  - Interactive Research Plan Explorer - Traceable Evidence Ledger Visual|
+-------------------------------------------------------------------------+
                                    | REST / SSE
+-------------------------------------------------------------------------+
|                      API & Orchestration Layer (Flask)                  |
|  - Research Run Management           - Telemetry & Logging Middleware   |
|  - Rate Limiting & Validation        - Event Broadcasting Hub           |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
|                       Research Intelligence Subsystems                  |
|  - Intent Classifier                 - Research Planner & Decomposer    |
|  - Search Tool Aggregator            - Crawler & Document Processor     |
|  - Hybrid Retrieval (pgvector+BM25)  - Cross-Encoder Reranker           |
|  - Evidence Extraction & Ledger      - Contradiction Detector           |
|  - Coverage Evaluator & Stopping     - Gap Discovery & Novelty Analyzer |
|  - Report Generator & Citations      - User & Project Memory Subsystem  |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
|                 Provider Abstraction Layer (LLM & Tools)                |
|  - LLMInterface (Gemini, Groq, OpenRouter)                              |
|  - SearchAdapters (Academic, Web, Reddit, GitHub)                       |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
|                        Data & State Persistence Layer                   |
|  - PostgreSQL with pgvector (Structured metadata, Vector embeddings)    |
|  - Redis & Celery (Asynchronous task queue, Broker, Rate-limit cache)   |
+-------------------------------------------------------------------------+
```

---

## 2. Core Subsystems

### 2.1 Provider-Agnostic LLM Interface & Router
- **Standardized Base Interface**: Defines `generate()`, `generate_structured()`, `stream()`, and `embed()`.
- **Intelligent Routing**: Dynamic task-based model selection:
  - Fast models (e.g. Gemini Flash / Groq Llama) for query expansion and classification.
  - Reasoning models (e.g. Gemini Pro / Claude 3.5 Sonnet) for planning, contradiction analysis, and synthesis.
- **Resilience**: Exponential backoff retry, rate-limit quota tracking, and automatic provider fallback.

### 2.2 Pluggable Search Adapters
- Uniform output normalization across heterogeneous providers:
  - **AcademicSearch**: OpenAlex, Crossref, arXiv, Semantic Scholar, PubMed.
  - **WebSearch**: Serper, Tavily, SearXNG.
  - **CommunitySearch**: Reddit API.
  - **CodeSearch**: GitHub REST/GraphQL API.

### 2.3 Document Processing & Hybrid Retrieval
- **Structure-Aware Chunking**: Preserves section titles, page numbers, and semantic boundaries.
- **Dual Retrieval Pipeline**:
  - Dense vector similarity via `pgvector` (`text-embedding-004` / `bge-large-en`).
  - Sparse lexical matching via BM25 / PostgreSQL full-text search.
  - Cross-encoder reranking over top candidates.

### 2.4 Evidence Ledger & Citation Integrity
- Fine-grained traceability linking every claim in generated reports directly to an exact document chunk, page, section, confidence score, and corroborating sources.
- Guaranteed zero citation hallucination: all references must map to database source records verified during the research run.
