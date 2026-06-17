from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ResumeUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    resume_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=80,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    description: str | None = None

    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    is_visible: bool | None = None


class ResumeResponse(BaseModel):
    id: int
    title: str
    resume_type: str
    description: str | None
    original_filename: str
    mime_type: str
    file_size_bytes: int
    download_count: int
    download_url: str
    display_order: int
    is_visible: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )