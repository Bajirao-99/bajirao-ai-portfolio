from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_admin
from app.db.database import get_db
from app.models.admin_user import AdminUser
from app.models.coding_profile import CodingProfile
from app.schemas.integration import (
    CodingProfileCreate,
    CodingProfileResponse,
    CodingProfileUpdate,
)
from app.services.content_service import (
    create_record,
    delete_record,
    get_record_by_id,
    list_visible_records,
    update_record,
)


router = APIRouter(
    prefix="/api/v1/coding-profiles",
    tags=["Coding Profiles"],
)


@router.get(
    "",
    response_model=list[CodingProfileResponse],
)
def list_coding_profiles(
    database_session: Session = Depends(get_db),
):
    return list_visible_records(
        database_session,
        CodingProfile,
    )


@router.get(
    "/platform/{platform}",
    response_model=CodingProfileResponse,
)
def read_coding_profile_by_platform(
    platform: str,
    database_session: Session = Depends(get_db),
):
    statement = select(
        CodingProfile
    ).where(
        CodingProfile.platform
        == platform.strip().lower(),
        CodingProfile.is_visible.is_(True),
    )

    coding_profile = database_session.scalar(
        statement
    )

    if coding_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding profile not found.",
        )

    return coding_profile


@router.post(
    "",
    response_model=CodingProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_coding_profile(
    profile_data: CodingProfileCreate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    create_data = profile_data.model_dump(
        mode="json"
    )

    create_data["platform"] = (
        create_data["platform"]
        .strip()
        .lower()
    )

    try:
        return create_record(
            database_session=database_session,
            model=CodingProfile,
            record_data=create_data,
            entity_name="Coding profile",
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{profile_id}",
    response_model=CodingProfileResponse,
)
def update_coding_profile(
    profile_id: int,
    profile_data: CodingProfileUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    coding_profile = get_record_by_id(
        database_session=database_session,
        model=CodingProfile,
        record_id=profile_id,
    )

    if coding_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding profile not found.",
        )

    update_data = profile_data.model_dump(
        exclude_unset=True,
        mode="json",
    )

    if "platform" in update_data:
        update_data["platform"] = (
            update_data["platform"]
            .strip()
            .lower()
        )

    try:
        return update_record(
            database_session=database_session,
            record=coding_profile,
            record_data=update_data,
            entity_name="Coding profile",
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_coding_profile(
    profile_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    coding_profile = get_record_by_id(
        database_session=database_session,
        model=CodingProfile,
        record_id=profile_id,
    )

    if coding_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding profile not found.",
        )

    delete_record(
        database_session,
        coding_profile,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )