from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_admin
from app.db.database import get_db
from app.models.admin_user import AdminUser
from app.schemas.communication import (
    InterviewRequestAdminResponse,
    InterviewRequestCreate,
    InterviewRequestUpdate,
    SubmissionResponse,
)
from app.services.communication_service import (
    create_interview_request,
    delete_interview_request,
    get_interview_request_by_id,
    list_interview_requests,
    update_interview_request,
)


public_router = APIRouter(
    prefix="/api/v1/interview-requests",
    tags=["Interview Requests"],
)


admin_router = APIRouter(
    prefix="/api/v1/admin/interview-requests",
    tags=["Admin Interview Requests"],
)


@public_router.post(
    "",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_interview_request(
    request_data: InterviewRequestCreate,
    database_session: Session = Depends(get_db),
):
    interview_request = create_interview_request(
        database_session=database_session,
        request_data=request_data.model_dump(),
    )

    return {
        "id": interview_request.id,
        "status": interview_request.status,
        "message": (
            "Your interview request has been "
            "submitted successfully."
        ),
        "created_at": interview_request.created_at,
    }


@admin_router.get(
    "",
    response_model=list[
        InterviewRequestAdminResponse
    ],
)
def read_interview_requests(
    request_status: str | None = Query(
        default=None,
        alias="status",
    ),
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
    return list_interview_requests(
        database_session=database_session,
        status_filter=request_status,
        limit=limit,
        offset=offset,
    )


@admin_router.get(
    "/{request_id}",
    response_model=InterviewRequestAdminResponse,
)
def read_interview_request(
    request_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    interview_request = (
        get_interview_request_by_id(
            database_session=database_session,
            request_id=request_id,
        )
    )

    if interview_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview request not found.",
        )

    return interview_request


@admin_router.put(
    "/{request_id}",
    response_model=InterviewRequestAdminResponse,
)
def modify_interview_request(
    request_id: int,
    update_data: InterviewRequestUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    interview_request = (
        get_interview_request_by_id(
            database_session=database_session,
            request_id=request_id,
        )
    )

    if interview_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview request not found.",
        )

    return update_interview_request(
        database_session=database_session,
        interview_request=interview_request,
        update_data=update_data.model_dump(
            exclude_unset=True
        ),
    )


@admin_router.delete(
    "/{request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_interview_request(
    request_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    interview_request = (
        get_interview_request_by_id(
            database_session=database_session,
            request_id=request_id,
        )
    )

    if interview_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview request not found.",
        )

    delete_interview_request(
        database_session=database_session,
        interview_request=interview_request,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )