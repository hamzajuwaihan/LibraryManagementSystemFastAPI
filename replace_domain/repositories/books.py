from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.engine import Connection
from sqlalchemy.dialects.postgresql import insert
from replace_domain.infra.db.schema import books, library_users
from replace_domain.exceptions import (
    BookIsNotBorrowedError,
    BookNotFoundError,
    UserNotAssociatedWithLibraryError,
)
from replace_domain.repositories.authors import get as get_author
from replace_domain.repositories.libraries import get as get_library


@dataclass
class Books:
    id: UUID
    name: str
    author_id: UUID
    borrowed_by: UUID
    is_borrowed: bool
    library_id: UUID
    created_at: datetime
    updated_at: datetime


def get(id: UUID, conn: Connection) -> Books:
    """
    Retrieve a single book by its ID.
    """
    if book := conn.execute(books.select().where(books.c.id == id)).first():
        return Books(**book._asdict())
    else:
        raise BookNotFoundError(id)


def get_all(conn: Connection) -> list[Books]:
    """
    Retrieve all books from the database.
    """
    return [
        Books(**book) for book in conn.execute(books.select()).mappings().fetchall()
    ]


def delete(id: UUID, conn: Connection) -> None:
    """
    Delete a book by its ID.
    """
    book = get(id, conn)
    conn.execute(books.delete().where(books.c.id == book.id))


def new(name: str, author_id: UUID, library_id: UUID, conn: Connection) -> Books:
    """
    Create a new book in the database.
    """
    author = get_author(author_id, conn)

    library = get_library(library_id, conn)

    default_retry_map = (
        conn.execute(
            insert(books)
            .values(name=name, author_id=author.id, library_id=library.id)
            .returning(books)
        )
        .mappings()
        .one()
    )

    return Books(**default_retry_map)


def borrow(book_id: UUID, user_id: UUID, conn: Connection) -> Books:
    """
    Borrow a book by a user. The user must be associated with the book's library.
    """
    # Retrieve the book details
    book = get(book_id, conn)

    # Check if the user is associated with the book's library
    is_user_in_library = conn.execute(
        select(library_users.c.user_id).where(  # Correct way to select a single column
            library_users.c.user_id == user_id,
            library_users.c.library_id == book.library_id,
        )
    ).first()

    if not is_user_in_library:
        raise UserNotAssociatedWithLibraryError(user_id, book.library_id)

    # Mark the book as borrowed by the user
    conn.execute(
        books.update()
        .where(books.c.id == book_id)
        .values(borrowed_by=user_id, is_borrowed=True)
    )

    # Return the updated book details
    return get(book_id, conn)


def unborrow(book_id: UUID, conn: Connection):
    """
    Unborrow the provided book.
    """
    # Retrieve the book details
    book = get(book_id, conn)

    # Check if the book is borrowed
    if not book.is_borrowed:
        # Raise an exception if the book is not currently borrowed
        raise BookIsNotBorrowedError(book_id)

    # Update the book status to unborrowed
    conn.execute(
        books.update()
        .where(books.c.id == book_id)
        .values(borrowed_by=None, is_borrowed=False)
    )

    # Return the updated book details
    return get(book_id, conn)
