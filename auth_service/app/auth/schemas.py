from uuid import UUID
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    hashed_password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
