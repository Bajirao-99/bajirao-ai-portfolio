from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import (
    TrustedHostMiddleware,
)

from app.core.logging_config import (
    configure_logging,
)
from app.middleware.security_headers import (
    SecurityHeadersMiddleware,
)

from app.api.routes.achievement import (
    router as achievement_router,
)
from app.api.routes.analytics import (
    admin_router as admin_analytics_router,
)
from app.api.routes.analytics import (
    public_router as analytics_router,
)
from app.api.routes.auth import router as auth_router
from app.api.routes.certification import (
    router as certification_router,
)
from app.api.routes.coding_profile import (
    router as coding_profile_router,
)
from app.api.routes.contact import (
    admin_router as admin_contact_router,
)
from app.api.routes.contact import (
    public_router as contact_router,
)
from app.api.routes.education import (
    router as education_router,
)
from app.api.routes.experience import (
    router as experience_router,
)
from app.api.routes.github import (
    router as github_router,
)
from app.api.routes.health import router as health_router
from app.api.routes.interview_request import (
    admin_router as admin_interview_router,
)
from app.api.routes.interview_request import (
    public_router as interview_router,
)
from app.api.routes.profile import router as profile_router
from app.api.routes.project import router as project_router
from app.api.routes.research import router as research_router
from app.api.routes.resume import router as resume_router
from app.api.routes.skill import router as skill_router
from app.core.config import settings
from app.services.file_storage import (
    PROJECT_UPLOAD_DIR,
)

from app.api.routes.job_match import (
    admin_router as admin_job_match_router,
)
from app.api.routes.job_match import (
    public_router as job_match_router,
)

from app.api.routes.portfolio_chat import (
    admin_router as admin_chat_router,
)
from app.api.routes.portfolio_chat import (
    public_router as portfolio_chat_router,
)

configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description=(
        "Backend API for Bajirao's "
        "Advanced AI Portfolio"
    ),
    version=settings.app_version,
    debug=settings.debug,
    docs_url=(
        "/docs"
        if settings.enable_docs
        else None
    ),
    redoc_url=(
        "/redoc"
        if settings.enable_docs
        else None
    ),
    openapi_url=(
        "/openapi.json"
        if settings.enable_docs
        else None
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        settings.cors_origins_list
    ),
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "X-Request-ID",
    ],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=(
        settings.trusted_hosts_list
    ),
)

app.add_middleware(
    SecurityHeadersMiddleware,
    environment=settings.app_env,
)

app.mount(
    "/media/projects",
    StaticFiles(
        directory=str(PROJECT_UPLOAD_DIR)
    ),
    name="project-media",
)

@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    error: Exception,
):
    request_id = request.headers.get(
        "X-Request-ID",
        "not-provided",
    )

    logger.exception(
        "Unhandled API error. "
        "Path=%s RequestID=%s",
        request.url.path,
        request_id,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": (
                "An unexpected server error "
                "occurred."
            ),
            "request_id": request_id,
        },
    )

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(education_router)
app.include_router(experience_router)
app.include_router(skill_router)
app.include_router(achievement_router)
app.include_router(certification_router)
app.include_router(project_router)
app.include_router(research_router)
app.include_router(resume_router)
app.include_router(github_router)
app.include_router(coding_profile_router)

app.include_router(contact_router)
app.include_router(interview_router)
app.include_router(analytics_router)
app.include_router(job_match_router)
app.include_router(portfolio_chat_router)

app.include_router(admin_contact_router)
app.include_router(admin_interview_router)
app.include_router(admin_analytics_router)
app.include_router(admin_job_match_router)
app.include_router(admin_chat_router)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": (
            "Bajirao AI Portfolio API is running"
        ),
        "status": "success",
        "documentation": "/docs",
    }