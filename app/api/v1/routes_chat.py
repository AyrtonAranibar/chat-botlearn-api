from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.clients.llm_client import llm_client
from app.api.v1.schemas import ChatRequest


router = APIRouter()


# original
@router.post("/chat/completions")
async def chat_completion(request: ChatRequest):
    return await llm_client.chat_completion(
        messages=request.messages,
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )

#  STREAMING
@router.post("/chat/completions/stream")
async def chat_stream(request: ChatRequest):

    async def event_stream():
        async for chunk in llm_client.chat_completion_stream(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        ):
            yield f"data: {chunk}*\n\n*"
        yield "data: [DONE]*\n\n*"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
