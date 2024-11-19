import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from replace_domain.infra.db.engine import metadata

authors = sa.Table(
    "authors",
    metadata,
    sa.Column(
        "id",
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        server_default=sa.func.uuid_generate_v4(),
    ),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
)

libraries = sa.Table(
    "libraries",
    metadata,
    sa.Column(
        "id",
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        server_default=sa.func.uuid_generate_v4(),
    ),
    sa.Column("name", sa.String, nullable=False, unique=True),
    sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
)

books = sa.Table(
    "books",
    metadata,
    sa.Column(
        "id",
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        server_default=sa.func.uuid_generate_v4(),
    ),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("author_id", UUID(as_uuid=True), nullable=False),
    sa.Column("borrowed_by", UUID(as_uuid=True), nullable=True),
    sa.Column("is_borrowed", sa.Boolean, default=False),
    sa.Column("library_id", UUID(as_uuid=True), nullable=False),
    sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    sa.ForeignKeyConstraint(
        ["author_id"], ["authors.id"], name="books_author_id_authors_id_fk"
    ),
    sa.ForeignKeyConstraint(
        ["borrowed_by"], ["users.id"], name="books_borrowed_by_users_id_fk"
    ),
    sa.ForeignKeyConstraint(
        ["library_id"], ["libraries.id"], name="books_library_id_libraries_id_fk"
    ),
)

users = sa.Table(
    "users",
    metadata,
    sa.Column(
        "id",
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        server_default=sa.func.uuid_generate_v4(),
    ),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("email", sa.String, nullable=False, unique=True, index=True),
    sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
)

library_users = sa.Table(
    "library_users",
    metadata,
    sa.Column("user_id", UUID(as_uuid=True), nullable=False),
    sa.Column("library_id", UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(
        ["user_id"], ["users.id"], name="library_users_user_id_users_id_fk"
    ),
    sa.ForeignKeyConstraint(
        ["library_id"],
        ["libraries.id"],
        name="library_users_library_id_libraries_id_fk",
    ),
    sa.PrimaryKeyConstraint("user_id", "library_id"),
)
