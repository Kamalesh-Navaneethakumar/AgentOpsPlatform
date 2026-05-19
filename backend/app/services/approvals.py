from backend.app import crud, schemas
from sqlalchemy.orm import Session


def require_approval(workflow, db: Session):
    if workflow.approval_required and not workflow.approved:
        return True
    return False


def approve_workflow(db: Session, decision: schemas.ApprovalDecision):
    workflow = crud.get_workflow(db, decision.workflow_id)
    if not workflow:
        return None
    workflow.approved = decision.approved
    workflow.status = "approved" if decision.approved else "rejected"
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow
