from datetime import datetime
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
)


class TopLanguageResponse(BaseModel):
    language: str
    repositories: int


class GitHubProfileResponse(BaseModel):
    id: int
    github_user_id: int
    username: str
    name: str | None
    bio: str | None
    avatar_url: str
    profile_url: str
    company: str | None
    location: str | None
    blog_url: str | None
    followers: int
    following: int
    public_repos: int
    total_stars: int
    total_forks: int
    top_languages: list[TopLanguageResponse]
    github_created_at: datetime | None
    github_updated_at: datetime | None
    last_synced_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class GitHubRepositoryResponse(BaseModel):
    id: int
    github_repo_id: int
    name: str
    full_name: str
    description: str | None
    repository_url: str
    homepage_url: str | None
    language: str | None
    topics: list[str]
    stars_count: int
    forks_count: int
    open_issues_count: int
    is_fork: bool
    is_archived: bool
    is_featured: bool
    is_visible: bool
    display_order: int
    github_created_at: datetime | None
    github_updated_at: datetime | None
    github_pushed_at: datetime | None
    last_synced_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class GitHubRepositoryUpdate(BaseModel):
    is_featured: bool | None = None
    is_visible: bool | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )


class GitHubPortfolioResponse(BaseModel):
    profile: GitHubProfileResponse
    repositories: list[GitHubRepositoryResponse]


class CodingProfileBase(BaseModel):
    platform: str = Field(
        min_length=2,
        max_length=80,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    username: str | None = Field(
        default=None,
        max_length=150,
    )

    display_name: str = Field(
        min_length=2,
        max_length=150,
    )

    profile_url: HttpUrl | None = None

    total_solved: int | None = Field(
        default=None,
        ge=0,
    )

    rating: float | None = Field(
        default=None,
        ge=0,
    )

    max_rating: float | None = Field(
        default=None,
        ge=0,
    )

    ranking: str | None = Field(
        default=None,
        max_length=200,
    )

    achievement_summary: str | None = None

    statistics: dict[str, Any] = Field(
        default_factory=dict,
    )

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class CodingProfileCreate(CodingProfileBase):
    pass


class CodingProfileUpdate(BaseModel):
    platform: str | None = Field(
        default=None,
        min_length=2,
        max_length=80,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    username: str | None = Field(
        default=None,
        max_length=150,
    )

    display_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    profile_url: HttpUrl | None = None

    total_solved: int | None = Field(
        default=None,
        ge=0,
    )

    rating: float | None = Field(
        default=None,
        ge=0,
    )

    max_rating: float | None = Field(
        default=None,
        ge=0,
    )

    ranking: str | None = Field(
        default=None,
        max_length=200,
    )

    achievement_summary: str | None = None

    statistics: dict[str, Any] | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class CodingProfileResponse(CodingProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )