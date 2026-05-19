from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    input_document: str
    priority: Optional[str] = "normal"
    approval_required: Optional[bool] = True

class WorkflowUpdate(BaseModel):
    status: Optional[str]
    approved: Optional[bool]
    output_summary: Optional[str]
    tasks: Optional[List[Dict[str, Any]]]
    observation: Optional[Dict[str, Any]]

class WorkflowRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    priority: str
    input_document: str
    output_summary: Optional[str]
    tasks: List[Dict[str, Any]]
    observation: Dict[str, Any]
    approval_required: bool
    approved: bool

    class Config:
        orm_mode = True

class AgentLogCreate(BaseModel):
    workflow_id: int
    agent_name: str
    prompt: str
    response: str
    status: str
    latency_ms: int
    retries: int
    error_message: Optional[str] = None

class AgentLogRead(BaseModel):
    id: int
    workflow_id: int
    agent_name: str
    prompt: str
    response: str
    status: str
    latency_ms: int
    retries: int
    error_message: Optional[str]

    class Config:
        orm_mode = True

class ApprovalDecision(BaseModel):
    workflow_id: int
    approved: bool
    note: Optional[str] = None
