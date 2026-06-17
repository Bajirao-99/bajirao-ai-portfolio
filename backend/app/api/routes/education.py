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
from app.models.education import Education
from app.schemas.portfolio_content import (
    EducationCreate,
    EducationResponse,
    EducationUpdate,
)
from app.services.content_service import (
    create_record,
    delete_record,
    get_record_by_id,
    list_visible_records,
    update_record,
)


router = APIRouter(
    prefix="/api/v1/education",
    tags=["Education"],
)


@router.get(
    "",
    response_model=list[EducationResponse],
)
def list_education(
    database_session: Session = Depends(get_db),
):
    return list_visible_records(
        database_session,
        Education,
    )


@router.get(
    "/{education_id}",
    response_model=EducationResponse,
)
def read_education(
    education_id: int,
    database_session: Session = Depends(get_db),
):
    education = get_record_by_id(
        database_session,
        Education,
        education_id,
    )

    if education is None or not education.is_visible:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found.",
        )

    return education


@router.post(
    "",
    response_model=EducationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_education(
    education_data: EducationCreate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    try:
        return create_record(
            database_session,
            Education,
            education_data.model_dump(),
            "Education record",
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{education_id}",
    response_model=EducationResponse,
)
def update_education(
    education_id: int,
    education_data: EducationUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    education = get_record_by_id(
        database_session,
        Education,
        education_id,
    )

    if education is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found.",
        )

    try:
        return update_record(
            database_session,
            education,
            education_data.model_dump(
                exclude_unset=True
            ),
            "Education record",
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.delete(
    "/{education_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_education(
    education_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    education = get_record_by_id(
        database_session,
        Education,
        education_id,
    )

    if education is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found.",
        )

    delete_record(
        database_session,
        education,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )