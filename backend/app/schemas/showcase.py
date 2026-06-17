from datetime import date, datetime
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    StringConstraints,
)


StackItem = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=80,
    ),
]

ModelName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100,
    ),
]

MetricValue = float | int | str


# -------------------------------------------------
# Project Images
# -------------------------------------------------

class ProjectImageCreate(BaseModel):
    image_url: str = Field(
        min_length=1,
        max_length=500,
    )

    alt_text: str = Field(
        min_length=2,
        max_length=250,
    )

    caption: str | None = Field(
        default=None,
        max_length=500,
    )

    display_order: int = Field(
        default=0,
        ge=0,
    )


class ProjectImageResponse(BaseModel):
    id: int
    project_id: int
    image_url: str
    alt_text: str
    caption: str | None
    display_order: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# -------------------------------------------------
# Projects
# -------------------------------------------------

class ProjectBase(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    slug: str = Field(
        min_length=2,
        max_length=220,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    category: str = Field(
        min_length=2,
        max_length=100,
    )

    short_description: str = Field(
        min_length=10,
        max_length=500,
    )

    description: str = Field(
        min_length=20,
    )

    tech_stack: list[StackItem] = Field(
        default_factory=list,
        max_length=30,
    )

    github_url: HttpUrl | None = None
    live_demo_url: HttpUrl | None = None

    challenges: str | None = None
    solutions: str | None = None
    results: str | None = None

    is_featured: bool = False

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    slug: str | None = Field(
        default=None,
        min_length=2,
        max_length=220,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    category: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    short_description: str | None = Field(
        default=None,
        min_length=10,
        max_length=500,
    )

    description: str | None = Field(
        default=None,
        min_length=20,
    )

    tech_stack: list[StackItem] | None = Field(
        default=None,
        max_length=30,
    )

    github_url: HttpUrl | None = None
    live_demo_url: HttpUrl | None = None

    challenges: str | None = None
    solutions: str | None = None
    results: str | None = None

    is_featured: bool | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class ProjectResponse(ProjectBase):
    id: int
    view_count: int
    images: list[ProjectImageResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# -------------------------------------------------
# Research and Publications
# -------------------------------------------------

class ResearchBase(BaseModel):
    title: str = Field(
        min_length=5,
        max_length=300,
    )

    slug: str = Field(
        min_length=2,
        max_length=320,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    research_type: str = Field(
        min_length=2,
        max_length=100,
    )

    short_summary: str = Field(
        min_length=10,
        max_length=500,
    )

    abstract: str = Field(
        min_length=20,
    )

    dataset_details: str | None = None
    methodology: str | None = None

    models_used: list[ModelName] = Field(
        default_factory=list,
        max_length=30,
    )

    metrics: dict[str, MetricValue] = Field(
        default_factory=dict,
    )

    publication_status: str = Field(
        min_length=2,
        max_length=100,
    )

    publication_date: date | None = None

    venue: str | None = Field(
        default=None,
        max_length=250,
    )

    paper_url: HttpUrl | None = None
    thesis_url: HttpUrl | None = None
    code_url: HttpUrl | None = None

    is_featured: bool = False

    display_order: int = Field(
        default=0,
        ge=0,
    )

    is_visible: bool = True


class ResearchCreate(ResearchBase):
    pass


class ResearchUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=5,
        max_length=300,
    )

    slug: str | None = Field(
        default=None,
        min_length=2,
        max_length=320,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    research_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    short_summary: str | None = Field(
        default=None,
        min_length=10,
        max_length=500,
    )

    abstract: str | None = Field(
        default=None,
        min_length=20,
    )

    dataset_details: str | None = None
    methodology: str | None = None

    models_used: list[ModelName] | None = Field(
        default=None,
        max_length=30,
    )

    metrics: dict[str, MetricValue] | None = None

    publication_status: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    publication_date: date | None = None

    venue: str | None = Field(
        default=None,
        max_length=250,
    )

    paper_url: HttpUrl | None = None
    thesis_url: HttpUrl | None = None
    code_url: HttpUrl | None = None

    is_featured: bool | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class ResearchResponse(ResearchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )