from fastapi import APIRouter, HTTPException, status, Request
from uuid import UUID
from replace_domain.controllers.models.books import BookRequestBody
from replace_domain.exceptions import (
    BookIsNotBorrowedError,
    UserNotAssociatedWithLibraryError,
)
from replace_domain.repositories.books import (
    borrow,
    get,
    get_all,
    delete,
    new,
    Books,
    unborrow,
)
from typing import List
from replace_domain.infra.db.engine import engine

books_router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@books_router.get("/", response_model=List[Books])
async def get_all_books(r: Request):
    """
    Get all books from the database.
    """
    with engine.connect() as conn:
        books = get_all(conn)
    return books


@books_router.get("/{book_id}", response_model=Books)
async def get_book(book_id: UUID):
    """
    Get a single book by its ID.
    """
    with engine.connect() as conn:
        book = get(book_id, conn)
    return book



@books_router.post("/", response_model=Books)
async def create_book(book: BookRequestBody):
    """
    Create a new book.
    """
    with engine.begin() as conn:
        new_book = new(
            name=book.name,
            author_id=book.author_id,
            library_id=book.library_id,
            conn=conn,
        )
    return new_book



@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    """
    Delete a book by its ID.
    """
    with engine.begin() as conn:
        delete(book_id, conn)



@books_router.post("/{book_id}/borrow/user/{user_id}", status_code=status.HTTP_200_OK)
async def borrow_book(book_id: UUID, user_id: UUID):
    """
    Borrow a book for a user.
    """
    try:
        with engine.begin() as conn:
            book = borrow(book_id, user_id, conn)
        return book
    except UserNotAssociatedWithLibraryError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)



@books_router.post("/{book_id}/unborrow", status_code=status.HTTP_200_OK)
async def unborrow_book(book_id: UUID):
    """
    Unborrow the book if the user is allowed to do so.
    """
    try:
        with engine.begin() as conn:
            book = unborrow(book_id, conn)
        return book
    except BookIsNotBorrowedError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
