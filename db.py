from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped 
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from fastapi import Depends

db_string = 'postgresql+asyncpg://admin:pass@localhost:5432/bv'

engine = create_async_engine(db_string, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs , DeclarativeBase):
    pass

class Book(Base):
    __tablename__='books'
    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(String(100))
    author : Mapped[str] = mapped_column(String(100))
    description : Mapped[Optional[str]]
        
async def get_session():
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
