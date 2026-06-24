from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ChatHistoryMessage(BaseModel):
    role: Literal["user", "assistant"]

    content: str = Field(
        min_length=1,
        max_length=1500,
    )


class PortfolioChatRequest(BaseModel):
    visitor_key: UUID

    question: str = Field(
        min_length=3,
        max_length=1500,
    )

    history: list[ChatHistoryMessage] = Field(
        default_factory=list,
        max_length=6,
    )

    top_k: int | None = Field(
        default=None,
        ge=1,
        le=10,
    )


class ChatSource(BaseModel):
    source_type: str
    source_id: int | None
    title: str
    url: str | None
    relevance_score: float


class PortfolioChatResponse(BaseModel):
    interaction_id: int
    answer: str
    grounded: bool
    confidence_score: float
    sources: list[ChatSource]
    model_name: str
    retrieval_method: str

    answer_mode: Literal[
        "portfolio",
        "general",
        "mixed",
    ] = "portfolio"
    
    disclaimer: str = (
        "This answer is generated only from the "
        "portfolio information currently available."
    )


class ChatInteractionHistoryResponse(BaseModel):
    id: int
    visitor_key: str
    question: str
    answer: str
    source_refs: list[ChatSource]
    confidence_score: float
    grounded: bool
    model_name: str
    retrieval_method: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )