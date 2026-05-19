from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import init_db
from backend.app.routers.workflows import router as workflows_router
from backend.app.routers.agents import router as agents_router
from backend.app.routers.metrics import router as metrics_router

app = FastAPI(
    title="AgentOps Workflow Orchestration",
    description="Enterprise AI workflow orchestration with multi-agent collaboration.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflows_router, prefix="/api/workflows", tags=["workflows"])
app.include_router(agents_router, prefix="/api/agents", tags=["agents"])
app.include_router(metrics_router, prefix="/api/metrics", tags=["metrics"])

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "AgentOps"}
