from sqlalchemy import String, Text, JSON, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..base import BaseModel


class LLMCall(BaseModel):
    __tablename__ = "llm_calls"

    research_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_runs.id"), nullable=True, index=True)
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    model: Mapped[str] = mapped_column(String(128), nullable=False)
    task_name: Mapped[str] = mapped_column(String(128), nullable=False)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(32), default="success") # success, failed, fallback
    error: Mapped[str] = mapped_column(Text, nullable=True)


class ToolCall(BaseModel):
    __tablename__ = "tool_calls"

    research_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_runs.id"), nullable=True, index=True)
    tool_name: Mapped[str] = mapped_column(String(64), nullable=False)
    query: Mapped[str] = mapped_column(String(512), nullable=True)
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    results_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(32), default="success")
    error: Mapped[str] = mapped_column(Text, nullable=True)
    call_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
