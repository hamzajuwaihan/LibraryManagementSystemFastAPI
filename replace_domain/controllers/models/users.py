from pydantic import BaseModel


class UserRequestBody(BaseModel):
    name: str
    email: str
