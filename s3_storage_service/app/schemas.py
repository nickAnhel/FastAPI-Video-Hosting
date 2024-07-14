from pydantic import BaseModel


class FilenameSchema(BaseModel):
    filename: str


class FilenamesSchema(BaseModel):
    filenames: list[str]
