from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


# -------------------------------------------------
# Education
# -------------------------------------------------

class EducationBase(BaseModel):
    institution: str = Field(
        min_length=2,
        max_length=200,
    )
    degree: str = Field(
        min_length=2,
        max_length=150,
    )
    field_of_study: str = Field(
        min_length=2,
        max_length=150,
    )
    start_date: date
    end_date: date | None = None
    grade: str | None = Field(
        default=None,
        max_length=100,
    )
    description: str | None = None
    location: str | None = Field(
        default=None,
        max_length=150,
    )
    display_order: int = Field(
        default=0,
        ge=0,
    )
    is_visible: bool = True


class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    institution: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )
    degree: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    field_of_study: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    start_date: date | None = None
    end_date: date | None = None
    grade: str | None = Field(
        default=None,
        max_length=100,
    )
    description: str | None = None
    location: str | None = Field(
        default=None,
        max_length=150,
    )
    display_order: int | None = Field(
        default=None,
        ge=0,
    )
    is_visible: bool | None = None


class EducationResponse(EducationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# -------------------------------------------------
# Experience
# -------------------------------------------------

class ExperienceBase(BaseModel):
    organization: str = Field(
        min_length=2,
        max_length=200,
    )
    job_title: str = Field(
        min_length=2,
        max_length=150,
    )
    employment_type: str | None = Field(
        default=None,
        max_length=80,
    )
    location: str | None = Field(
        default=None,
        max_length=150,
    )
    start_date: date
    end_date: date | None = None
    is_current: bool = False
    description: str | None = None
    display_order: int = Field(
        default=0,
        ge=0,
    )
    is_visible: bool = True


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    organization: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )
    job_title: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    employment_type: str | None = Field(
        default=None,
        max_length=80,
    )
    location: str | None = Field(
        default=None,
        max_length=150,
    )
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None
    description: str | None = None
    display_order: int | None = Field(
        default=None,
        ge=0,
    )
    is_visible: bool | None = None


class ExperienceResponse(ExperienceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# -------------------------------------------------
# Skill
# -------------------------------------------------

class SkillBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    category: str = Field(
        min_length=2,
        max_length=100,
    )
    proficiency: int = Field(
        default=50,
        ge=0,
        le=100,
    )
    icon_name: str | None = Field(
        default=None,
        max_length=100,
    )
    is_featured: bool = False
    display_order: int = Field(
        default=0,
        ge=0,
    )
    is_visible: bool = True


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    category: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    proficiency: int | None = Field(
        default=None,
        ge=0,
        le=100,
    )
    icon_name: str | None = Field(
        default=None,
        max_length=100,
    )
    is_featured: bool | None = None
    display_order: int | None = Field(
        default=None,
        ge=0,
    )
    is_visible: bool | None = None


class SkillResponse(SkillBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# -------------------------------------------------
# Achievement
# -------------------------------------------------

class AchievementBase(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=250,
    )
    issuer: str | None = Field(
        default=None,
        max_length=200,
    )
    achievement_date: date | None = None
    result: str | None = Field(
        default=None,
        max_length=200,
    )
    description: str | None = None
    proof_url: str | None = Field(
        default=None,
        max_length=500,
    )
    display_order: int = Field(
        default=0,
        ge=0,
    )
    is_visible: bool = True


class AchievementCreate(AchievementBase):
    pass


class AchievementUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=250,
    )
    issuer: str | None = Field(
        default=None,
        max_length=200,
    )
    achievement_date: date | None = None
    result: str | None = Field(
        default=None,
        max_length=200,
    )
    description: str | None = None
    proof_url: str | None = Field(
        default=None,
        max_length=500,
    )
    display_order: int | None = Field(
        default=None,
        ge=0,
    )
    is_visible: bool | None = None


class AchievementResponse(AchievementBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# -------------------------------------------------
# Certification
# -------------------------------------------------

class CertificationBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=250,
    )
    issuer: str = Field(
        min_length=2,
        max_length=200,
    )
    issue_date: date | None = None
    expiration_date: date | None = None
    credential_id: str | None = Field(
        default=None,
        max_length=200,
    )
    credential_url: str | None = Field(
        default=None,
        max_length=500,
    )
    description: str | None = None
    display_order: int = Field(
        default=0,
        ge=0,
    )
    is_visible: bool = True


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=250,
    )
    issuer: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )
    issue_date: date | None = None
    expiration_date: date | None = None
    credential_id: str | None = Field(
        default=None,
        max_length=200,
    )
    credential_url: str | None = Field(
        default=None,
        max_length=500,
    )
    description: str | None = None
    display_order: int | None = Field(
        default=None,
        ge=0,
    )
    is_visible: bool | None = None


class CertificationResponse(CertificationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )