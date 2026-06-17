from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models.project import Project, ProjectImage
from app.models.research import ResearchPublication

from app.services.file_storage import (
    delete_project_file_from_url,
)

# -------------------------------------------------
# Projects
# -------------------------------------------------

def list_public_projects(
    database_session: Session,
    featured: bool | None = None,
) -> list[Project]:
    statement = (
        select(Project)
        .options(selectinload(Project.images))
        .where(Project.is_visible.is_(True))
        .order_by(
            Project.display_order.asc(),
            Project.id.asc(),
        )
    )

    if featured is not None:
        statement = statement.where(
            Project.is_featured.is_(featured)
        )

    return list(
        database_session.scalars(statement).all()
    )


def get_public_project_by_slug(
    database_session: Session,
    slug: str,
) -> Project | None:
    statement = (
        select(Project)
        .options(selectinload(Project.images))
        .where(
            Project.slug == slug,
            Project.is_visible.is_(True),
        )
    )

    return database_session.scalar(statement)


def get_project_by_id(
    database_session: Session,
    project_id: int,
) -> Project | None:
    statement = (
        select(Project)
        .options(selectinload(Project.images))
        .where(Project.id == project_id)
    )

    return database_session.scalar(statement)


def create_project(
    database_session: Session,
    project_data: dict[str, Any],
) -> Project:
    project = Project(**project_data)

    database_session.add(project)

    try:
        database_session.commit()
        database_session.refresh(project)

    except IntegrityError as error:
        database_session.rollback()

        raise ValueError(
            "A project with this slug already exists."
        ) from error

    return get_project_by_id(
        database_session,
        project.id,
    )


def update_project(
    database_session: Session,
    project: Project,
    project_data: dict[str, Any],
) -> Project:
    for field_name, field_value in project_data.items():
        setattr(
            project,
            field_name,
            field_value,
        )

    try:
        database_session.commit()
        database_session.refresh(project)

    except IntegrityError as error:
        database_session.rollback()

        raise ValueError(
            "The project could not be updated. "
            "The slug may already exist."
        ) from error

    return get_project_by_id(
        database_session,
        project.id,
    )


def delete_project(
    database_session: Session,
    project: Project,
) -> None:
    project_image_urls = [
        image.image_url
        for image in project.images
    ]

    database_session.delete(project)
    database_session.commit()

    for image_url in project_image_urls:
        delete_project_file_from_url(
            image_url
        )

def add_project_image(
    database_session: Session,
    project: Project,
    image_data: dict[str, Any],
) -> ProjectImage:
    image = ProjectImage(
        project_id=project.id,
        **image_data,
    )

    database_session.add(image)
    database_session.commit()
    database_session.refresh(image)

    return image


def get_project_image_by_id(
    database_session: Session,
    image_id: int,
) -> ProjectImage | None:
    return database_session.get(
        ProjectImage,
        image_id,
    )


def delete_project_image(
    database_session: Session,
    image: ProjectImage,
) -> None:
    image_url = image.image_url

    database_session.delete(image)
    database_session.commit()

    delete_project_file_from_url(
        image_url
    )

# -------------------------------------------------
# Research and Publications
# -------------------------------------------------

def list_public_research(
    database_session: Session,
    featured: bool | None = None,
) -> list[ResearchPublication]:
    statement = (
        select(ResearchPublication)
        .where(
            ResearchPublication.is_visible.is_(True)
        )
        .order_by(
            ResearchPublication.display_order.asc(),
            ResearchPublication.id.asc(),
        )
    )

    if featured is not None:
        statement = statement.where(
            ResearchPublication.is_featured.is_(
                featured
            )
        )

    return list(
        database_session.scalars(statement).all()
    )


def get_public_research_by_slug(
    database_session: Session,
    slug: str,
) -> ResearchPublication | None:
    statement = select(ResearchPublication).where(
        ResearchPublication.slug == slug,
        ResearchPublication.is_visible.is_(True),
    )

    return database_session.scalar(statement)


def get_research_by_id(
    database_session: Session,
    research_id: int,
) -> ResearchPublication | None:
    return database_session.get(
        ResearchPublication,
        research_id,
    )


def create_research(
    database_session: Session,
    research_data: dict[str, Any],
) -> ResearchPublication:
    research = ResearchPublication(**research_data)

    database_session.add(research)

    try:
        database_session.commit()
        database_session.refresh(research)

    except IntegrityError as error:
        database_session.rollback()

        raise ValueError(
            "A research record with this slug "
            "already exists."
        ) from error

    return research


def update_research(
    database_session: Session,
    research: ResearchPublication,
    research_data: dict[str, Any],
) -> ResearchPublication:
    for field_name, field_value in research_data.items():
        setattr(
            research,
            field_name,
            field_value,
        )

    try:
        database_session.commit()
        database_session.refresh(research)

    except IntegrityError as error:
        database_session.rollback()

        raise ValueError(
            "The research record could not be updated. "
            "The slug may already exist."
        ) from error

    return research


def delete_research(
    database_session: Session,
    research: ResearchPublication,
) -> None:
    database_session.delete(research)
    database_session.commit()