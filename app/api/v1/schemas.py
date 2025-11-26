# app/api/v1/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Literal


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: float = 0.3
    max_tokens: int = 1024


class ChatResponseMessage(BaseModel):
    role: str
    content: str


class ChatResponseChoice(BaseModel):
    index: int
    message: ChatResponseMessage


class ChatResponse(BaseModel):
    id: str
    model: str
    choices: List[ChatResponseChoice]
