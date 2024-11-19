from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from replace_domain.exceptions import LibraryNotFoundError
from sqlalchemy import Connection
from sqlalchemy.dialects.postgresql import insert
from replace_domain.infra.db.schema import libraries, library_users, users
from replace_domain.repositories.users import Users, get as get_user


@dataclass
class Libraries:
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    users: list[Users]


def get(id: UUID, conn: Connection) -> Libraries:
    """
    Retrieve a single library by its ID, including its associated users.
    """
    library_data = conn.execute(libraries.select().where(libraries.c.id == id)).first()
    if not library_data:
        raise LibraryNotFoundError(id)

    library = Libraries(**library_data._asdict(), users=[])
    users_data = conn.execute(
        users.select()
        .join(library_users, library_users.c.user_id == users.c.id)
        .where(library_users.c.library_id == id)
    ).fetchall()

    library.users = [Users(**user._asdict()) for user in users_data]
    return library


def get_all(conn: Connection) -> list[Libraries]:
    """
    Retrieve all libraries from the database, including their associated users.
    """
    libraries_data = conn.execute(libraries.select()).fetchall()
    libraries_list = []

    for library_data in libraries_data:
        library = Libraries(**library_data._asdict(), users=[])
        users_data = conn.execute(
            users.select()
            .join(library_users, library_users.c.user_id == users.c.id)
            .where(library_users.c.library_id == library.id)
        ).fetchall()
        library.users = [Users(**user._asdict()) for user in users_data]
        libraries_list.append(library)

    return libraries_list


def delete(id: UUID, conn: Connection) -> None:
    """
    Delete a library by its ID.
    """
    library = get(id, conn)

    conn.execute(libraries.delete().where(libraries.c.id == library.id))


def new(name: str, conn: Connection) -> Libraries:
    """
    Create a new library in the database.
    """
    default_retry_map = (
        conn.execute(
            insert(libraries)
            .values(
                name=name,
            )
            .returning(libraries)
        )
        .mappings()
        .one()
    )
    return Libraries(**default_retry_map, users=[])


def add_user_to_library(user_id: UUID, library_id: UUID, conn: Connection) -> None:
    """
    Add a user to a library by inserting a record into the library_users table.
    """
    library = get(library_id, conn)
    user = get_user(user_id, conn)

    conn.execute(insert(library_users).values(user_id=user.id, library_id=library.id))
