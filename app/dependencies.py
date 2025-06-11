from db import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends


async def get_session():
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
