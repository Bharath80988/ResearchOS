import json
import time
import httpx
from typing import Optional, Dict, Any, Generator
from ..base import BaseLLMProvider, LLMResponse
from ...utils import logger


class HuggingFaceProvider(BaseLLMProvider):
    """
    Hugging Face Serverless Inference API (Free Tier):
    - Qwen/Qwen2.5-72B-Instruct
    - mistralai/Mistral-7B-Instruct-v0.3
    """

    BASE_URL = "https://api-inference.huggingface.co/models"

    def __init__(self, api_key: Optional[str] = None, default_model: str = "Qwen/Qwen2.5-72B-Instruct"):
        super().__init__(api_key=api_key, default_model=default_model)

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

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
        url = f"{self.BASE_URL}/{target_model}"

        full_prompt = f"System: {system_prompt}\nUser: {prompt}\nAssistant:" if system_prompt else prompt

        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": max(temperature, 0.01),
                "return_full_text": False,
            },
            "options": {"wait_for_model": True},
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                res = client.post(url, headers=self._get_headers(), json=payload)
                res.raise_for_status()
                data = res.json()

            latency = (time.time() - start_time) * 1000
            
            if isinstance(data, list) and len(data) > 0:
                content = data[0].get("generated_text", "")
            elif isinstance(data, dict):
                content = data.get("generated_text", "")
            else:
                content = str(data)

            return LLMResponse(
                content=content,
                prompt_tokens=len(full_prompt) // 4,
                completion_tokens=len(content) // 4,
                total_tokens=(len(full_prompt) + len(content)) // 4,
                model=target_model,
                provider="huggingface",
                latency_ms=latency,
                raw_response=data,
            )
        except Exception as e:
            logger.error(f"HuggingFace generate error ({target_model}): {e}")
            raise

    def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        sys = (system_prompt or "") + "\nRespond with valid raw JSON only. Do not include markdown codeblocks."
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
            logger.warning(f"Could not parse structured JSON from HuggingFace: {ex}")
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
        # Serverless HTTP fallback streaming (yield full output in chunks)
        resp = self.generate(prompt=prompt, system_prompt=system_prompt, model=model, temperature=temperature, max_tokens=max_tokens)
        words = resp.content.split(" ")
        for word in words:
            yield word + " "
            time.sleep(0.02)
