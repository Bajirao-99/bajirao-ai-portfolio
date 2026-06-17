from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    Response,
    UploadFile,
    status,
)

from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_admin
from app.db.database import get_db
from app.models.admin_user import AdminUser
from app.schemas.showcase import (
    ProjectCreate,
    ProjectImageCreate,
    ProjectImageResponse,
    ProjectResponse,
    ProjectUpdate,
)

from app.services.file_storage import (
    FileTooLargeError,
    InvalidFileError,
    delete_project_file_by_name,
    store_project_image,
)

from app.services.showcase_service import (
    add_project_image,
    create_project,
    delete_project,
    delete_project_image,
    get_project_by_id,
    get_project_image_by_id,
    get_public_project_by_slug,
    list_public_projects,
    update_project,
)


router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Project Showcase"],
)


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def list_projects(
    featured: bool | None = Query(
        default=None,
        description=(
            "Filter projects by featured status."
        ),
    ),
    database_session: Session = Depends(get_db),
):
    return list_public_projects(
        database_session=database_session,
        featured=featured,
    )


@router.get(
    "/slug/{slug}",
    response_model=ProjectResponse,
)
def read_project_by_slug(
    slug: str,
    database_session: Session = Depends(get_db),
):
    project = get_public_project_by_slug(
        database_session=database_session,
        slug=slug,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project_record(
    project_data: ProjectCreate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    try:
        return create_project(
            database_session=database_session,
            project_data=project_data.model_dump(
                mode="json",
            ),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project_record(
    project_id: int,
    project_data: ProjectUpdate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    project = get_project_by_id(
        database_session=database_session,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    try:
        return update_project(
            database_session=database_session,
            project=project,
            project_data=project_data.model_dump(
                exclude_unset=True,
                mode="json",
            ),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project_record(
    project_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    project = get_project_by_id(
        database_session=database_session,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    delete_project(
        database_session=database_session,
        project=project,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.post(
    "/{project_id}/images",
    response_model=ProjectImageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project_image(
    project_id: int,
    image_data: ProjectImageCreate,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    project = get_project_by_id(
        database_session=database_session,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return add_project_image(
        database_session=database_session,
        project=project,
        image_data=image_data.model_dump(
            mode="json",
        ),
    )

@router.post(
    "/{project_id}/upload-image",
    response_model=ProjectImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_project_image(
    project_id: int,
    file: UploadFile = File(),
    alt_text: str = Form(
        min_length=2,
        max_length=250,
    ),
    caption: str | None = Form(
        default=None,
        max_length=500,
    ),
    display_order: int = Form(
        default=0,
        ge=0,
    ),
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    project = get_project_by_id(
        database_session=database_session,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    try:
        stored_file = await store_project_image(
            file
        )

    except FileTooLargeError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_413_CONTENT_TOO_LARGE
            ),
            detail=str(error),
        ) from error

    except InvalidFileError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    try:
        return add_project_image(
            database_session=database_session,
            project=project,
            image_data={
                "image_url": stored_file.public_url,
                "alt_text": alt_text.strip(),
                "caption": caption,
                "display_order": display_order,
            },
        )

    except Exception:
        delete_project_file_by_name(
            stored_file.stored_filename
        )
        raise
    
@router.delete(
    "/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_project_image(
    image_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    image = get_project_image_by_id(
        database_session=database_session,
        image_id=image_id,
    )

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project image not found.",
        )

    delete_project_image(
        database_session=database_session,
        image=image,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )