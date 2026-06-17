from datetime import date, datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Integer,
    JSON,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ResearchPublication(Base):
    __tablename__ = "research_publications"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
        unique=True,
        index=True,
    )

    research_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    short_summary: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    abstract: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    dataset_details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    methodology: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    models_used: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
        server_default=text("'[]'::json"),
    )

    metrics: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
        server_default=text("'{}'::json"),
    )

    publication_status: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    publication_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    venue: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )

    paper_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    thesis_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    code_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )

    is_visible: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )