# app/clients/llm_client.py
import httpx
import aiohttp
import json
from typing import Dict, Any, AsyncGenerator

from app.core.config import get_settings

_settings = get_settings()


class LLMClient:
    def __init__(self) -> None:
        self.base_url = _settings.VLLM_BASE_URL
        self.model = _settings.VLLM_MODEL
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=60.0)

    # Método original
    async def chat_completion(self, messages, temperature: float, max_tokens: int) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": [m.model_dump() for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }

        response = await self._client.post("/v1/chat/completions", json=payload)
        response.raise_for_status()
        return response.json()


    # Nuevo método STREAMING
    async def chat_completion_stream(
        self,
        messages,
        temperature: float,
        max_tokens: int
    ) -> AsyncGenerator[str, None]:

        payload = {
            "model": self.model,
            "messages": [m.model_dump() for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload
            ) as resp:

                if resp.status != 200:
                    raise Exception(await resp.text())
                
                async for raw in resp.content:
                    line = raw.decode("utf-8")

                    if not line.startswith("data:"):
                        continue

                    data = line.replace("data:", "", 1)

                    if data.strip() == "[DONE]":
                        return

                    try:
                        data_json = json.loads(data)
                        delta = (
                            data_json
                            .get("choices", [{}])[0]
                            .get("delta", {})
                            .get("content", "")
                        )
                        if delta:
                            yield delta
                    except Exception:
                        continue


llm_client = LLMClient()
