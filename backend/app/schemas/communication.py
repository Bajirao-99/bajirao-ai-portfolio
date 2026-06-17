from datetime import datetime
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


ContactStatus = Literal[
    "new",
    "read",
    "replied",
    "archived",
]

InterviewStatus = Literal[
    "pending",
    "reviewed",
    "scheduled",
    "completed",
    "declined",
    "archived",
]


class SubmissionResponse(BaseModel):
    id: int
    status: str
    message: str
    created_at: datetime


# -------------------------------------------------
# Contact Messages
# -------------------------------------------------

class ContactMessageCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=150,
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    subject: str = Field(
        min_length=3,
        max_length=250,
    )

    message: str = Field(
        min_length=10,
        max_length=5000,
    )


class ContactMessageUpdate(BaseModel):
    status: ContactStatus | None = None

    admin_notes: str | None = Field(
        default=None,
        max_length=5000,
    )


class ContactMessageAdminResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None
    subject: str
    message: str
    status: str
    admin_notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# -------------------------------------------------
# Interview Requests
# -------------------------------------------------

class InterviewRequestCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=150,
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    company: str = Field(
        min_length=2,
        max_length=200,
    )

    role: str = Field(
        min_length=2,
        max_length=200,
    )

    preferred_datetime: datetime | None = None

    timezone: str | None = Field(
        default=None,
        max_length=100,
    )

    meeting_mode: str | None = Field(
        default=None,
        max_length=100,
    )

    message: str | None = Field(
        default=None,
        max_length=5000,
    )

    @field_validator("preferred_datetime")
    @classmethod
    def validate_timezone_information(
        cls,
        value: datetime | None,
    ) -> datetime | None:
        if (
            value is not None
            and value.tzinfo is None
        ):
            raise ValueError(
                "preferred_datetime must include "
                "timezone information."
            )

        return value


class InterviewRequestUpdate(BaseModel):
    status: InterviewStatus | None = None

    admin_notes: str | None = Field(
        default=None,
        max_length=5000,
    )

    preferred_datetime: datetime | None = None

    @field_validator("preferred_datetime")
    @classmethod
    def validate_timezone_information(
        cls,
        value: datetime | None,
    ) -> datetime | None:
        if (
            value is not None
            and value.tzinfo is None
        ):
            raise ValueError(
                "preferred_datetime must include "
                "timezone information."
            )

        return value


class InterviewRequestAdminResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None
    company: str
    role: str
    preferred_datetime: datetime | None
    timezone: str | None
    meeting_mode: str | None
    message: str | None
    status: str
    admin_notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )