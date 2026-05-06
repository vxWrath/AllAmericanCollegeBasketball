import datetime
import os
import sys
from typing import Any

import asyncpg
import orjson

from .cache import Cache
from .logger import get_logger

logger = get_logger("database")


# Dict-like encoders/decoders
def _dumps(obj: Any) -> str:
    return orjson.dumps(obj).decode("utf-8")


def _loads(obj: Any) -> Any:
    # asyncpg returns empty jsonb as the string `"{}"` (with surrounding quotes),
    # which orjson cannot parse — treat it as an empty dict instead
    if obj == '"{}"':
        return {}
    return orjson.loads(obj)


# Datetime handling for timestamptz columns (PostgreSQL sends these as ISO strings)
def _datetime_encoder(dt: str | datetime.datetime) -> str:
    if isinstance(dt, datetime.datetime):
        return dt.isoformat()
    return dt


def _datetime_decoder(dt_str: str) -> datetime.datetime:
    fixed = dt_str.replace("T", " ").replace("Z", "+00:00")
    return datetime.datetime.fromisoformat(fixed)


async def _pg_init(connection: asyncpg.Connection) -> None:
    await connection.set_type_codec(
        "jsonb",
        encoder=_dumps,
        decoder=_loads,
        schema="pg_catalog",
        format="text",
    )
    await connection.set_type_codec(
        "timestamptz",
        encoder=_datetime_encoder,
        decoder=_datetime_decoder,
        schema="pg_catalog",
        format="text",
    )


class Database:
    def __init__(self, cache: Cache) -> None:
        self.pool: asyncpg.Pool
        self.cache = cache

    async def connect(self) -> None:
        dsn = os.getenv(key="DATABASE_URL", default=None)
        if dsn is None:
            logger.error("DATABASE_URL environment variable is not set.")
            sys.exit(1)

        self.pool = await asyncpg.create_pool(
            dsn=dsn,
            init=_pg_init,
        )

        if not hasattr(self.cache, "redis"):
            raise RuntimeError("Cache must be connected before connecting to the database.")

        logger.info("Database connected successfully.")

    async def close(self) -> None:
        if hasattr(self, "pool"):
            await self.pool.close()

        logger.info("Database connection closed.")
