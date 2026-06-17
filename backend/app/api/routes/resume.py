from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_admin
from app.db.database import get_db
from app.models.admin_user import AdminUser
from app.schemas.resume import (
    ResumeResponse,
    ResumeUpdate,
)
from app.services.file_storage import (
    FileTooLargeError,
    InvalidFileError,
    get_resume_file_path,
    store_resume_pdf,
)
from app.services.resume_service import (
    create_resume,
    delete_resume,
    get_public_resume_by_id,
    get_resume_by_id,
    increment_download_count,
    list_public_resumes,
    replace_resume_file,
    update_resume,
)


router = APIRouter(
    prefix="/api/v1/resumes",
    tags=["Resume Management"],
)


def raise_file_error(
    error: Exception,
) -> None:
    if isinstance(
        error,
        FileTooLargeError,
    ):
        raise HTTPException(
            status_code=(
                status.HTTP_413_CONTENT_TOO_LARGE
            ),
            detail=str(error),
        ) from error

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(error),
    ) from error


@router.get(
    "",
    response_model=list[ResumeResponse],
)
def list_resumes(
    database_session: Session = Depends(get_db),
):
    return list_public_resumes(
        database_session
    )


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def read_resume(
    resume_id: int,
    database_session: Session = Depends(get_db),
):
    resume = get_public_resume_by_id(
        database_session,
        resume_id,
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    return resume


@router.get(
    "/{resume_id}/download",
)
def download_resume(
    resume_id: int,
    database_session: Session = Depends(get_db),
):
    resume = get_public_resume_by_id(
        database_session,
        resume_id,
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    file_path = get_resume_file_path(
        resume.stored_filename
    )

    if not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file is missing.",
        )

    increment_download_count(
        database_session,
        resume,
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=resume.original_filename,
    )


@router.post(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    title: str = Form(
        min_length=2,
        max_length=200,
    ),
    resume_type: str = Form(
        min_length=2,
        max_length=80,
        pattern=(
            r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
        ),
    ),
    file: UploadFile = File(),
    description: str | None = Form(
        default=None,
    ),
    display_order: int = Form(
        default=0,
        ge=0,
    ),
    is_visible: bool = Form(
        default=True,
    ),
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    try:
        stored_file = await store_resume_pdf(
            file
        )

    except (
        FileTooLargeError,
        InvalidFileError,
    ) as error:
        raise_file_error(error)

    try:
        return create_resume(
            database_session=database_session,
            title=title.strip(),
            resume_type=resume_type.strip().lower(),
            description=description,
            display_order=display_order,
            is_visible=is_visible,
            stored_file=stored_file,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def update_resume_metadata(
    resume_id: int,
    resume_data: ResumeUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    resume = get_resume_by_id(
        database_session,
        resume_id,
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    update_data = resume_data.model_dump(
        exclude_unset=True
    )

    if "resume_type" in update_data:
        update_data["resume_type"] = (
            update_data["resume_type"]
            .strip()
            .lower()
        )

    try:
        return update_resume(
            database_session,
            resume,
            update_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{resume_id}/file",
    response_model=ResumeResponse,
)
async def replace_resume_pdf(
    resume_id: int,
    file: UploadFile = File(),
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    resume = get_resume_by_id(
        database_session,
        resume_id,
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    try:
        stored_file = await store_resume_pdf(
            file
        )

    except (
        FileTooLargeError,
        InvalidFileError,
    ) as error:
        raise_file_error(error)

    return replace_resume_file(
        database_session,
        resume,
        stored_file,
    )


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_resume(
    resume_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    resume = get_resume_by_id(
        database_session,
        resume_id,
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found.",
        )

    delete_resume(
        database_session,
        resume,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )