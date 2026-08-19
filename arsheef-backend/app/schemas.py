from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LinkedAccountOut(BaseModel):
    platform: str
    platform_username: str | None
    is_verified: bool

    class Config:
        from_attributes = True
