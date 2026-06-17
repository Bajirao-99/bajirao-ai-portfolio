from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_admin
from app.db.database import get_db
from app.models.admin_user import AdminUser
from app.models.experience import Experience
from app.schemas.portfolio_content import (
    ExperienceCreate,
    ExperienceResponse,
    ExperienceUpdate,
)
from app.services.content_service import (
    create_record,
    delete_record,
    get_record_by_id,
    list_visible_records,
    update_record,
)


router = APIRouter(
    prefix="/api/v1/experiences",
    tags=["Work Experience"],
)


@router.get(
    "",
    response_model=list[ExperienceResponse],
)
def list_experiences(
    database_session: Session = Depends(get_db),
):
    return list_visible_records(
        database_session,
        Experience,
    )


@router.get(
    "/{experience_id}",
    response_model=ExperienceResponse,
)
def read_experience(
    experience_id: int,
    database_session: Session = Depends(get_db),
):
    experience = get_record_by_id(
        database_session,
        Experience,
        experience_id,
    )

    if experience is None or not experience.is_visible:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work experience not found.",
        )

    return experience


@router.post(
    "",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_experience(
    experience_data: ExperienceCreate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    try:
        return create_record(
            database_session,
            Experience,
            experience_data.model_dump(),
            "Work experience",
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{experience_id}",
    response_model=ExperienceResponse,
)
def update_experience(
    experience_id: int,
    experience_data: ExperienceUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    experience = get_record_by_id(
        database_session,
        Experience,
        experience_id,
    )

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work experience not found.",
        )

    try:
        return update_record(
            database_session,
            experience,
            experience_data.model_dump(
                exclude_unset=True
            ),
            "Work experience",
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.delete(
    "/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_experience(
    experience_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    experience = get_record_by_id(
        database_session,
        Experience,
        experience_id,
    )

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work experience not found.",
        )

    delete_record(
        database_session,
        experience,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )