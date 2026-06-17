from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_admin
from app.core.config import settings
from app.core.security import create_access_token
from app.db.database import get_db
from app.models.admin_user import AdminUser
from app.schemas.auth import AdminResponse, TokenResponse
from app.services.admin_service import (
    authenticate_admin,
    record_admin_login,
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Admin Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        401: {
            "description": "Incorrect username or password."
        },
        403: {
            "description": "Admin account is disabled."
        },
    },
)
def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    database_session: Session = Depends(get_db),
):
    admin = authenticate_admin(
        database_session=database_session,
        username=form_data.username.strip(),
        password=form_data.password,
    )

    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is disabled.",
        )

    record_admin_login(
        database_session=database_session,
        admin=admin,
    )

    access_token = create_access_token(
        subject=admin.id,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=(
            settings.access_token_expire_minutes * 60
        ),
    )


@router.get(
    "/me",
    response_model=AdminResponse,
)
def read_current_admin(
    current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return current_admin