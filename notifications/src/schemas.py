from pydantic import BaseModel, EmailStr


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
