from collections import Counter
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.github import (
    GitHubProfile,
    GitHubRepository,
)


def parse_github_datetime(
    value: str | None,
) -> datetime | None:
    if not value:
        return None

    return datetime.fromisoformat(
        value.replace(
            "Z",
            "+00:00",
        )
    )


def get_github_profile(
    database_session: Session,
) -> GitHubProfile | None:
    statement = (
        select(GitHubProfile)
        .order_by(GitHubProfile.id.asc())
    )

    return database_session.scalar(
        statement
    )


def list_public_github_repositories(
    database_session: Session,
    profile_id: int,
    featured: bool | None = None,
) -> list[GitHubRepository]:
    statement = (
        select(GitHubRepository)
        .where(
            GitHubRepository.github_profile_id
            == profile_id,
            GitHubRepository.is_visible.is_(True),
        )
        .order_by(
            GitHubRepository.is_featured.desc(),
            GitHubRepository.display_order.asc(),
            GitHubRepository.stars_count.desc(),
            GitHubRepository.github_pushed_at.desc(),
        )
    )

    if featured is not None:
        statement = statement.where(
            GitHubRepository.is_featured.is_(
                featured
            )
        )

    return list(
        database_session.scalars(
            statement
        ).all()
    )


def get_github_repository_by_id(
    database_session: Session,
    repository_id: int,
) -> GitHubRepository | None:
    return database_session.get(
        GitHubRepository,
        repository_id,
    )


def update_github_repository(
    database_session: Session,
    repository: GitHubRepository,
    update_data: dict[str, Any],
) -> GitHubRepository:
    for field_name, field_value in (
        update_data.items()
    ):
        setattr(
            repository,
            field_name,
            field_value,
        )

    database_session.commit()
    database_session.refresh(repository)

    return repository


def sync_github_portfolio(
    database_session: Session,
    profile_data: dict[str, Any],
    repositories_data: list[dict[str, Any]],
) -> GitHubProfile:
    current_time = datetime.now(
        timezone.utc
    )

    github_user_id = int(
        profile_data["id"]
    )

    statement = select(
        GitHubProfile
    ).where(
        GitHubProfile.github_user_id
        == github_user_id
    )

    profile = database_session.scalar(
        statement
    )

    if profile is None:
        profile = GitHubProfile(
            github_user_id=github_user_id,
            username=profile_data["login"],
            avatar_url=profile_data["avatar_url"],
            profile_url=profile_data["html_url"],
        )

        database_session.add(profile)
        database_session.flush()

    language_counter = Counter(
        repository_data.get("language")
        for repository_data in repositories_data
        if repository_data.get("language")
    )

    profile.username = profile_data["login"]
    profile.name = profile_data.get("name")
    profile.bio = profile_data.get("bio")
    profile.avatar_url = profile_data["avatar_url"]
    profile.profile_url = profile_data["html_url"]
    profile.company = profile_data.get("company")
    profile.location = profile_data.get("location")
    profile.blog_url = (
        profile_data.get("blog") or None
    )
    profile.followers = profile_data.get(
        "followers",
        0,
    )
    profile.following = profile_data.get(
        "following",
        0,
    )
    profile.public_repos = profile_data.get(
        "public_repos",
        0,
    )
    profile.total_stars = sum(
        repository.get(
            "stargazers_count",
            0,
        )
        for repository in repositories_data
    )
    profile.total_forks = sum(
        repository.get(
            "forks_count",
            0,
        )
        for repository in repositories_data
    )
    profile.top_languages = [
        {
            "language": language,
            "repositories": count,
        }
        for language, count
        in language_counter.most_common(10)
    ]
    profile.github_created_at = (
        parse_github_datetime(
            profile_data.get("created_at")
        )
    )
    profile.github_updated_at = (
        parse_github_datetime(
            profile_data.get("updated_at")
        )
    )
    profile.last_synced_at = current_time

    database_session.flush()

    existing_statement = select(
        GitHubRepository
    ).where(
        GitHubRepository.github_profile_id
        == profile.id
    )

    existing_repositories = list(
        database_session.scalars(
            existing_statement
        ).all()
    )

    existing_by_github_id = {
        repository.github_repo_id: repository
        for repository in existing_repositories
    }

    synchronized_repository_ids: set[int] = set()

    for repository_data in repositories_data:
        github_repository_id = int(
            repository_data["id"]
        )

        synchronized_repository_ids.add(
            github_repository_id
        )

        repository = existing_by_github_id.get(
            github_repository_id
        )

        is_new_repository = repository is None

        if repository is None:
            repository = GitHubRepository(
                github_profile_id=profile.id,
                github_repo_id=github_repository_id,
                name=repository_data["name"],
                full_name=repository_data["full_name"],
                repository_url=(
                    repository_data["html_url"]
                ),
            )

            database_session.add(repository)

        repository.name = repository_data["name"]
        repository.full_name = (
            repository_data["full_name"]
        )
        repository.description = (
            repository_data.get("description")
        )
        repository.repository_url = (
            repository_data["html_url"]
        )
        repository.homepage_url = (
            repository_data.get("homepage")
            or None
        )
        repository.language = (
            repository_data.get("language")
        )
        repository.topics = (
            repository_data.get("topics")
            or []
        )
        repository.stars_count = (
            repository_data.get(
                "stargazers_count",
                0,
            )
        )
        repository.forks_count = (
            repository_data.get(
                "forks_count",
                0,
            )
        )
        repository.open_issues_count = (
            repository_data.get(
                "open_issues_count",
                0,
            )
        )
        repository.is_fork = (
            repository_data.get(
                "fork",
                False,
            )
        )
        repository.is_archived = (
            repository_data.get(
                "archived",
                False,
            )
        )

        if is_new_repository:
            repository.is_visible = not (
                repository.is_archived
            )

        repository.github_created_at = (
            parse_github_datetime(
                repository_data.get(
                    "created_at"
                )
            )
        )
        repository.github_updated_at = (
            parse_github_datetime(
                repository_data.get(
                    "updated_at"
                )
            )
        )
        repository.github_pushed_at = (
            parse_github_datetime(
                repository_data.get(
                    "pushed_at"
                )
            )
        )
        repository.last_synced_at = (
            current_time
        )

    for existing_repository in (
        existing_repositories
    ):
        if (
            existing_repository.github_repo_id
            not in synchronized_repository_ids
        ):
            database_session.delete(
                existing_repository
            )

    database_session.commit()
    database_session.refresh(profile)

    return profile