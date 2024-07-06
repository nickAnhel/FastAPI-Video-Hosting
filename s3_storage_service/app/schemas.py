from pydantic import BaseModel


class FilenameSchema(BaseModel):
    filename: str
