from typing import Literal

from pydantic import BaseModel


class AIStatusResponse(BaseModel):
    configured: bool
    model: str


class AIChatTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class AIChatRequest(BaseModel):
    question: str
    history: list[AIChatTurn] = []


class AISourceResponse(BaseModel):
    id: str
    title: str
    url: str
    source: str


class AIChatResponse(BaseModel):
    answer: str
    sources: list[AISourceResponse]
    model: str
