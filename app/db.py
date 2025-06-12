import os
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import URL, String
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv("../.env")

url_object = URL.create(
    "postgresql+asyncpg",
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    port=int(os.getenv("PORT")),  # Convert port to integer
    database=os.getenv("DB"),
)

engine = create_async_engine(url_object, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]]
