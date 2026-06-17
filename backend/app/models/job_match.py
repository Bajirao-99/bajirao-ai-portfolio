from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    JSON,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class JobMatchAnalysis(Base):
    __tablename__ = "job_match_analyses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    job_title: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )

    company_name: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )

    job_description_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )

    overall_match_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    match_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    score_breakdown: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    matched_skills: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    missing_skills: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    recommended_resume_type: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    embedding_method: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )