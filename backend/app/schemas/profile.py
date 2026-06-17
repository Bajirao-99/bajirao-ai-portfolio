from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
)


class ProfileBase(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=120,
    )

    headline: str = Field(
        min_length=2,
        max_length=250,
    )

    short_bio: str = Field(
        min_length=10,
        max_length=500,
    )

    about_me: str = Field(
        min_length=20,
    )

    email: EmailStr

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    location: str | None = Field(
        default=None,
        max_length=150,
    )

    profile_image_url: HttpUrl | None = None
    linkedin_url: HttpUrl | None = None
    github_url: HttpUrl | None = None
    leetcode_url: HttpUrl | None = None
    codechef_url: HttpUrl | None = None

    years_experience: float = Field(
        default=0.0,
        ge=0,
        le=60,
    )


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=120,
    )

    headline: str | None = Field(
        default=None,
        min_length=2,
        max_length=250,
    )

    short_bio: str | None = Field(
        default=None,
        min_length=10,
        max_length=500,
    )

    about_me: str | None = Field(
        default=None,
        min_length=20,
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    location: str | None = Field(
        default=None,
        max_length=150,
    )

    profile_image_url: HttpUrl | None = None
    linkedin_url: HttpUrl | None = None
    github_url: HttpUrl | None = None
    leetcode_url: HttpUrl | None = None
    codechef_url: HttpUrl | None = None

    years_experience: float | None = Field(
        default=None,
        ge=0,
        le=60,
    )

    is_active: bool | None = None


class ProfileResponse(ProfileBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )