from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from backend.app.database import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="pending")
    priority = Column(String(50), default="normal")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    input_document = Column(Text)
    output_summary = Column(Text)
    tasks = Column(JSON, default=[])
    observation = Column(JSON, default={})
    approval_required = Column(Boolean, default=True)
    approved = Column(Boolean, default=False)

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, nullable=False)
    agent_name = Column(String(100), nullable=False)
    prompt = Column(Text)
    response = Column(Text)
    status = Column(String(30), default="success")
    latency_ms = Column(Integer, default=0)
    retries = Column(Integer, default=0)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
