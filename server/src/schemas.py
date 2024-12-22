from pydantic import BaseModel, ConfigDict, EmailStr


class Status(BaseModel):
    success: bool = True
    detail: str = "Request processed successfully"


class Email(BaseModel):
    email: EmailStr
    subject: str
    content: str
    type: str = "email"


class Telegram(BaseModel):
    chat_id: int
    content: str
    preview_url: str
    type: str = "telegram"


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
