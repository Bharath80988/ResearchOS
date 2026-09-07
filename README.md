# ResearchOS 🔬

**ResearchOS** is a production-grade, provider-agnostic Deep Research Engine and research workstation designed for academic, technical, market, competitive, and scientific investigations.

Unlike standard conversational chatbots or basic naive RAG demos, ResearchOS conducts iterative, multi-stage deep research: planning investigation strategies, searching cross-domain indexes, crawling and parsing structured evidence, verifying claims against sources, detecting conflicting findings, identifying underexplored research gaps, and synthesizing traceable, citation-backed reports.

---

## 🏛️ System Architecture

```
User Question
     ↓
[Intent Classifier] ────────────→ [Research Planner]
                                         ↓
                                [Query Decomposer]
                                         ↓
   [Parallel Multi-Source Search (Academic, Web, Reddit, GitHub)]
                                         ↓
                      [Crawler & Document Ingestion]
                                         ↓
               [Hybrid Search & Reranker (pgvector + BM25)]
                                         ↓
                     [Evidence Ledger & Claim Tracker]
                                         ↓
                 [Contradiction & Disagreement Detection]
                                         ↓
                     [Research Coverage Evaluator]
                       ├── Insufficient → Loop back for new queries
                       └── Sufficient → Proceed
                                         ↓
                    [Research Gap & Novelty Analyzer]
                                         ↓
                     [Citation-Validated Synthesizer]
                                         ↓
                      Final Comprehensive Report
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Node.js 20+** and **npm**
- *(Optional)* **Docker & Docker Compose** for running PostgreSQL + pgvector & Redis

### 1. Clone & Configure Environment
```bash
cp .env.example .env
```
Edit `.env` to configure your API keys (e.g. `GEMINI_API_KEY`, `GROQ_API_KEY`, `OPENROUTER_API_KEY`) and database parameters.

### 2. Run with Docker Compose (Recommended)
```bash
docker compose up --build
```
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:5000`

### 3. Run Locally for Development

#### Backend:
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
python run.py
```

#### Frontend:
```bash
cd frontend
npm install
npm run dev
```

---

## 📚 Documentation (`docs/`)
All detailed specifications and developer guides are located in the [**`docs/`**](docs/README.md) directory:
- [System Architecture](docs/ARCHITECTURE.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [REST & SSE API Specification](docs/API.md)
- [Database Schema & Vectors](docs/DATABASE.md)
- [Deep Research Engine Specification](docs/RESEARCH_ENGINE.md)
- [Evaluation & Benchmarking Framework](docs/EVALUATION.md)

---

## 🛡️ License
Apache-2.0 License.
