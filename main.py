from fastapi import FastAPI, HTTPException
from db import Base, engine, Book, SessionDep
from schemas import BookCreate, BookUpdate
from sqlalchemy import select
from contextlib import asynccontextmanager

#lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post('/books')
async def add_book(book: BookCreate, session: SessionDep):
    nb = Book(title=book.title, author=book.author, description=book.description)
    session.add(nb)
    await session.commit()
    await session.refresh(nb)   
    return nb


@app.get('/books')
async def get_books(session: SessionDep):
    res = await session.execute(select(Book))
    books = res.scalars().all()
    return books


@app.get('/book/{id}')
async def get_book(id: int, session: SessionDep):
    res = await session.get(Book, id)
    return res


@app.post('/book/{id}')
async def update_book(id:int, update: BookUpdate, session: SessionDep):
    res = await session.get(Book, id)

    if not res:
        raise HTTPException(status_code=404, detail='Does that book exist?')
    
    if update.author:
        res.author = update.author
    if update.description:
        res.description = update.description
    if update.title:
        res.title = update.title
    
    await session.commit()
    return res


@app.delete('/book/{id}')
async def delete_book(id: int, session: SessionDep):
    res = await session.get(Book, id)
    await session.delete(res)
    await session.commit()
    return "book deleted!"