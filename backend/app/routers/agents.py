from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app import crud, schemas
from backend.app.database import get_db
from pydantic import BaseModel

from backend.app.services.langchain_rag import rag_answer

router = APIRouter()


@router.get("/logs", response_model=list[schemas.AgentLogRead])
def get_agent_logs(workflow_id: int = None, db: Session = Depends(get_db)):
    return crud.list_agent_logs(db, workflow_id=workflow_id)


class RAGRequest(BaseModel):
    document: str
    question: str


@router.post("/rag/query")
def rag_query(payload: RAGRequest):
    try:
        return rag_answer(payload.document, payload.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
