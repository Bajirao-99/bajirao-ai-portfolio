from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int


class AdminResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    last_login: datetime | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )