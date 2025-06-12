import crud
from dependencies import SessionDep
from fastapi import APIRouter
from schemas import BookCreate, BookUpdate

router = APIRouter()


@router.post("/books")
async def add_book(book: BookCreate, session: SessionDep):
    """route to add a book"""
    return await crud.create_book(session, book)


@router.get("/books")
async def get_books(session: SessionDep):
    """route to get a list of all books"""
    return await crud.get_all_books(session)


@router.get("/book/{id}")
async def get_book(id: int, session: SessionDep):
    """route to get an individual book"""
    return await crud.get_book_by_id(session, id)


@router.post("/book/{id}")
async def update_book(id: int, update: BookUpdate, session: SessionDep):
    """Route to allow for updation of a book"""
    return await crud.update_book(session, id, update)


@router.delete("/book/{id}")
async def delete_book(id: int, session: SessionDep):
    """route to delete a specific book through the book id"""
    return await crud.delete_book(session, id)
