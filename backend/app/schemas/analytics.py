from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PageViewCreate(BaseModel):
    visitor_key: UUID

    page_path: str = Field(
        min_length=1,
        max_length=300,
        pattern=r"^/",
    )

    referrer: str | None = Field(
        default=None,
        max_length=500,
    )


class PageViewResponse(BaseModel):
    recorded: bool
    visitor_key: UUID
    page_path: str
    viewed_at: datetime


class ProjectViewResponse(BaseModel):
    project_id: int
    slug: str
    view_count: int


class AnalyticsSummary(BaseModel):
    total_unique_visitors: int
    total_page_views: int
    period_page_views: int
    total_project_views: int
    total_resume_downloads: int
    total_contact_messages: int
    new_contact_messages: int
    total_interview_requests: int
    pending_interview_requests: int
    total_job_match_analyses: int
    total_chat_interactions: int


class TopPageStat(BaseModel):
    page_path: str
    views: int


class TopProjectStat(BaseModel):
    id: int
    title: str
    slug: str
    view_count: int


class ResumeDownloadStat(BaseModel):
    id: int
    title: str
    resume_type: str
    download_count: int


class DailyPageViewStat(BaseModel):
    view_date: date
    views: int


class AnalyticsDashboardResponse(BaseModel):
    period_days: int
    summary: AnalyticsSummary
    top_pages: list[TopPageStat]
    top_projects: list[TopProjectStat]
    resume_downloads: list[ResumeDownloadStat]
    daily_page_views: list[DailyPageViewStat]