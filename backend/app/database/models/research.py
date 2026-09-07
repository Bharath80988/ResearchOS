from datetime import datetime, timezone
from sqlalchemy import String, Text, JSON, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import BaseModel


class ResearchRun(BaseModel):
    __tablename__ = "research_runs"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"), nullable=True, index=True)
    
    question: Mapped[str] = mapped_column(Text, nullable=False)
    intent: Mapped[str] = mapped_column(String(64), default="general_research", index=True)
    depth: Mapped[str] = mapped_column(String(32), default="standard")
    status: Mapped[str] = mapped_column(String(32), default="queued", index=True) # queued, planning, searching, analyzing, synthesizing, completed, failed
    
    progress_percentage: Mapped[int] = mapped_column(Integer, default=0)
    current_stage: Mapped[str] = mapped_column(String(64), default="initialized")
    
    plan: Mapped[dict] = mapped_column(JSON, default=dict)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    
    options: Mapped[dict] = mapped_column(JSON, default=dict)
    stats: Mapped[dict] = mapped_column(JSON, default=dict) # iterations, sources_count, claims_count, tokens, cost
    
    user = relationship("User", back_populates="research_runs")
    project = relationship("Project", back_populates="research_runs")
    tasks = relationship("ResearchTask", back_populates="research_run", cascade="all, delete-orphan", order_by="ResearchTask.priority")
    queries = relationship("ResearchQuery", back_populates="research_run", cascade="all, delete-orphan")
    events = relationship("ResearchEvent", back_populates="research_run", cascade="all, delete-orphan", order_by="ResearchEvent.created_at")
    reports = relationship("ResearchReport", back_populates="research_run", cascade="all, delete-orphan")


class ResearchTask(BaseModel):
    __tablename__ = "research_tasks"

    research_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_runs.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    purpose: Mapped[str] = mapped_column(String(255), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(32), default="pending") # pending, in_progress, completed, failed
    source_types: Mapped[list] = mapped_column(JSON, default=list)
    completion_criteria: Mapped[str] = mapped_column(Text, nullable=True)
    coverage_score: Mapped[float] = mapped_column(Float, default=0.0)

    research_run = relationship("ResearchRun", back_populates="tasks")


class ResearchQuery(BaseModel):
    __tablename__ = "research_queries"

    research_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_runs.id"), nullable=False, index=True)
    task_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_tasks.id"), nullable=True, index=True)
    query_text: Mapped[str] = mapped_column(String(512), nullable=False)
    strategy: Mapped[str] = mapped_column(String(64), default="broad") # broad, precise, academic, recent, contradictory, limitation
    source_type: Mapped[str] = mapped_column(String(64), default="web") # web, academic, reddit, github
    results_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(32), default="executed")

    research_run = relationship("ResearchRun", back_populates="queries")


class ResearchEvent(BaseModel):
    __tablename__ = "research_events"

    research_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_runs.id"), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    stage: Mapped[str] = mapped_column(String(64), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)

    research_run = relationship("ResearchRun", back_populates="events")
