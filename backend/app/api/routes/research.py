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
from app.schemas.showcase import (
    ResearchCreate,
    ResearchResponse,
    ResearchUpdate,
)
from app.services.showcase_service import (
    create_research,
    delete_research,
    get_public_research_by_slug,
    get_research_by_id,
    list_public_research,
    update_research,
)


router = APIRouter(
    prefix="/api/v1/research",
    tags=["Research and Publications"],
)


@router.get(
    "",
    response_model=list[ResearchResponse],
)
def list_research_records(
    featured: bool | None = Query(
        default=None,
        description=(
            "Filter research records by featured status."
        ),
    ),
    database_session: Session = Depends(get_db),
):
    return list_public_research(
        database_session=database_session,
        featured=featured,
    )


@router.get(
    "/slug/{slug}",
    response_model=ResearchResponse,
)
def read_research_by_slug(
    slug: str,
    database_session: Session = Depends(get_db),
):
    research = get_public_research_by_slug(
        database_session=database_session,
        slug=slug,
    )

    if research is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research record not found.",
        )

    return research


@router.post(
    "",
    response_model=ResearchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_research_record(
    research_data: ResearchCreate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    try:
        return create_research(
            database_session=database_session,
            research_data=research_data.model_dump(
                mode="json",
            ),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{research_id}",
    response_model=ResearchResponse,
)
def update_research_record(
    research_id: int,
    research_data: ResearchUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    research = get_research_by_id(
        database_session=database_session,
        research_id=research_id,
    )

    if research is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research record not found.",
        )

    try:
        return update_research(
            database_session=database_session,
            research=research,
            research_data=research_data.model_dump(
                exclude_unset=True,
                mode="json",
            ),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.delete(
    "/{research_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_research_record(
    research_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    research = get_research_by_id(
        database_session=database_session,
        research_id=research_id,
    )

    if research is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Research record not found.",
        )

    delete_research(
        database_session=database_session,
        research=research,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )