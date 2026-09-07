from sqlalchemy import String, JSON, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    preferences: Mapped[dict] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    research_runs = relationship("ResearchRun", back_populates="user", cascade="all, delete-orphan")


class Project(BaseModel):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True, nullable=True)
    context_metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    owner = relationship("User", back_populates="projects")
    research_runs = relationship("ResearchRun", back_populates="project", cascade="all, delete-orphan")
