from db import Book
from fastapi import HTTPException
from schemas import BookCreate, BookUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_book(session: AsyncSession, book_data: BookCreate) -> Book:
    book = Book(
        title=book_data.title,
        author=book_data.author,
        description=book_data.description,
    )
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


async def get_all_books(session: AsyncSession) -> list[Book]:
    result = await session.execute(select(Book))
    return result.scalars().all()


async def get_book_by_id(session: AsyncSession, book_id: int) -> Book:
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Does that book exist?")
    return book


async def update_book(
    session: AsyncSession, book_id: int, update_data: BookUpdate
) -> Book:
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Does that book exist?")

    if update_data.title:
        book.title = update_data.title
    if update_data.author:
        book.author = update_data.author
    if update_data.description:
        book.description = update_data.description

    await session.commit()
    return book


async def delete_book(session: AsyncSession, book_id: int) -> str:
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Does that book exist?")

    await session.delete(book)
    await session.commit()
    return "book deleted!"
