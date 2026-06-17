from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    JSON,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class CodingProfile(Base):
    __tablename__ = "coding_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    platform: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        unique=True,
        index=True,
    )

    username: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    profile_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    total_solved: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    rating: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    max_rating: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    ranking: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    achievement_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    statistics: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
        server_default=text("'{}'::json"),
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