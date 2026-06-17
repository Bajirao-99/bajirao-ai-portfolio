from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_admin
from app.db.database import get_db
from app.models.admin_user import AdminUser
from app.schemas.profile import (
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)
from app.services.profile_service import (
    create_profile as create_profile_record,
)
from app.services.profile_service import (
    get_active_profile,
    get_profile_by_id,
)
from app.services.profile_service import (
    update_profile as update_profile_record,
)


router = APIRouter(
    prefix="/api/v1/profile",
    tags=["Professional Profile"],
)


@router.get(
    "",
    response_model=ProfileResponse,
    responses={
        404: {
            "description": "Professional profile not found."
        }
    },
)
def read_public_profile(
    database_session: Session = Depends(get_db),
):
    profile = get_active_profile(database_session)

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professional profile not found.",
        )

    return profile


@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {
            "description": "Authentication required."
        },
        409: {
            "description": (
                "An active professional profile "
                "already exists."
            )
        },
    },
)
def create_public_profile(
    profile_data: ProfileCreate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    try:
        return create_profile_record(
            database_session=database_session,
            profile_data=profile_data.model_dump(
                mode="json",
            ),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{profile_id}",
    response_model=ProfileResponse,
    responses={
        401: {
            "description": "Authentication required."
        },
        404: {
            "description": "Professional profile not found."
        },
        409: {
            "description": "Updated data conflicts with existing data."
        },
    },
)
def update_public_profile(
    profile_id: int,
    profile_data: ProfileUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    profile = get_profile_by_id(
        database_session=database_session,
        profile_id=profile_id,
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professional profile not found.",
        )

    update_data = profile_data.model_dump(
        exclude_unset=True,
        mode="json",
    )

    try:
        return update_profile_record(
            database_session=database_session,
            profile=profile,
            profile_data=update_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error