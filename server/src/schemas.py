from pydantic import BaseModel, ConfigDict


class Status(BaseModel):
    success: bool = True
    detail: str = "Request processed successfully"


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
