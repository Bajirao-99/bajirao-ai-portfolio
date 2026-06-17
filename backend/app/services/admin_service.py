from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.admin_user import AdminUser


def get_admin_by_id(
    database_session: Session,
    admin_id: int,
) -> AdminUser | None:
    return database_session.get(
        AdminUser,
        admin_id,
    )


def get_admin_by_username(
    database_session: Session,
    username: str,
) -> AdminUser | None:
    statement = select(AdminUser).where(
        AdminUser.username == username.lower()
    )

    return database_session.scalar(statement)


def authenticate_admin(
    database_session: Session,
    username: str,
    password: str,
) -> AdminUser | None:
    admin = get_admin_by_username(
        database_session=database_session,
        username=username,
    )

    if admin is None:
        return None

    if not verify_password(
        plain_password=password,
        stored_password_hash=admin.password_hash,
    ):
        return None

    return admin


def record_admin_login(
    database_session: Session,
    admin: AdminUser,
) -> AdminUser:
    admin.last_login = datetime.now(timezone.utc)

    database_session.commit()
    database_session.refresh(admin)

    return admin