# ResearchOS — REST & SSE API Specification

Base URL: `http://localhost:5000/api`

---

## 1. System & Health

### `GET /health`
Returns system component status (database, redis, active workers).

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "services": {
    "database": "connected",
    "redis": "connected"
  },
  "timestamp": "2026-09-07T11:00:00Z"
}
```

---

## 2. Research Runs

### `POST /research`
Initiates a new research run.

**Request Body:**
```json
{
  "question": "Can multimodal RAG improve classroom assessment systems?",
  "intent": "academic_research",
  "depth": "deep",
  "project_id": null,
  "options": {
    "include_academic": true,
    "include_web": true,
    "include_github": true,
    "include_reddit": false
  }
}
```

**Response (202 Accepted):**
```json
{
  "research_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "question": "Can multimodal RAG improve classroom assessment systems?",
  "status": "queued",
  "created_at": "2026-09-07T11:00:00Z",
  "stream_url": "/api/research/9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d/stream"
}
```

---

### `GET /research`
Lists past research runs with pagination.

**Query Parameters:**
- `limit` (default: 20)
- `offset` (default: 0)

---

### `GET /research/{research_id}`
Fetches the detailed status, research plan, summary, and current findings for a specific research run.

---

### `GET /research/{research_id}/events`
Fetches the chronological list of all state changes and log events emitted during the research run.

---

### `GET /research/{research_id}/stream`
Server-Sent Events (SSE) live stream delivering real-time execution events (`planning_started`, `plan_created`, `search_completed`, `evidence_found`, `gap_analysis_started`, `report_generated`, `research_completed`).
