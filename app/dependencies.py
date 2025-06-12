from typing import Annotated

from db import async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session():
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
