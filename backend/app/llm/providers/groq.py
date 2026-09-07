import json
import time
import httpx
from typing import Optional, Dict, Any, Generator
from ..base import BaseLLMProvider, LLMResponse
from ...utils import logger


class GroqProvider(BaseLLMProvider):
    """
    Groq API Provider (Free Tier):
    - llama-3.3-70b-versatile
    - llama-3.1-8b-instant (Ideal for 300+ tokens/sec parallel worker extraction)
    """

    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, api_key: Optional[str] = None, default_model: str = "llama-3.1-8b-instant"):
        super().__init__(api_key=api_key, default_model=default_model)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key or ''}",
            "Content-Type": "application/json",
        }

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        start_time = time.time()
        target_model = model or self.default_model

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                res = client.post(self.BASE_URL, headers=self._get_headers(), json=payload)
                res.raise_for_status()
                data = res.json()

            latency = (time.time() - start_time) * 1000
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})

            return LLMResponse(
                content=content,
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                model=target_model,
                provider="groq",
                latency_ms=latency,
                raw_response=data,
            )
        except Exception as e:
            logger.error(f"Groq generate error ({target_model}): {e}")
            raise

    def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        sys = (system_prompt or "") + "\nYou MUST output valid raw JSON only. Do not enclose in markdown blocks."
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
            logger.warning(f"Could not parse structured JSON from Groq: {ex}")
            resp.parsed_json = {}

        return resp

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 2048,
    ) -> Generator[str, None, None]:
        target_model = model or self.default_model
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }

        with httpx.Client(timeout=30.0) as client:
            with client.stream("POST", self.BASE_URL, headers=self._get_headers(), json=payload) as response:
                for line in response.iter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            token = chunk["choices"][0]["delta"].get("content", "")
                            if token:
                                yield token
                        except Exception:
                            continue
