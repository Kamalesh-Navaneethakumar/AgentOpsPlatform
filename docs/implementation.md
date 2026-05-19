# Implementation Guide

This guide walks through the platform module by module.

## 1. Configuration
`backend/app/config.py` loads environment variables and defines runtime settings:
- `DATABASE_URL` for SQLite or PostgreSQL
- `AI_PROVIDER` to switch between OpenAI or Gemini
- retry and logging settings

## 2. Database
`backend/app/database.py` creates the SQLAlchemy engine and session factory.
`init_db()` creates tables at startup.

## 3. Models and schemas
`backend/app/models.py` defines `Workflow` and `AgentLog` tables.
`backend/app/schemas.py` defines the API contract using Pydantic.

## 4. CRUD
`backend/app/crud.py` provides reusable database functions for create, read, update, and list operations.

## 5. AI Services
`backend/app/services/ai_client.py` wraps OpenAI / Gemini calls.
`backend/app/services/retries.py` retries failed AI calls with backoff.
`backend/app/services/observability.py` standardizes logs for prompt-level telemetry.
`backend/app/services/approvals.py` handles human approval workflows.

## 6. Agents
Each specialized agent extends `BaseAgent`:
- `DocumentAnalysisAgent`
- `SummarizationAgent`
- `TaskExtractionAgent`
- `PriorityClassificationAgent`
- `ReportingAgent`

The orchestrator coordinates agents and persists progress.

## 7. API routes
API endpoints are grouped by responsibility:
- `/api/workflows/` for workflow lifecycle actions
- `/api/agents/logs` for agent observability
- `/api/metrics/summary` for dashboard metrics

## 8. Frontend
The Streamlit app at `frontend/streamlit_app.py` lets users:
- create workflows
- view workflow status
- approve or reject pending workflows
- inspect agent logs and metrics

## 9. Running the project
1. Install dependencies
2. Set environment variables in `.env`
3. Run backend and frontend separately
4. Use the UI to test workflows and approval flow
