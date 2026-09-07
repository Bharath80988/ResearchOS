from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class SearchResult:
    title: str
    url: str
    source_type: str  # academic, web, github, reddit
    domain: str
    snippet: str
    author: Optional[str] = None
    published_at: Optional[str] = None
    doi: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    raw_content: Optional[str] = None


class BaseSearchTool(ABC):
    @abstractmethod
    def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        pass
