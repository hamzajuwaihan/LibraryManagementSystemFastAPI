from fastapi import APIRouter, status, Request
from uuid import UUID
from replace_domain.controllers.models.libraries import LibraryRequestBody
from replace_domain.repositories.libraries import (
    add_user_to_library,
    get,
    get_all,
    delete,
    new,
    Libraries,
)
from typing import List
from replace_domain.infra.db.engine import engine


libraries_router = APIRouter(
    prefix="/libraries",
    tags=["Libraries"],
)


@libraries_router.get("/", response_model=List[Libraries])
async def get_all_libraries(r: Request):
    """
    Get all libraries from the database.
    """
    with engine.connect() as conn:
        libraries = get_all(conn)
    return libraries


@libraries_router.get("/{library_id}", response_model=Libraries)
async def get_library(library_id: UUID):
    """
    Get a single library by its ID.
    """
    with engine.connect() as conn:
        library = get(library_id, conn)
    return library



@libraries_router.post("/", response_model=Libraries)
async def create_library(library: LibraryRequestBody):
    """
    Create a new library.
    """
    with engine.begin() as conn:
        return new(name=library.name, conn=conn)


@libraries_router.delete("/{library_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_library(library_id: UUID):
    """
    Delete a library by its ID.
    """
    with engine.begin() as conn:
        delete(library_id, conn)



@libraries_router.post(
    "/{library_id}/add_user/{user_id}", status_code=status.HTTP_200_OK
)
async def add_user_to_library_endpoint(library_id: UUID, user_id: UUID):
    """
    Add a user to a library.
    """
    with engine.begin() as conn:
        add_user_to_library(user_id, library_id, conn)
    return {"message": "User added to the library"}
