from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app import crud, schemas
from backend.app.database import get_db

router = APIRouter()

@router.get("/logs", response_model=list[schemas.AgentLogRead])
def get_agent_logs(workflow_id: int = None, db: Session = Depends(get_db)):
    return crud.list_agent_logs(db, workflow_id=workflow_id)
