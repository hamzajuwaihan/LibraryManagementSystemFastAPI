from pydantic import BaseModel


class AuthorRequestBody(BaseModel):
    name: str
