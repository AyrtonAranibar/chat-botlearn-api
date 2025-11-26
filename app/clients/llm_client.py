# app/clients/llm_client.py
import httpx
from typing import Dict, Any

from app.core.config import get_settings

_settings = get_settings()


class LLMClient:
    def __init__(self) -> None:
        self.base_url = _settings.VLLM_BASE_URL
        self.model = _settings.VLLM_MODEL
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=60.0)

    async def chat_completion(self, messages, temperature: float, max_tokens: int) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": [m.model_dump() for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            # sin streaming por ahora
            "stream": False,
        }

        response = await self._client.post("/v1/chat/completions", json=payload)
        response.raise_for_status()
        return response.json()


llm_client = LLMClient()
