from sqlalchemy import String, Text, JSON, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import BaseModel


class Claim(BaseModel):
    __tablename__ = "claims"

    research_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_runs.id"), nullable=False, index=True)
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    claim_type: Mapped[str] = mapped_column(String(64), default="empirical") # empirical, methodological, theoretical, comparative
    confidence: Mapped[float] = mapped_column(Float, default=0.8)
    corroboration_count: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(32), default="verified") # verified, disputed, unverified

    evidence_items = relationship("Evidence", back_populates="claim", cascade="all, delete-orphan")


class Evidence(BaseModel):
    __tablename__ = "evidence"

    claim_id: Mapped[str] = mapped_column(String(36), ForeignKey("claims.id"), nullable=False, index=True)
    chunk_id: Mapped[str] = mapped_column(String(36), ForeignKey("document_chunks.id"), nullable=True, index=True)
    exact_passage: Mapped[str] = mapped_column(Text, nullable=False)
    section: Mapped[str] = mapped_column(String(255), nullable=True)
    page_number: Mapped[int] = mapped_column(Integer, nullable=True)
    support_score: Mapped[float] = mapped_column(Float, default=0.9)
    metadata_info: Mapped[dict] = mapped_column(JSON, default=dict)

    claim = relationship("Claim", back_populates="evidence_items")


class Contradiction(BaseModel):
    __tablename__ = "contradictions"

    research_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_runs.id"), nullable=False, index=True)
    claim_a: Mapped[str] = mapped_column(Text, nullable=False)
    claim_b: Mapped[str] = mapped_column(Text, nullable=False)
    source_a_id: Mapped[str] = mapped_column(String(36), ForeignKey("sources.id"), nullable=True)
    source_b_id: Mapped[str] = mapped_column(String(36), ForeignKey("sources.id"), nullable=True)
    divergence_reason: Mapped[str] = mapped_column(Text, nullable=True) # e.g. different datasets, metrics, environments
    significance: Mapped[str] = mapped_column(String(32), default="moderate")


class ResearchGap(BaseModel):
    __tablename__ = "research_gaps"

    research_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_runs.id"), nullable=False, index=True)
    gap_title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    gap_type: Mapped[str] = mapped_column(String(64), default="methodology") # methodology, evaluation, dataset, cross-domain
    supporting_limitations: Mapped[list] = mapped_column(JSON, default=list)
    suggested_direction: Mapped[str] = mapped_column(Text, nullable=True)
    research_strength: Mapped[str] = mapped_column(String(64), default="potentially novel")
