from contextlib import asynccontextmanager

import views
from db import Base, engine
from fastapi import FastAPI


# lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(views.router)
