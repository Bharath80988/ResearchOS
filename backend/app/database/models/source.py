from sqlalchemy import String, Text, JSON, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import BaseModel

# Optional pgvector support
try:
    from pgvector.sqlalchemy import Vector
    VectorColumn = Vector(768)
except ImportError:
    VectorColumn = JSON


class Source(BaseModel):
    __tablename__ = "sources"

    research_run_id: Mapped[str] = mapped_column(String(36), ForeignKey("research_runs.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=True, index=True)
    source_type: Mapped[str] = mapped_column(String(64), default="web", index=True) # web, academic, reddit, github
    domain: Mapped[str] = mapped_column(String(255), nullable=True)
    author: Mapped[str] = mapped_column(String(255), nullable=True)
    published_at: Mapped[str] = mapped_column(String(64), nullable=True)
    doi: Mapped[str] = mapped_column(String(128), nullable=True, index=True)
    
    # Source Quality Profile
    quality_score: Mapped[float] = mapped_column(Float, default=0.5)
    is_peer_reviewed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_official_docs: Mapped[bool] = mapped_column(Boolean, default=False)
    citation_count: Mapped[int] = mapped_column(Integer, default=0)
    source_metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    documents = relationship("Document", back_populates="source", cascade="all, delete-orphan")


class Document(BaseModel):
    __tablename__ = "documents"

    source_id: Mapped[str] = mapped_column(String(36), ForeignKey("sources.id"), nullable=False, index=True)
    content_type: Mapped[str] = mapped_column(String(64), default="text/html")
    raw_content: Mapped[str] = mapped_column(Text, nullable=True)
    cleaned_content: Mapped[str] = mapped_column(Text, nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0)
    doc_metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    source = relationship("Source", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(BaseModel):
    __tablename__ = "document_chunks"

    document_id: Mapped[str] = mapped_column(String(36), ForeignKey("documents.id"), nullable=False, index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, default=0)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    section: Mapped[str] = mapped_column(String(255), nullable=True)
    page_number: Mapped[int] = mapped_column(Integer, nullable=True)
    token_count: Mapped[int] = mapped_column(Integer, default=0)
    chunk_hash: Mapped[str] = mapped_column(String(64), index=True)
    embedding: Mapped[list] = mapped_column(VectorColumn, nullable=True)

    document = relationship("Document", back_populates="chunks")
