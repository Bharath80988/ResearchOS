from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Generator
from dataclasses import dataclass, field
from enum import Enum


class ModelTier(str, Enum):
    REASONING = "reasoning"   # DeepSeek R1, Gemini Pro, Llama 70B
    FAST = "fast"             # Llama 3.1 8B, Gemini Flash
    WORKER = "worker"         # Fast parallel source extractors


@dataclass
class LLMResponse:
    content: str
    parsed_json: Optional[Dict[str, Any]] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model: str = ""
    provider: str = ""
    latency_ms: float = 0.0
    raw_response: Optional[Any] = None


class BaseLLMProvider(ABC):
    """Abstract interface for all LLM providers (Free, Serverless, and Commercial)."""

    def __init__(self, api_key: Optional[str] = None, default_model: Optional[str] = None):
        self.api_key = api_key
        self.default_model = default_model

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        """Generates text completion."""
        pass

    @abstractmethod
    def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        """Generates guaranteed structured JSON output."""
        pass

    @abstractmethod
    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> Generator[str, None, None]:
        """Streams token chunks."""
        pass

    def is_available(self) -> bool:
        """Returns True if this provider is configured and available."""
        return bool(self.api_key)
