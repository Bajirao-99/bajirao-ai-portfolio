from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import (
    get_current_admin,
)
from app.db.database import get_db
from app.models.admin_user import AdminUser
from app.schemas.job_match import (
    JobMatchHistoryResponse,
    JobMatchRequest,
    JobMatchResponse,
)
from app.services.job_match_service import (
    analyze_job_match,
    delete_job_match_analysis,
    get_job_match_analysis_by_id,
    list_job_match_analyses,
)


public_router = APIRouter(
    prefix="/api/v1/ai/job-match",
    tags=["AI Job Description Matcher"],
)


admin_router = APIRouter(
    prefix="/api/v1/admin/job-match-analyses",
    tags=["Admin AI Analyses"],
)


@public_router.post(
    "",
    response_model=JobMatchResponse,
    status_code=status.HTTP_201_CREATED,
)
def match_job_description(
    request_data: JobMatchRequest,
    database_session: Session = Depends(get_db),
):
    try:
        return analyze_job_match(
            database_session=database_session,
            job_description=(
                request_data.job_description
            ),
            job_title=request_data.job_title,
            company_name=(
                request_data.company_name
            ),
            top_k=request_data.top_k,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@admin_router.get(
    "",
    response_model=list[
        JobMatchHistoryResponse
    ],
)
def read_job_match_history(
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return list_job_match_analyses(
        database_session=database_session,
        limit=limit,
        offset=offset,
    )


@admin_router.delete(
    "/{analysis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_job_match_analysis(
    analysis_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    analysis = get_job_match_analysis_by_id(
        database_session=database_session,
        analysis_id=analysis_id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job match analysis not found.",
        )

    delete_job_match_analysis(
        database_session=database_session,
        analysis=analysis,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )