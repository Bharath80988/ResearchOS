from sqlalchemy import String, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..base import BaseModel


class UserMemory(BaseModel):
    __tablename__ = "user_memory"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(64), default="preference") # preference, tech_stack, research_interest, constraint
    key: Mapped[str] = mapped_column(String(128), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[dict] = mapped_column(JSON, default=dict)


class ProjectMemory(BaseModel):
    __tablename__ = "project_memory"

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    topic: Mapped[str] = mapped_column(String(128), nullable=False)
    content: Mapped[Text] = mapped_column(Text, nullable=False)
    metadata_info: Mapped[dict] = mapped_column(JSON, default=dict)


class ResearchMemory(BaseModel):
    __tablename__ = "research_memory"

    research_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_runs.id"), nullable=False, index=True)
    summary_key: Mapped[str] = mapped_column(String(128), nullable=False)
    distilled_knowledge: Mapped[str] = mapped_column(Text, nullable=False)
    keywords: Mapped[list] = mapped_column(JSON, default=list)
