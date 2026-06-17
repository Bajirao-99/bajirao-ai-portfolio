from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_admin
from app.core.config import settings
from app.db.database import get_db
from app.models.admin_user import AdminUser
from app.schemas.integration import (
    GitHubPortfolioResponse,
    GitHubRepositoryResponse,
    GitHubRepositoryUpdate,
)
from app.services.github_api_service import (
    GitHubAPIError,
    fetch_github_portfolio,
)
from app.services.github_service import (
    get_github_profile,
    get_github_repository_by_id,
    list_public_github_repositories,
    sync_github_portfolio,
    update_github_repository,
)


router = APIRouter(
    prefix="/api/v1/integrations/github",
    tags=["GitHub Integration"],
)


@router.get(
    "",
    response_model=GitHubPortfolioResponse,
)
def read_github_portfolio(
    featured: bool | None = Query(
        default=None,
        description=(
            "Filter repositories by featured status."
        ),
    ),
    database_session: Session = Depends(get_db),
):
    profile = get_github_profile(
        database_session
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "GitHub data has not been "
                "synchronized yet."
            ),
        )

    repositories = (
        list_public_github_repositories(
            database_session=database_session,
            profile_id=profile.id,
            featured=featured,
        )
    )

    return {
        "profile": profile,
        "repositories": repositories,
    }


@router.post(
    "/sync",
    response_model=GitHubPortfolioResponse,
)
async def synchronize_github_portfolio(
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    try:
        profile_data, repositories_data = (
            await fetch_github_portfolio(
                settings.github_username
            )
        )

    except GitHubAPIError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error

    profile = sync_github_portfolio(
        database_session=database_session,
        profile_data=profile_data,
        repositories_data=repositories_data,
    )

    repositories = (
        list_public_github_repositories(
            database_session=database_session,
            profile_id=profile.id,
        )
    )

    return {
        "profile": profile,
        "repositories": repositories,
    }


@router.put(
    "/repositories/{repository_id}",
    response_model=GitHubRepositoryResponse,
)
def update_repository_display_settings(
    repository_id: int,
    repository_data: GitHubRepositoryUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    repository = get_github_repository_by_id(
        database_session=database_session,
        repository_id=repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GitHub repository not found.",
        )

    return update_github_repository(
        database_session=database_session,
        repository=repository,
        update_data=repository_data.model_dump(
            exclude_unset=True
        ),
    )