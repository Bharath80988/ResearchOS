import json
import time
import httpx
from typing import Optional, Dict, Any, Generator
from ..base import BaseLLMProvider, LLMResponse
from ...utils import logger


class OpenRouterProvider(BaseLLMProvider):
    """
    OpenRouter API Provider supporting Free Tier models:
    - deepseek/deepseek-r1:free
    - deepseek/deepseek-chat:free
    - meta-llama/llama-3.3-70b-instruct:free
    - qwen/qwen-2.5-72b-instruct:free
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: Optional[str] = None, default_model: str = "deepseek/deepseek-r1:free"):
        super().__init__(api_key=api_key, default_model=default_model)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key or ''}",
            "HTTP-Referer": "https://github.com/researchos/researchos",
            "X-Title": "ResearchOS",
            "Content-Type": "application/json",
        }

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
            with httpx.Client(timeout=45.0) as client:
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
                provider="openrouter",
                latency_ms=latency,
                raw_response=data,
            )
        except Exception as e:
            logger.error(f"OpenRouter generate error ({target_model}): {e}")
            raise

    def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        sys = (system_prompt or "") + "\nRespond with valid, raw JSON only. Do not include markdown formatting or backticks."
        resp = self.generate(prompt=prompt, system_prompt=sys, model=model, temperature=temperature, max_tokens=max_tokens)
        
        # Clean potential markdown wrapping
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
            logger.warning(f"Could not parse structured JSON from OpenRouter output: {ex}")
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

        with httpx.Client(timeout=45.0) as client:
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
