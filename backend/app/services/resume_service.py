from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.services.file_storage import (
    StoredFile,
    delete_resume_file,
)


def list_public_resumes(
    database_session: Session,
) -> list[Resume]:
    statement = (
        select(Resume)
        .where(Resume.is_visible.is_(True))
        .order_by(
            Resume.display_order.asc(),
            Resume.id.asc(),
        )
    )

    return list(
        database_session.scalars(
            statement
        ).all()
    )


def get_public_resume_by_id(
    database_session: Session,
    resume_id: int,
) -> Resume | None:
    statement = select(Resume).where(
        Resume.id == resume_id,
        Resume.is_visible.is_(True),
    )

    return database_session.scalar(
        statement
    )


def get_resume_by_id(
    database_session: Session,
    resume_id: int,
) -> Resume | None:
    return database_session.get(
        Resume,
        resume_id,
    )


def create_resume(
    database_session: Session,
    title: str,
    resume_type: str,
    description: str | None,
    display_order: int,
    is_visible: bool,
    stored_file: StoredFile,
) -> Resume:
    resume = Resume(
        title=title,
        resume_type=resume_type,
        description=description,
        original_filename=(
            stored_file.original_filename
        ),
        stored_filename=(
            stored_file.stored_filename
        ),
        mime_type=stored_file.mime_type,
        file_size_bytes=(
            stored_file.file_size_bytes
        ),
        display_order=display_order,
        is_visible=is_visible,
    )

    database_session.add(resume)

    try:
        database_session.commit()
        database_session.refresh(resume)

    except IntegrityError as error:
        database_session.rollback()

        delete_resume_file(
            stored_file.stored_filename
        )

        raise ValueError(
            "A resume with this resume type "
            "already exists."
        ) from error

    except Exception:
        database_session.rollback()

        delete_resume_file(
            stored_file.stored_filename
        )

        raise

    return resume


def update_resume(
    database_session: Session,
    resume: Resume,
    resume_data: dict[str, Any],
) -> Resume:
    for field_name, field_value in resume_data.items():
        setattr(
            resume,
            field_name,
            field_value,
        )

    try:
        database_session.commit()
        database_session.refresh(resume)

    except IntegrityError as error:
        database_session.rollback()

        raise ValueError(
            "A resume with this type already exists."
        ) from error

    return resume


def replace_resume_file(
    database_session: Session,
    resume: Resume,
    stored_file: StoredFile,
) -> Resume:
    old_stored_filename = (
        resume.stored_filename
    )

    resume.original_filename = (
        stored_file.original_filename
    )

    resume.stored_filename = (
        stored_file.stored_filename
    )

    resume.mime_type = (
        stored_file.mime_type
    )

    resume.file_size_bytes = (
        stored_file.file_size_bytes
    )

    try:
        database_session.commit()
        database_session.refresh(resume)

    except Exception:
        database_session.rollback()

        delete_resume_file(
            stored_file.stored_filename
        )

        raise

    delete_resume_file(
        old_stored_filename
    )

    return resume


def increment_download_count(
    database_session: Session,
    resume: Resume,
) -> Resume:
    resume.download_count += 1

    database_session.commit()
    database_session.refresh(resume)

    return resume


def delete_resume(
    database_session: Session,
    resume: Resume,
) -> None:
    stored_filename = (
        resume.stored_filename
    )

    database_session.delete(resume)
    database_session.commit()

    delete_resume_file(
        stored_filename
    )