# ResearchOS — Development Guide

## Environment Setup

### 1. Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 16 with pgvector extension (or Docker)
- Redis 7+ (or Docker)

---

## Running the Development Servers

### 1. Start Support Services (Postgres & Redis)
```bash
docker compose up -d postgres redis
```

### 2. Configure Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Initialize Database & Run Backend
```bash
# In backend directory with virtualenv active
python run.py
```
The backend API server will listen on `http://127.0.0.1:5000`.

### 4. Run Frontend
```bash
cd frontend
npm install
npm run dev
```
The Vite development server will listen on `http://localhost:5173`.

---

## Running Tests

### Backend Unit & Integration Tests
```bash
cd backend
pytest -v
```
