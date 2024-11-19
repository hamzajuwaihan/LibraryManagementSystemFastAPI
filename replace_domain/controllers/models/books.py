from uuid import UUID
from pydantic import BaseModel


class BookRequestBody(BaseModel):
    name: str
    library_id: UUID
    author_id: UUID
