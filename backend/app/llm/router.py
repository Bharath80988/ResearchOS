from typing import Dict, Optional, List, Generator
from .base import BaseLLMProvider, LLMResponse, ModelTier
from .providers.openrouter import OpenRouterProvider
from .providers.groq import GroqProvider
from .providers.huggingface import HuggingFaceProvider
from .providers.gemini import GeminiProvider
from ..config import get_settings
from ..utils import logger

settings = get_settings()


class LLMRouter:
    """
    Intelligent LLM Router that manages multi-provider dispatching,
    free-tier model selection, automatic retries, and fallback pipelines.
    """

    def __init__(self):
        self.providers: Dict[str, BaseLLMProvider] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        # OpenRouter (Free DeepSeek R1, DeepSeek V3, Llama 3.3, Qwen)
        self.providers["openrouter"] = OpenRouterProvider(
            api_key=settings.OPENROUTER_API_KEY,
            default_model=settings.DEFAULT_REASONING_MODEL
        )
        # Groq (Free Fast Inference)
        self.providers["groq"] = GroqProvider(
            api_key=settings.GROQ_API_KEY,
            default_model=settings.DEFAULT_WORKER_MODEL
        )
        # Hugging Face (Free Serverless Inference)
        self.providers["huggingface"] = HuggingFaceProvider(
            api_key=settings.HUGGINGFACE_API_KEY,
            default_model="Qwen/Qwen2.5-72B-Instruct"
        )
        # Gemini (Free Tier)
        self.providers["gemini"] = GeminiProvider(
            api_key=settings.GEMINI_API_KEY,
            default_model=settings.DEFAULT_FAST_MODEL
        )

    def get_provider(self, provider_name: Optional[str] = None) -> BaseLLMProvider:
        """Retrieves specific provider or active default."""
        if provider_name and provider_name in self.providers:
            return self.providers[provider_name]
        
        # Check active configured default
        def_name = settings.DEFAULT_LLM_PROVIDER
        if def_name in self.providers and self.providers[def_name].is_available():
            return self.providers[def_name]

        # Auto fallback to any available configured provider
        for name, prov in self.providers.items():
            if prov.is_available():
                return prov

        # Return default provider instance (will attempt execution or mock fallback)
        return self.providers.get("openrouter")

    def route_for_tier(self, tier: ModelTier) -> BaseLLMProvider:
        """Selects optimal provider/model for the given task tier."""
        if tier == ModelTier.WORKER or tier == ModelTier.FAST:
            # Prefer ultra-fast Groq for parallel workers, or Gemini Flash
            if self.providers["groq"].is_available():
                return self.providers["groq"]
            if self.providers["gemini"].is_available():
                return self.providers["gemini"]

        if tier == ModelTier.REASONING:
            # Prefer OpenRouter DeepSeek-R1 / Qwen, or Gemini Pro
            if self.providers["openrouter"].is_available():
                return self.providers["openrouter"]
            if self.providers["gemini"].is_available():
                return self.providers["gemini"]

        return self.get_provider()

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        tier: ModelTier = ModelTier.REASONING,
        provider_name: Optional[str] = None,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        provider = self.get_provider(provider_name) if provider_name else self.route_for_tier(tier)
        try:
            return provider.generate(prompt=prompt, system_prompt=system_prompt, max_tokens=max_tokens)
        except Exception as e:
            logger.warning(f"Primary provider {provider.__class__.__name__} failed: {e}. Attempting fallback.")
            for fallback_name, fallback_prov in self.providers.items():
                if fallback_prov != provider and fallback_prov.is_available():
                    try:
                        return fallback_prov.generate(prompt=prompt, system_prompt=system_prompt, max_tokens=max_tokens)
                    except Exception:
                        continue
            raise

    def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        tier: ModelTier = ModelTier.REASONING,
        provider_name: Optional[str] = None,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        provider = self.get_provider(provider_name) if provider_name else self.route_for_tier(tier)
        try:
            return provider.generate_structured(prompt=prompt, system_prompt=system_prompt, max_tokens=max_tokens)
        except Exception as e:
            logger.warning(f"Structured generation on {provider.__class__.__name__} failed: {e}. Trying fallback.")
            for fallback_name, fallback_prov in self.providers.items():
                if fallback_prov != provider and fallback_prov.is_available():
                    try:
                        return fallback_prov.generate_structured(prompt=prompt, system_prompt=system_prompt, max_tokens=max_tokens)
                    except Exception:
                        continue
            raise

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        tier: ModelTier = ModelTier.REASONING,
        provider_name: Optional[str] = None,
        max_tokens: int = 2048,
    ) -> Generator[str, None, None]:
        provider = self.get_provider(provider_name) if provider_name else self.route_for_tier(tier)
        return provider.stream(prompt=prompt, system_prompt=system_prompt, max_tokens=max_tokens)


# Global router singleton
router = LLMRouter()
