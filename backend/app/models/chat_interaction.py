from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    JSON,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ChatInteraction(Base):
    __tablename__ = "chat_interactions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    visitor_key: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        index=True,
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    source_refs: Mapped[list[dict]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
        server_default=text("'[]'::json"),
    )

    confidence_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    grounded: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    model_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    retrieval_method: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )