# AgentOps AI Workflow Orchestration Platform

A production-style Python project that simulates enterprise AI operations with multiple collaborating agents. The platform combines a FastAPI backend, Streamlit frontend, SQLite data persistence, and modular AI workflows.

## Core capabilities
- Multi-agent workflow orchestration
- Document analysis, summarization, task extraction, priority classification, reporting
- Human approval workflow before final action
- Observability dashboard for prompts, latency, retries, failures, and metrics
- API-first architecture with modular services

## Quick start
1. Create a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create `.env` from `.env.example` and set `OPENAI_API_KEY`.
3. Start the backend:
   ```bash
   uvicorn backend.app.main:app --reload --port 8000
   ```
4. Start the frontend:
   ```bash
   streamlit run frontend/streamlit_app.py
   ```

## Folder structure
- `backend/app/` — FastAPI app, database, agents, services, routers
- `frontend/` — Streamlit observability dashboard and workflow UI
- `docs/` — architecture and implementation guidance

## Next steps
- Connect to PostgreSQL by updating `DATABASE_URL`
- Add production-grade auth and role-based approval
- Extend the agent orchestration pipeline with new workflow steps
