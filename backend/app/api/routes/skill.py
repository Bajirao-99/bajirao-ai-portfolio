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
from app.models.skill import Skill
from app.schemas.portfolio_content import (
    SkillCreate,
    SkillResponse,
    SkillUpdate,
)
from app.services.content_service import (
    create_record,
    delete_record,
    get_record_by_id,
    list_visible_records,
    update_record,
)


router = APIRouter(
    prefix="/api/v1/skills",
    tags=["Technical Skills"],
)


@router.get(
    "",
    response_model=list[SkillResponse],
)
def list_skills(
    database_session: Session = Depends(get_db),
):
    return list_visible_records(
        database_session,
        Skill,
    )


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
)
def read_skill(
    skill_id: int,
    database_session: Session = Depends(get_db),
):
    skill = get_record_by_id(
        database_session,
        Skill,
        skill_id,
    )

    if skill is None or not skill.is_visible:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found.",
        )

    return skill


@router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_skill(
    skill_data: SkillCreate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    try:
        return create_record(
            database_session,
            Skill,
            skill_data.model_dump(),
            "Skill",
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{skill_id}",
    response_model=SkillResponse,
)
def update_skill(
    skill_id: int,
    skill_data: SkillUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    skill = get_record_by_id(
        database_session,
        Skill,
        skill_id,
    )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found.",
        )

    try:
        return update_record(
            database_session,
            skill,
            skill_data.model_dump(
                exclude_unset=True
            ),
            "Skill",
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_skill(
    skill_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    skill = get_record_by_id(
        database_session,
        Skill,
        skill_id,
    )

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found.",
        )

    delete_record(
        database_session,
        skill,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )