from pydantic import BaseModel,EmailStr
from typing import Optional


class UserRequestBody(BaseModel):
    name: str
    email: EmailStr

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None