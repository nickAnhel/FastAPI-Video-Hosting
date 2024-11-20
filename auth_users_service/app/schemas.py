from pydantic import BaseModel


class Status(BaseModel):
    success: bool = True
    detail: str = "Request processed successfully"
