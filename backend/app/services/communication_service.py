from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.contact_message import ContactMessage
from app.models.interview_request import InterviewRequest


# -------------------------------------------------
# Contact Messages
# -------------------------------------------------

def create_contact_message(
    database_session: Session,
    message_data: dict[str, Any],
) -> ContactMessage:
    contact_message = ContactMessage(
        **message_data
    )

    database_session.add(
        contact_message
    )

    database_session.commit()
    database_session.refresh(
        contact_message
    )

    return contact_message


def list_contact_messages(
    database_session: Session,
    status_filter: str | None,
    limit: int,
    offset: int,
) -> list[ContactMessage]:
    statement = (
        select(ContactMessage)
        .order_by(
            ContactMessage.created_at.desc()
        )
        .limit(limit)
        .offset(offset)
    )

    if status_filter is not None:
        statement = statement.where(
            ContactMessage.status
            == status_filter
        )

    return list(
        database_session.scalars(
            statement
        ).all()
    )


def get_contact_message_by_id(
    database_session: Session,
    message_id: int,
) -> ContactMessage | None:
    return database_session.get(
        ContactMessage,
        message_id,
    )


def update_contact_message(
    database_session: Session,
    contact_message: ContactMessage,
    update_data: dict[str, Any],
) -> ContactMessage:
    for field_name, field_value in (
        update_data.items()
    ):
        setattr(
            contact_message,
            field_name,
            field_value,
        )

    database_session.commit()
    database_session.refresh(
        contact_message
    )

    return contact_message


def delete_contact_message(
    database_session: Session,
    contact_message: ContactMessage,
) -> None:
    database_session.delete(
        contact_message
    )
    database_session.commit()


# -------------------------------------------------
# Interview Requests
# -------------------------------------------------

def create_interview_request(
    database_session: Session,
    request_data: dict[str, Any],
) -> InterviewRequest:
    interview_request = InterviewRequest(
        **request_data
    )

    database_session.add(
        interview_request
    )

    database_session.commit()
    database_session.refresh(
        interview_request
    )

    return interview_request


def list_interview_requests(
    database_session: Session,
    status_filter: str | None,
    limit: int,
    offset: int,
) -> list[InterviewRequest]:
    statement = (
        select(InterviewRequest)
        .order_by(
            InterviewRequest.created_at.desc()
        )
        .limit(limit)
        .offset(offset)
    )

    if status_filter is not None:
        statement = statement.where(
            InterviewRequest.status
            == status_filter
        )

    return list(
        database_session.scalars(
            statement
        ).all()
    )


def get_interview_request_by_id(
    database_session: Session,
    request_id: int,
) -> InterviewRequest | None:
    return database_session.get(
        InterviewRequest,
        request_id,
    )


def update_interview_request(
    database_session: Session,
    interview_request: InterviewRequest,
    update_data: dict[str, Any],
) -> InterviewRequest:
    for field_name, field_value in (
        update_data.items()
    ):
        setattr(
            interview_request,
            field_name,
            field_value,
        )

    database_session.commit()
    database_session.refresh(
        interview_request
    )

    return interview_request


def delete_interview_request(
    database_session: Session,
    interview_request: InterviewRequest,
) -> None:
    database_session.delete(
        interview_request
    )
    database_session.commit()