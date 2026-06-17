import re
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.core.config import BASE_DIR


UPLOAD_ROOT = BASE_DIR / "uploads"
PROJECT_UPLOAD_DIR = UPLOAD_ROOT / "projects"
RESUME_UPLOAD_DIR = UPLOAD_ROOT / "resumes"

PROJECT_UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

RESUME_UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024
MAX_RESUME_SIZE_BYTES = 10 * 1024 * 1024
UPLOAD_CHUNK_SIZE = 1024 * 1024


ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/octet-stream",
}

ALLOWED_PDF_CONTENT_TYPES = {
    "application/pdf",
    "application/octet-stream",
}

IMAGE_FORMAT_EXTENSIONS = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "WEBP": ".webp",
}

IMAGE_FORMAT_MIME_TYPES = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
}


class FileStorageError(Exception):
    pass


class FileTooLargeError(FileStorageError):
    pass


class InvalidFileError(FileStorageError):
    pass


@dataclass(frozen=True)
class StoredFile:
    original_filename: str
    stored_filename: str
    file_size_bytes: int
    mime_type: str
    public_url: str | None = None


def sanitize_filename(
    filename: str | None,
    default_name: str,
) -> str:
    raw_name = Path(
        filename or default_name
    ).name

    sanitized_name = re.sub(
        r"[^A-Za-z0-9._ -]",
        "_",
        raw_name,
    ).strip()

    if not sanitized_name:
        return default_name

    return sanitized_name[:200]


async def write_limited_upload(
    upload_file: UploadFile,
    destination: Path,
    maximum_size: int,
) -> int:
    total_size = 0

    try:
        with destination.open("wb") as output_file:
            while True:
                chunk = await upload_file.read(
                    UPLOAD_CHUNK_SIZE
                )

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > maximum_size:
                    raise FileTooLargeError(
                        "Uploaded file exceeds the allowed size."
                    )

                output_file.write(chunk)

    except Exception:
        destination.unlink(
            missing_ok=True
        )
        raise

    if total_size == 0:
        destination.unlink(
            missing_ok=True
        )

        raise InvalidFileError(
            "Uploaded file is empty."
        )

    return total_size


async def store_project_image(
    upload_file: UploadFile,
) -> StoredFile:
    if (
        upload_file.content_type
        not in ALLOWED_IMAGE_CONTENT_TYPES
    ):
        raise InvalidFileError(
            "Only JPG, PNG and WebP images are allowed."
        )

    original_filename = sanitize_filename(
        upload_file.filename,
        "project-image",
    )

    temporary_path = (
        PROJECT_UPLOAD_DIR
        / f"{uuid4().hex}.upload"
    )

    file_size = await write_limited_upload(
        upload_file=upload_file,
        destination=temporary_path,
        maximum_size=MAX_IMAGE_SIZE_BYTES,
    )

    try:
        with Image.open(temporary_path) as image:
            detected_format = image.format

            if (
                detected_format
                not in IMAGE_FORMAT_EXTENSIONS
            ):
                raise InvalidFileError(
                    "Unsupported image format."
                )

            image.verify()

    except (
        UnidentifiedImageError,
        OSError,
        ValueError,
        Image.DecompressionBombError,
    ) as error:
        temporary_path.unlink(
            missing_ok=True
        )

        raise InvalidFileError(
            "The uploaded file is not a valid image."
        ) from error

    extension = IMAGE_FORMAT_EXTENSIONS[
        detected_format
    ]

    mime_type = IMAGE_FORMAT_MIME_TYPES[
        detected_format
    ]

    stored_filename = (
        f"{uuid4().hex}{extension}"
    )

    final_path = (
        PROJECT_UPLOAD_DIR
        / stored_filename
    )

    temporary_path.replace(final_path)

    return StoredFile(
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_size_bytes=file_size,
        mime_type=mime_type,
        public_url=(
            f"/media/projects/{stored_filename}"
        ),
    )


async def store_resume_pdf(
    upload_file: UploadFile,
) -> StoredFile:
    if (
        upload_file.content_type
        not in ALLOWED_PDF_CONTENT_TYPES
    ):
        raise InvalidFileError(
            "Only PDF resume files are allowed."
        )

    original_filename = sanitize_filename(
        upload_file.filename,
        "resume.pdf",
    )

    if (
        Path(original_filename).suffix.lower()
        != ".pdf"
    ):
        raise InvalidFileError(
            "Resume filename must end with .pdf."
        )

    temporary_path = (
        RESUME_UPLOAD_DIR
        / f"{uuid4().hex}.upload"
    )

    file_size = await write_limited_upload(
        upload_file=upload_file,
        destination=temporary_path,
        maximum_size=MAX_RESUME_SIZE_BYTES,
    )

    try:
        with temporary_path.open("rb") as pdf_file:
            if pdf_file.read(5) != b"%PDF-":
                raise InvalidFileError(
                    "The uploaded file is not a PDF."
                )

        pdf_reader = PdfReader(
            str(temporary_path),
            strict=True,
        )

        if pdf_reader.is_encrypted:
            raise InvalidFileError(
                "Password-protected PDFs are not allowed."
            )

        if len(pdf_reader.pages) == 0:
            raise InvalidFileError(
                "The PDF does not contain any pages."
            )

    except InvalidFileError:
        temporary_path.unlink(
            missing_ok=True
        )
        raise

    except (
        PdfReadError,
        OSError,
        ValueError,
    ) as error:
        temporary_path.unlink(
            missing_ok=True
        )

        raise InvalidFileError(
            "The uploaded file is not a valid PDF."
        ) from error

    stored_filename = (
        f"{uuid4().hex}.pdf"
    )

    final_path = (
        RESUME_UPLOAD_DIR
        / stored_filename
    )

    temporary_path.replace(final_path)

    return StoredFile(
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_size_bytes=file_size,
        mime_type="application/pdf",
    )


def get_resume_file_path(
    stored_filename: str,
) -> Path:
    safe_filename = Path(
        stored_filename
    ).name

    return (
        RESUME_UPLOAD_DIR
        / safe_filename
    )


def delete_resume_file(
    stored_filename: str,
) -> None:
    file_path = get_resume_file_path(
        stored_filename
    )

    file_path.unlink(
        missing_ok=True
    )


def delete_project_file_by_name(
    stored_filename: str,
) -> None:
    safe_filename = Path(
        stored_filename
    ).name

    file_path = (
        PROJECT_UPLOAD_DIR
        / safe_filename
    )

    file_path.unlink(
        missing_ok=True
    )


def delete_project_file_from_url(
    image_url: str,
) -> None:
    local_prefix = "/media/projects/"

    if not image_url.startswith(
        local_prefix
    ):
        return

    stored_filename = image_url.removeprefix(
        local_prefix
    )

    delete_project_file_by_name(
        stored_filename
    )