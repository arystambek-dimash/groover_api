from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from src.adapters.database.config import Base
from src.main.web import settings
from src.adapters.database.models import *

# Alembic Config object
config = context.config

# Modify the URL to use psycopg2 for synchronous migration
sync_db_uri = settings.db.db_uri.replace('asyncpg', 'psycopg2')
config.set_main_option('sqlalchemy.url', sync_db_uri)

# Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata object for 'autogenerate'
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
