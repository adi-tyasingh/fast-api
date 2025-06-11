from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    description: str | None


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    description: str | None = None
