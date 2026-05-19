# AgentOps Architecture

## Overview
AgentOps is built as a modular, API-first platform with separate backend and frontend layers.

- `backend/app/` contains the FastAPI service, database models, AI agents, orchestration logic, and business APIs.
- `frontend/` contains a Streamlit dashboard for workflow creation, approval, observability, and metrics.
- `docs/` contains architecture and implementation documentation that explains the design choices.

## Backend layers

1. `config.py` — application settings, environment variables, and provider selection.
2. `database.py` — SQLAlchemy database initialization and session management.
3. `models.py` — persistent workflow and agent log entities.
4. `schemas.py` — Pydantic request/response structures.
5. `crud.py` — database operations for workflows and logs.
6. `services/` — AI provider client, retry decorators, approval utilities, and observability metadata.
7. `agents/` — specialized AI components for document analysis, summarization, task extraction, priority classification, reporting, and the orchestrator.
8. `routers/` — HTTP endpoints for workflows, agent logs, and metrics.

## Workflow flow

1. Create a workflow via the API.
2. `AgentOrchestrator` runs each agent sequentially.
3. Each agent logs its prompt, response, latency, and status.
4. The workflow enters approval pending state if human signoff is required.
5. Approval decisions update workflow status and let stakeholders finalize actions.
