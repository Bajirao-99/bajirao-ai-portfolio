from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class SiteVisitor(Base):
    __tablename__ = "site_visitors"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    visitor_key: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        unique=True,
        index=True,
    )

    total_page_views: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )

    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )


class PageView(Base):
    __tablename__ = "page_views"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    visitor_id: Mapped[int] = mapped_column(
        ForeignKey(
            "site_visitors.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    page_path: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        index=True,
    )

    referrer: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    viewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )