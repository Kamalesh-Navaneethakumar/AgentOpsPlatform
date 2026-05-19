from sqlalchemy.orm import Session
from backend.app import models, schemas


def create_workflow(db: Session, workflow_data: schemas.WorkflowCreate) -> models.Workflow:
    workflow = models.Workflow(
        name=workflow_data.name,
        description=workflow_data.description,
        input_document=workflow_data.input_document,
        priority=workflow_data.priority,
        approval_required=workflow_data.approval_required,
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow


def get_workflow(db: Session, workflow_id: int):
    return db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()


def update_workflow(db: Session, workflow_id: int, update_data: schemas.WorkflowUpdate):
    workflow = get_workflow(db, workflow_id)
    if not workflow:
        return None
    for field, value in update_data.dict(exclude_none=True).items():
        setattr(workflow, field, value)
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow


def list_workflows(db: Session, limit: int = 50):
    return db.query(models.Workflow).order_by(models.Workflow.created_at.desc()).limit(limit).all()


def create_agent_log(db: Session, log_data: schemas.AgentLogCreate):
    log = models.AgentLog(**log_data.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def list_agent_logs(db: Session, workflow_id: int = None, limit: int = 100):
    query = db.query(models.AgentLog).order_by(models.AgentLog.created_at.desc())
    if workflow_id is not None:
        query = query.filter(models.AgentLog.workflow_id == workflow_id)
    return query.limit(limit).all()
