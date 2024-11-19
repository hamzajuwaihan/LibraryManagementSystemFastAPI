from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from sqlalchemy.engine import Connection
from sqlalchemy.dialects.postgresql import insert
from replace_domain.infra.db.schema import authors
from replace_domain.exceptions import ModelNotFoundError


@dataclass
class Authors:
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime


def get(id: UUID, conn: Connection) -> Authors:
    """
    Get an author from DB by Id.
    """
    if author := conn.execute(authors.select().where(authors.c.id == id)).first():
        return Authors(**author._asdict())
    else:
        raise ModelNotFoundError(Authors, id)


def get_all(conn: Connection) -> list[Authors]:
    """
    Get all authors in DB.
    """
    return [Authors(**author) for author in conn.execute(authors.select()).mappings().fetchall()]


def delete(id: UUID, conn: Connection) -> None:
    """
    Delete Author from DB.
    """
    author = get(id, conn)
    conn.execute(authors.delete().where(authors.c.id == author.id))


def new(name: str, conn: Connection) -> Authors:
    """
    Creates an author in the DB.
    """
    default_retry_map = conn.execute(insert(authors).values(
        name=name,
    ).returning(authors)).mappings().one()
    return Authors(**default_retry_map)
