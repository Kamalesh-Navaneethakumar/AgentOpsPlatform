from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app import crud, schemas
from backend.app.database import get_db
from backend.app.agents.orchestrator import AgentOrchestrator
from backend.app.services.approvals import approve_workflow, require_approval

router = APIRouter()

@router.post("/", response_model=schemas.WorkflowRead)
def create_workflow(workflow: schemas.WorkflowCreate, db: Session = Depends(get_db)):
    created = crud.create_workflow(db, workflow)
    orchestrator = AgentOrchestrator(db)
    orchestrator.run_workflow(created, approval_required=workflow.approval_required)
    return created

@router.get("/{workflow_id}", response_model=schemas.WorkflowRead)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    workflow = crud.get_workflow(db, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.get("/", response_model=list[schemas.WorkflowRead])
def list_workflows(db: Session = Depends(get_db)):
    return crud.list_workflows(db)

@router.post("/approve", response_model=schemas.WorkflowRead)
def approve(decision: schemas.ApprovalDecision, db: Session = Depends(get_db)):
    workflow = crud.get_workflow(db, decision.workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if not require_approval(workflow, db):
        raise HTTPException(status_code=400, detail="Workflow does not require approval or is already approved")
    updated = approve_workflow(db, decision)
    return updated
