from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ResearchCreateRequest(BaseModel):
    question: str = Field(..., min_length=3, description="The user's research inquiry or prompt.")
    intent: Optional[str] = Field(default="general_research", description="Classified or requested intent category.")
    depth: Optional[str] = Field(default="standard", description="Research depth level: quick, standard, or deep.")
    project_id: Optional[str] = Field(default=None, description="Optional project workspace identifier.")
    user_id: Optional[str] = Field(default=None, description="Optional user ID.")
    options: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Fine-grained research flags and filters.")


class ResearchTaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: Optional[str] = None
    purpose: Optional[str] = None
    priority: int = 1
    status: str
    source_types: List[str] = []
    coverage_score: float = 0.0


class ResearchEventSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    research_run_id: str
    event_type: str
    stage: Optional[str] = None
    message: str
    payload: Dict[str, Any] = {}
    created_at: datetime


class ResearchRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    question: str
    intent: str
    depth: str
    status: str
    progress_percentage: int
    current_stage: str
    summary: Optional[str] = None
    error_message: Optional[str] = None
    plan: Dict[str, Any] = {}
    stats: Dict[str, Any] = {}
    options: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime
    tasks: Optional[List[ResearchTaskSchema]] = []


class ResearchRunCreateResponse(BaseModel):
    research_id: str
    question: str
    status: str
    created_at: datetime
    stream_url: str
