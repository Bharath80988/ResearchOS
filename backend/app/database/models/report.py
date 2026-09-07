from sqlalchemy import String, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import BaseModel


class ResearchReport(BaseModel):
    __tablename__ = "research_reports"

    research_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_runs.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    report_type: Mapped[str] = mapped_column(String(64), default="deep_research_report")
    executive_summary: Mapped[str] = mapped_column(Text, nullable=True)
    markdown_content: Mapped[str] = mapped_column(Text, nullable=False)
    sections_json: Mapped[dict] = mapped_column(JSON, default=dict)

    research_run = relationship("ResearchRun", back_populates="reports")
    citations = relationship("Citation", back_populates="report", cascade="all, delete-orphan")


class Citation(BaseModel):
    __tablename__ = "citations"

    report_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_reports.id"), nullable=False, index=True)
    source_id: Mapped[str] = mapped_column(String(36), ForeignKey("sources.id"), nullable=False, index=True)
    citation_key: Mapped[str] = mapped_column(String(64), nullable=False) # e.g. [1] or [Vaswani2017]
    citation_format_apa: Mapped[str] = mapped_column(Text, nullable=True)
    citation_format_bibtex: Mapped[str] = mapped_column(Text, nullable=True)
    citation_format_ieee: Mapped[str] = mapped_column(Text, nullable=True)
    verified: Mapped[bool] = mapped_column(default=True)

    report = relationship("ResearchReport", back_populates="citations")
