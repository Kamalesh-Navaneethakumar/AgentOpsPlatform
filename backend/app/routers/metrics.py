from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app import crud
from backend.app.database import get_db

router = APIRouter()

@router.get("/summary")
def get_metrics(db: Session = Depends(get_db)):
    workflows = crud.list_workflows(db, limit=200)
    total = len(workflows)
    approvals_pending = sum(1 for item in workflows if item.status == "approval_pending")
    failed = sum(1 for item in workflows if item.status == "failed")
    completed = sum(1 for item in workflows if item.status == "completed")
    return {
        "total_workflows": total,
        "approvals_pending": approvals_pending,
        "failed_workflows": failed,
        "completed_workflows": completed,
    }
