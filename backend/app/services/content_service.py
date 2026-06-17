from typing import Any, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import Base


ModelType = TypeVar(
    "ModelType",
    bound=Base,
)


def list_visible_records(
    database_session: Session,
    model: type[ModelType],
) -> list[ModelType]:
    statement = (
        select(model)
        .where(model.is_visible.is_(True))
        .order_by(
            model.display_order.asc(),
            model.id.asc(),
        )
    )

    return list(
        database_session.scalars(statement).all()
    )


def get_record_by_id(
    database_session: Session,
    model: type[ModelType],
    record_id: int,
) -> ModelType | None:
    return database_session.get(
        model,
        record_id,
    )


def create_record(
    database_session: Session,
    model: type[ModelType],
    record_data: dict[str, Any],
    entity_name: str,
) -> ModelType:
    record = model(**record_data)

    database_session.add(record)

    try:
        database_session.commit()
        database_session.refresh(record)

    except IntegrityError as error:
        database_session.rollback()

        raise ValueError(
            f"{entity_name} could not be created. "
            "Duplicate or invalid data was supplied."
        ) from error

    return record


def update_record(
    database_session: Session,
    record: ModelType,
    record_data: dict[str, Any],
    entity_name: str,
) -> ModelType:
    for field_name, field_value in record_data.items():
        setattr(
            record,
            field_name,
            field_value,
        )

    try:
        database_session.commit()
        database_session.refresh(record)

    except IntegrityError as error:
        database_session.rollback()

        raise ValueError(
            f"{entity_name} could not be updated. "
            "Duplicate or invalid data was supplied."
        ) from error

    return record


def delete_record(
    database_session: Session,
    record: ModelType,
) -> None:
    database_session.delete(record)
    database_session.commit()