# ResearchOS — Architectural Specification (v2.0)

ResearchOS is engineered with a modular, decoupled multi-agent architecture supporting 100% free models and sharded parallel worker extraction.

---

## 1. Multi-AI Orchestrator & Sharded Worker Pipeline

```
+-------------------------------------------------------------------------+
|                  Workstation Presentation Layer (React + Vite)          |
|  - Model Provider Selectors (DeepSeek R1, Groq, HuggingFace, Gemini)    |
|  - Real-time Event Stream / SSE Terminal & Multi-Agent Telemetry        |
+-------------------------------------------------------------------------+
                                    | REST / SSE
+-------------------------------------------------------------------------+
|                      API & Orchestration Layer (Flask)                  |
|  - Master ResearchOrchestrator        - Telemetry & Logging Middleware  |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
|                    Free LLM Router Layer (100% Free Tiers)              |
|  - OpenRouter (deepseek-r1:free, deepseek-chat:free, llama-3.3-70b:free)|
|  - Groq (llama-3.1-8b-instant @ 300+ t/s for parallel workers)          |
|  - Hugging Face Serverless (Qwen2.5-72B-Instruct)                       |
|  - Google Gemini Free Tier (gemini-2.5-flash / pro)                     |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
|                Parallel Workload Sharding & Evidence Extraction         |
|  - SearchAggregator (OpenAlex, arXiv, Wikipedia API)                    |
|  - Workload Sharder (30 sources -> 3 batches of 10 sources each)        |
|  - ParallelWorkerPool (N concurrent AI workers extracting raw text)     |
|  - Token Compression Engine (Raw HTML -> High-Signal Claims ~85% Saved) |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
|                       Synthesizer & Citation Engine                     |
|  - Cross-Source Evidence Merging      - Contradiction Detection         |
|  - Research Gap Discovery             - Exact Traceable Citations       |
+-------------------------------------------------------------------------+
```

---

## 2. Token Minimization & Worker Sharding

- **Worker Sharding**: When 30 URLs or research papers are retrieved, the `ParallelWorkerPool` shards them into batches of 10.
- **Concurrent Execution**: Fast free models (like Groq `llama-3.1-8b-instant` or OpenRouter) run in parallel over each batch.
- **Evidence Compression**: Instead of passing 50,000+ raw webpage tokens to the reasoning model, each worker produces structured JSON claims and supporting quotes (~2,000 tokens total), saving over 85% in token context.
