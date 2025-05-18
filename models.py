from pydantic import BaseModel, Field
from typing import Optional

from db import BookRepository


class BookBase(BaseModel):
    title: str
    author: str
    year: int
    genre: str
    pages: int
    availability: bool = True


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    year: Optional[int]
    genre: Optional[str]
    pages: Optional[int]
    availability: Optional[bool] = None


class Book(BookBase):
    id: int

