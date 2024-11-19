from fastapi import APIRouter, HTTPException, status, Request
from uuid import UUID
from replace_domain.controllers.models.users import UserRequestBody, UserUpdateRequest
from replace_domain.exceptions import EmailAlreadyExistsError
from replace_domain.repositories.users import get, get_all, delete, new, patch, Users
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
    with engine.connect() as conn:
        user = get(user_id, conn)
    return user



@users_router.post("/", response_model=Users, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserRequestBody):
    """
    Create a new user.
    """
    try:
        with engine.begin() as conn:
            return new(name=user.name, email=user.email, conn=conn)
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID):
    """
    Delete a user by its ID.
    """
    with engine.begin() as conn:
        delete(user_id, conn)

@users_router.patch("/{user_id}", response_model=Users)
async def update_user(user_id: UUID, user: UserUpdateRequest):
    """
    Update a user's details.
    """
    with engine.begin() as conn:
        try:
            updated_user = patch(user_id, user.model_dump(exclude_unset=True), conn)
            return updated_user
        except EmailAlreadyExistsError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))