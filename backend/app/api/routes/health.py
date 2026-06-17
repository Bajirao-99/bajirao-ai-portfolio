import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api/v1",
    tags=["Health"],
)


@router.get(
    "/health",
    include_in_schema=False,
)
def health_check():
    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@router.get(
    "/ready",
    include_in_schema=False,
)
def readiness_check(
    database_session: Session = Depends(
        get_db
    ),
):
    try:
        database_session.execute(
            text("SELECT 1")
        )

        return {
            "status": "ready",
            "database": "connected",
        }

    except SQLAlchemyError as error:
        logger.exception(
            "Database readiness check failed."
        )

        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=(
                "Application dependencies "
                "are not ready."
            ),
        ) from error