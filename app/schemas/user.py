import re

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)

    @field_validator("password")
    def validate_password(cls, v):
        pattern = r"(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()_+=-])"
        if not re.search(pattern, v):
            raise ValueError(
                "Password must contain at least one digit, one uppercase letter, "
                "one lowercase letter, and one special character."
            )

        return v


class UserInDB(UserBase):
    id: UUID4
    hashed_password: str
    is_active: bool | None = True
    is_admin: bool | None = False

    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBase):
    id: UUID4
    email: EmailStr
    is_active: bool | None = True
    is_admin: bool | None = False
