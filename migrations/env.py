import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from migrations.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Pull database URL from the environment — never hardcode credentials.
# Docker Compose sets ALEMBIC_DATABASE_URL to the psycopg2 variant; the app
# uses DATABASE_URL with asyncpg. Keeping them separate avoids driver string
# manipulation at runtime.
config.set_main_option("sqlalchemy.url", os.environ["ALEMBIC_DATABASE_URL"])

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
