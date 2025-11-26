# app/services/chat_service.py
from app.clients.llm_client import llm_client
from app.api.v1.schemas import ChatRequest, ChatResponse, ChatResponseMessage, ChatResponseChoice


class ChatService:
    async def send_chat(self, request: ChatRequest) -> ChatResponse:
        raw = await llm_client.chat_completion(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        # Mapeamos el JSON del modelo a nuestros schemas
        choices = []
        for c in raw.get("choices", []):
            msg = c.get("message", {})
            choices.append(
                ChatResponseChoice(
                    index=c.get("index", 0),
                    message=ChatResponseMessage(
                        role=msg.get("role", "assistant"),
                        content=msg.get("content", ""),
                    ),
                )
            )

        return ChatResponse(
            id=raw.get("id", ""),
            model=raw.get("model", ""),
            choices=choices,
        )


chat_service = ChatService()
