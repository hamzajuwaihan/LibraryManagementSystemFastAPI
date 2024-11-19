from pydantic import BaseModel


class LibraryRequestBody(BaseModel):
    name: str
