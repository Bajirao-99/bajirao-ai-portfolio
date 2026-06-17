from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.profile import Profile


def get_active_profile(
    database_session: Session,
) -> Profile | None:
    statement = (
        select(Profile)
        .where(Profile.is_active.is_(True))
        .order_by(Profile.id.asc())
    )

    return database_session.scalar(statement)


def get_profile_by_id(
    database_session: Session,
    profile_id: int,
) -> Profile | None:
    return database_session.get(
        Profile,
        profile_id,
    )


def create_profile(
    database_session: Session,
    profile_data: dict,
) -> Profile:
    existing_profile = get_active_profile(database_session)

    if existing_profile is not None:
        raise ValueError(
            "An active professional profile already exists."
        )

    profile = Profile(**profile_data)

    database_session.add(profile)

    try:
        database_session.commit()
        database_session.refresh(profile)

    except IntegrityError as error:
        database_session.rollback()

        raise ValueError(
            "A profile with this email already exists."
        ) from error

    return profile


def update_profile(
    database_session: Session,
    profile: Profile,
    profile_data: dict,
) -> Profile:
    for field_name, field_value in profile_data.items():
        setattr(
            profile,
            field_name,
            field_value,
        )

    try:
        database_session.commit()
        database_session.refresh(profile)

    except IntegrityError as error:
        database_session.rollback()

        raise ValueError(
            "The updated profile contains duplicate data."
        ) from error

    return profile