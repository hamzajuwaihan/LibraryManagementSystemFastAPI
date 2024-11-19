from fastapi import APIRouter, HTTPException, status, Request
from uuid import UUID
from replace_domain.controllers.models.users import UserRequestBody
from replace_domain.exceptions import EmailAlreadyExistsError, UserNotFoundError
from replace_domain.repositories.users import get, get_all, delete, new, Users
from typing import List
from replace_domain.infra.db.engine import engine


users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@users_router.get("/", response_model=List[Users])
async def get_all_users(r: Request):
    """
    Get all users from the database.
    """
    with engine.connect() as conn:
        users = get_all(conn)
    return users


@users_router.get("/{user_id}", response_model=Users)
async def get_user(user_id: UUID):
    """
    Get a single user by its ID.
    """
    try:
        with engine.connect() as conn:
            user = get(user_id, conn)
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@users_router.post("/", response_model=Users)
async def create_user(user: UserRequestBody):
    """
    Create a new user.
    """
    try:
        with engine.begin() as conn:
            return new(name=user.name, email=user.email, conn=conn)
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID):
    """
    Delete a user by its ID.
    """
    try:
        with engine.begin() as conn:
            delete(user_id, conn)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
