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
from app.models.certification import Certification
from app.schemas.portfolio_content import (
    CertificationCreate,
    CertificationResponse,
    CertificationUpdate,
)
from app.services.content_service import (
    create_record,
    delete_record,
    get_record_by_id,
    list_visible_records,
    update_record,
)


router = APIRouter(
    prefix="/api/v1/certifications",
    tags=["Certifications"],
)


@router.get(
    "",
    response_model=list[CertificationResponse],
)
def list_certifications(
    database_session: Session = Depends(get_db),
):
    return list_visible_records(
        database_session,
        Certification,
    )


@router.get(
    "/{certification_id}",
    response_model=CertificationResponse,
)
def read_certification(
    certification_id: int,
    database_session: Session = Depends(get_db),
):
    certification = get_record_by_id(
        database_session,
        Certification,
        certification_id,
    )

    if certification is None or not certification.is_visible:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found.",
        )

    return certification


@router.post(
    "",
    response_model=CertificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_certification(
    certification_data: CertificationCreate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    try:
        return create_record(
            database_session,
            Certification,
            certification_data.model_dump(),
            "Certification",
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{certification_id}",
    response_model=CertificationResponse,
)
def update_certification(
    certification_id: int,
    certification_data: CertificationUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    certification = get_record_by_id(
        database_session,
        Certification,
        certification_id,
    )

    if certification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found.",
        )

    try:
        return update_record(
            database_session,
            certification,
            certification_data.model_dump(
                exclude_unset=True
            ),
            "Certification",
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.delete(
    "/{certification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_certification(
    certification_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    certification = get_record_by_id(
        database_session,
        Certification,
        certification_id,
    )

    if certification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found.",
        )

    delete_record(
        database_session,
        certification,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )