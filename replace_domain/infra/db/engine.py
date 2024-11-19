import os
import sqlalchemy as sa


def get_db_url() -> str:
    return 'postgresql://%s:%s@%s:%s/%s' % (
        os.getenv('PGUSER', 'postgres'),
        os.getenv('PGPASSWORD', 'password'),
        os.getenv('PGHOST', 'localhost'),
        os.getenv('PGPORT', '5432'),
        os.getenv('PGDATABASE', 'postgres'),
    )


engine = sa.create_engine(get_db_url(), echo_pool=True, pool_pre_ping=True)


metadata = sa.MetaData()
