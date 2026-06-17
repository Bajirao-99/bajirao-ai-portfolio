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
from app.schemas.communication import (
    ContactMessageAdminResponse,
    ContactMessageCreate,
    ContactMessageUpdate,
    SubmissionResponse,
)
from app.services.communication_service import (
    create_contact_message,
    delete_contact_message,
    get_contact_message_by_id,
    list_contact_messages,
    update_contact_message,
)


public_router = APIRouter(
    prefix="/api/v1/contact",
    tags=["Contact"],
)


admin_router = APIRouter(
    prefix="/api/v1/admin/contact-messages",
    tags=["Admin Contact Messages"],
)


@public_router.post(
    "",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_contact_message(
    message_data: ContactMessageCreate,
    database_session: Session = Depends(get_db),
):
    contact_message = create_contact_message(
        database_session=database_session,
        message_data=message_data.model_dump(),
    )

    return {
        "id": contact_message.id,
        "status": contact_message.status,
        "message": (
            "Your message has been submitted "
            "successfully."
        ),
        "created_at": contact_message.created_at,
    }


@admin_router.get(
    "",
    response_model=list[
        ContactMessageAdminResponse
    ],
)
def read_contact_messages(
    message_status: str | None = Query(
        default=None,
        alias="status",
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return list_contact_messages(
        database_session=database_session,
        status_filter=message_status,
        limit=limit,
        offset=offset,
    )


@admin_router.get(
    "/{message_id}",
    response_model=ContactMessageAdminResponse,
)
def read_contact_message(
    message_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    contact_message = get_contact_message_by_id(
        database_session=database_session,
        message_id=message_id,
    )

    if contact_message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact message not found.",
        )

    return contact_message


@admin_router.put(
    "/{message_id}",
    response_model=ContactMessageAdminResponse,
)
def modify_contact_message(
    message_id: int,
    update_data: ContactMessageUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    contact_message = get_contact_message_by_id(
        database_session=database_session,
        message_id=message_id,
    )

    if contact_message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact message not found.",
        )

    return update_contact_message(
        database_session=database_session,
        contact_message=contact_message,
        update_data=update_data.model_dump(
            exclude_unset=True
        ),
    )


@admin_router.delete(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_contact_message(
    message_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    contact_message = get_contact_message_by_id(
        database_session=database_session,
        message_id=message_id,
    )

    if contact_message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact message not found.",
        )

    delete_contact_message(
        database_session=database_session,
        contact_message=contact_message,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )