from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import update
from replace_domain.infra.db.schema import users
from replace_domain.exceptions import EmailAlreadyExistsError, ModelNotFoundError


@dataclass
class Users:
    id: UUID
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


def get(id: UUID, conn: Connection) -> Users:
    """
    Retrieve a single user by its ID.
    """
    if user := conn.execute(users.select().where(users.c.id == id)).first():
        return Users(**user._asdict())
    else:
        raise ModelNotFoundError(Users, id)


def get_all(conn: Connection) -> list[Users]:
    """
    Retrieve all users from the database.
    """
    return [
        Users(**user) for user in conn.execute(users.select()).mappings().fetchall()
    ]


def delete(id: UUID, conn: Connection) -> None:
    """
    Delete a user by its ID.
    """
    user = get(id, conn)

    conn.execute(users.delete().where(user.c.id == user.id))


def new(name: str, email: str, conn: Connection) -> Users:
    """
    Create a new user in the database.
    """
    try:
        user_data = (
            conn.execute(
                insert(users)
                .values(
                    name=name,
                    email=email,
                )
                .returning(users)
            )
            .mappings()
            .one()
        )
        return Users(**user_data)
    except IntegrityError:
        raise EmailAlreadyExistsError(email)


def patch(user_id: UUID, update_data: dict, conn: Connection) -> Users:
    """
    Update a user's details in the database.
    """
    user = get(user_id, conn)  # Ensure the user exists

    try:
        updated_data = (
            conn.execute(
                update(users)
                .where(users.c.id == user.id)
                .values(**update_data)
                .returning(users)
            )
            .mappings()
            .one()
        )
        return Users(**updated_data)
    except IntegrityError:
        if "email" in update_data:
            raise EmailAlreadyExistsError(update_data["email"])
        raise
