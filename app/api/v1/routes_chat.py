# app/api/v1/routes_chat.py
from fastapi import APIRouter
from app.api.v1.schemas import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def create_chat_completion(request: ChatRequest) -> ChatResponse:
    """
    Endpoint principal para hablar con el modelo.
    """
    return await chat_service.send_chat(request)
