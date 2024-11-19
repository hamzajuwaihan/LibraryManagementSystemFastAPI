from typing import Any
from uuid import UUID
from pydantic import BaseModel


class ResponseError(BaseModel):
    title: str | None
    detail: str | None


class ModelNotFoundError(Exception):
    def __init__(self, model: type[Any], id: UUID | str) -> None:
        self.model = model.__name__
        self.id = id


class EmailAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.message = f"Email '{email}' is already taken."
        super().__init__(self.message)


class UserNotAssociatedWithLibraryError(Exception):
    def __init__(self, user_id: UUID, book_id: UUID):
        self.message = (
            f"User with ID {user_id} is not associated with library of book {book_id}"
        )
        super().__init__(self.message)


class BookIsNotBorrowedError(Exception):
    def __init__(self, book_id: UUID):
        self.message = (
            f"you cannot unborrow a book {book_id} that is not currently borrowed."
        )
        super().__init__(self.message)


class LibraryNameAlreadyTakenError(Exception):
    def __init__(self, name: str):
        self.message = f"{name} name is already taken."
        super().__init__(self.message)
