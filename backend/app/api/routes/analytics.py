from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_admin
from app.db.database import get_db
from app.models.admin_user import AdminUser
from app.schemas.analytics import (
    AnalyticsDashboardResponse,
    PageViewCreate,
    PageViewResponse,
    ProjectViewResponse,
)
from app.services.analytics_service import (
    get_dashboard_analytics,
    increment_project_view,
    record_page_view,
)


public_router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Portfolio Analytics"],
)


admin_router = APIRouter(
    prefix="/api/v1/admin/analytics",
    tags=["Admin Analytics"],
)


@public_router.post(
    "/page-view",
    response_model=PageViewResponse,
    status_code=status.HTTP_201_CREATED,
)
def track_page_view(
    page_view_data: PageViewCreate,
    database_session: Session = Depends(get_db),
):
    page_view = record_page_view(
        database_session=database_session,
        visitor_key=str(
            page_view_data.visitor_key
        ),
        page_path=page_view_data.page_path,
        referrer=page_view_data.referrer,
    )

    return {
        "recorded": True,
        "visitor_key": (
            page_view_data.visitor_key
        ),
        "page_path": page_view.page_path,
        "viewed_at": page_view.viewed_at,
    }


@public_router.post(
    "/projects/{slug}/view",
    response_model=ProjectViewResponse,
)
def track_project_view(
    slug: str,
    database_session: Session = Depends(get_db),
):
    project = increment_project_view(
        database_session=database_session,
        slug=slug,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return {
        "project_id": project.id,
        "slug": project.slug,
        "view_count": project.view_count,
    }


@admin_router.get(
    "",
    response_model=AnalyticsDashboardResponse,
)
def read_analytics_dashboard(
    days: int = Query(
        default=30,
        ge=1,
        le=365,
    ),
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return get_dashboard_analytics(
        database_session=database_session,
        days=days,
    )