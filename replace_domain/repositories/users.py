from dataclasses import dataclass
from sqlite3 import IntegrityError
from uuid import UUID
from datetime import datetime
from sqlalchemy.engine import Connection
from sqlalchemy.dialects.postgresql import insert
from replace_domain.infra.db.schema import users
from replace_domain.exceptions import EmailAlreadyExistsError, UserNotFoundError


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
        raise UserNotFoundError(id)


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
        default_retry_map = (
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
        return Users(**default_retry_map)
    except IntegrityError as e:
        if hasattr(e.orig, "pgcode") and e.orig.pgcode == "23505":
            if "ix_users_email" in str(e.orig):
                raise EmailAlreadyExistsError(email)
        raise e
