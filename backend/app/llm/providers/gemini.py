import json
import time
import httpx
from typing import Optional, Dict, Any, Generator
from ..base import BaseLLMProvider, LLMResponse
from ...utils import logger


class GeminiProvider(BaseLLMProvider):
    """
    Google Gemini API Provider (Free Tier):
    - gemini-2.5-flash
    - gemini-2.5-pro
    """

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

    def __init__(self, api_key: Optional[str] = None, default_model: str = "gemini-2.5-flash"):
        super().__init__(api_key=api_key, default_model=default_model)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        start_time = time.time()
        target_model = model or self.default_model
        url = f"{self.BASE_URL}/{target_model}:generateContent?key={self.api_key or ''}"

        contents = []
        if system_prompt:
            contents.append({"role": "user", "parts": [{"text": f"SYSTEM INSTRUCTION: {system_prompt}"}]})
            contents.append({"role": "model", "parts": [{"text": "Understood. I will follow instructions."}]})

        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }

        try:
            with httpx.Client(timeout=45.0) as client:
                res = client.post(url, json=payload)
                res.raise_for_status()
                data = res.json()

            latency = (time.time() - start_time) * 1000
            
            candidates = data.get("candidates", [])
            content = ""
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                content = "".join([p.get("text", "") for p in parts])

            usage = data.get("usageMetadata", {})

            return LLMResponse(
                content=content,
                prompt_tokens=usage.get("promptTokenCount", 0),
                completion_tokens=usage.get("candidatesTokenCount", 0),
                total_tokens=usage.get("totalTokenCount", 0),
                model=target_model,
                provider="gemini",
                latency_ms=latency,
                raw_response=data,
            )
        except Exception as e:
            logger.error(f"Gemini generate error ({target_model}): {e}")
            raise

    def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        sys = (system_prompt or "") + "\nRespond with valid, raw JSON only. Do not enclose in markdown blocks."
        resp = self.generate(prompt=prompt, system_prompt=sys, model=model, temperature=temperature, max_tokens=max_tokens)
        
        text = resp.content.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        try:
            resp.parsed_json = json.loads(text)
        except Exception as ex:
            logger.warning(f"Could not parse structured JSON from Gemini: {ex}")
            resp.parsed_json = {}

        return resp

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> Generator[str, None, None]:
        resp = self.generate(prompt=prompt, system_prompt=system_prompt, model=model, temperature=temperature, max_tokens=max_tokens)
        words = resp.content.split(" ")
        for word in words:
            yield word + " "
            time.sleep(0.01)
