from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.analytics import (
    PageView,
    SiteVisitor,
)
from app.models.contact_message import ContactMessage
from app.models.interview_request import InterviewRequest
from app.models.project import Project
from app.models.resume import Resume
from app.models.job_match import JobMatchAnalysis
from app.models.chat_interaction import ChatInteraction

def record_page_view(
    database_session: Session,
    visitor_key: str,
    page_path: str,
    referrer: str | None,
) -> PageView:
    current_time = datetime.now(
        timezone.utc
    )

    statement = select(
        SiteVisitor
    ).where(
        SiteVisitor.visitor_key
        == visitor_key
    )

    visitor = database_session.scalar(
        statement
    )

    if visitor is None:
        visitor = SiteVisitor(
            visitor_key=visitor_key,
            total_page_views=1,
            first_seen_at=current_time,
            last_seen_at=current_time,
        )

        database_session.add(visitor)
        database_session.flush()

    else:
        visitor.total_page_views += 1
        visitor.last_seen_at = current_time

    page_view = PageView(
        visitor_id=visitor.id,
        page_path=page_path,
        referrer=referrer,
        viewed_at=current_time,
    )

    database_session.add(page_view)
    database_session.commit()
    database_session.refresh(page_view)

    return page_view


def increment_project_view(
    database_session: Session,
    slug: str,
) -> Project | None:
    statement = select(Project).where(
        Project.slug == slug,
        Project.is_visible.is_(True),
    )

    project = database_session.scalar(
        statement
    )

    if project is None:
        return None

    project.view_count += 1

    database_session.commit()
    database_session.refresh(project)

    return project


def count_records(
    database_session: Session,
    model: type,
) -> int:
    result = database_session.scalar(
        select(func.count())
        .select_from(model)
    )

    return int(result or 0)


def get_dashboard_analytics(
    database_session: Session,
    days: int,
) -> dict[str, Any]:
    current_time = datetime.now(
        timezone.utc
    )

    period_start = current_time - timedelta(
        days=days
    )

    total_unique_visitors = count_records(
        database_session,
        SiteVisitor,
    )

    total_page_views = count_records(
        database_session,
        PageView,
    )

    period_page_views = database_session.scalar(
        select(func.count())
        .select_from(PageView)
        .where(
            PageView.viewed_at >= period_start
        )
    )

    total_project_views = database_session.scalar(
        select(
            func.coalesce(
                func.sum(Project.view_count),
                0,
            )
        )
    )

    total_resume_downloads = database_session.scalar(
        select(
            func.coalesce(
                func.sum(Resume.download_count),
                0,
            )
        )
    )

    total_contact_messages = count_records(
        database_session,
        ContactMessage,
    )

    new_contact_messages = database_session.scalar(
        select(func.count())
        .select_from(ContactMessage)
        .where(
            ContactMessage.status == "new"
        )
    )

    total_interview_requests = count_records(
        database_session,
        InterviewRequest,
    )

    pending_interview_requests = (
        database_session.scalar(
            select(func.count())
            .select_from(InterviewRequest)
            .where(
                InterviewRequest.status
                == "pending"
            )
        )
    )

    total_job_match_analyses = count_records(
        database_session,
        JobMatchAnalysis,
    )

    total_chat_interactions = count_records(
        database_session,
        ChatInteraction,
    )

    top_pages_statement = (
        select(
            PageView.page_path,
            func.count(PageView.id).label(
                "views"
            ),
        )
        .where(
            PageView.viewed_at >= period_start
        )
        .group_by(PageView.page_path)
        .order_by(
            func.count(PageView.id).desc()
        )
        .limit(10)
    )

    top_pages = [
        {
            "page_path": row.page_path,
            "views": int(row.views),
        }
        for row
        in database_session.execute(
            top_pages_statement
        ).all()
    ]

    top_projects_statement = (
        select(
            Project.id,
            Project.title,
            Project.slug,
            Project.view_count,
        )
        .where(
            Project.is_visible.is_(True)
        )
        .order_by(
            Project.view_count.desc(),
            Project.id.asc(),
        )
        .limit(10)
    )

    top_projects = [
        {
            "id": row.id,
            "title": row.title,
            "slug": row.slug,
            "view_count": row.view_count,
        }
        for row
        in database_session.execute(
            top_projects_statement
        ).all()
    ]

    resume_downloads_statement = (
        select(
            Resume.id,
            Resume.title,
            Resume.resume_type,
            Resume.download_count,
        )
        .order_by(
            Resume.download_count.desc(),
            Resume.id.asc(),
        )
    )

    resume_downloads = [
        {
            "id": row.id,
            "title": row.title,
            "resume_type": row.resume_type,
            "download_count": (
                row.download_count
            ),
        }
        for row
        in database_session.execute(
            resume_downloads_statement
        ).all()
    ]

    daily_page_views_statement = (
        select(
            func.date(
                PageView.viewed_at
            ).label("view_date"),
            func.count(
                PageView.id
            ).label("views"),
        )
        .where(
            PageView.viewed_at >= period_start
        )
        .group_by(
            func.date(PageView.viewed_at)
        )
        .order_by(
            func.date(PageView.viewed_at)
        )
    )

    daily_page_views = [
        {
            "view_date": row.view_date,
            "views": int(row.views),
        }
        for row
        in database_session.execute(
            daily_page_views_statement
        ).all()
    ]

    return {
        "period_days": days,
        "summary": {
            "total_unique_visitors": (
                total_unique_visitors
            ),
            "total_page_views": (
                total_page_views
            ),
            "period_page_views": int(
                period_page_views or 0
            ),
            "total_project_views": int(
                total_project_views or 0
            ),
            "total_resume_downloads": int(
                total_resume_downloads or 0
            ),
            "total_contact_messages": (
                total_contact_messages
            ),
            "new_contact_messages": int(
                new_contact_messages or 0
            ),
            "total_interview_requests": (
                total_interview_requests
            ),
            "pending_interview_requests": int(
                pending_interview_requests or 0
            ),
            "total_job_match_analyses": (
                total_job_match_analyses
            ),
            "total_chat_interactions": (
                total_chat_interactions
            ),
        },
        "top_pages": top_pages,
        "top_projects": top_projects,
        "resume_downloads": resume_downloads,
        "daily_page_views": daily_page_views,
    }