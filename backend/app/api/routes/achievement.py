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
from app.models.achievement import Achievement
from app.models.admin_user import AdminUser
from app.schemas.portfolio_content import (
    AchievementCreate,
    AchievementResponse,
    AchievementUpdate,
)
from app.services.content_service import (
    create_record,
    delete_record,
    get_record_by_id,
    list_visible_records,
    update_record,
)


router = APIRouter(
    prefix="/api/v1/achievements",
    tags=["Achievements"],
)


@router.get(
    "",
    response_model=list[AchievementResponse],
)
def list_achievements(
    database_session: Session = Depends(get_db),
):
    return list_visible_records(
        database_session,
        Achievement,
    )


@router.get(
    "/{achievement_id}",
    response_model=AchievementResponse,
)
def read_achievement(
    achievement_id: int,
    database_session: Session = Depends(get_db),
):
    achievement = get_record_by_id(
        database_session,
        Achievement,
        achievement_id,
    )

    if achievement is None or not achievement.is_visible:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found.",
        )

    return achievement


@router.post(
    "",
    response_model=AchievementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_achievement(
    achievement_data: AchievementCreate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    try:
        return create_record(
            database_session,
            Achievement,
            achievement_data.model_dump(),
            "Achievement",
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{achievement_id}",
    response_model=AchievementResponse,
)
def update_achievement(
    achievement_id: int,
    achievement_data: AchievementUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    achievement = get_record_by_id(
        database_session,
        Achievement,
        achievement_id,
    )

    if achievement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found.",
        )

    try:
        return update_record(
            database_session,
            achievement,
            achievement_data.model_dump(
                exclude_unset=True
            ),
            "Achievement",
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.delete(
    "/{achievement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_achievement(
    achievement_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    achievement = get_record_by_id(
        database_session,
        Achievement,
        achievement_id,
    )

    if achievement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievement not found.",
        )

    delete_record(
        database_session,
        achievement,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )