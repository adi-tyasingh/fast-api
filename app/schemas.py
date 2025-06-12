from typing import Optional

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str
    author: str
    description: str | None


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Updated Title (Not mandatory)")
    author: Optional[str] = Field(None, example="Updated Author Name (Not Mandatory)")
    description: Optional[str] = Field(
        None, example="Updated Description (Not Mandatory)"
    )
