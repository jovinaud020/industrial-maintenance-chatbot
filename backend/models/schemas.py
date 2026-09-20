from typing import List

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10
    )

    history: List[ChatMessage] = Field(
        default_factory=list
    )


class RegisterRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    email: str = Field(
        ...,
        min_length=5,
        max_length=100
    )

    password: str = Field(
        ...,
        min_length=6,
        max_length=72
    )


class LoginRequest(BaseModel):
    username: str
    password: str