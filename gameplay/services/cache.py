import asyncio
import builtins
import os
import sys
from collections.abc import Iterable
from typing import Any, get_origin

import msgspec
import orjson
from redis.asyncio.client import Redis

from .logger import get_logger

__all__ = ("Cache",)

logger = get_logger("cache")


class Cache:
    def __init__(self, app) -> None:
        self.app = app

        self.loop = asyncio.get_running_loop()

        self.redis: Redis

    async def connect(self) -> None:
        if not hasattr(self, "redis"):
            url = os.getenv(key="REDIS_URL", default=None)
            if url is None:
                logger.error("REDIS_URL environment variable is not set.")
                sys.exit(1)

            self.redis = Redis.from_url(
                url,
                decode_responses=False,
                health_check_interval=60,
                retry_on_timeout=True,
            )
            await self.redis.ping()  # type: ignore
            logger.info("Cache connected successfully.")

    async def close(self) -> None:
        if hasattr(self, "redis"):
            await self.redis.connection_pool.disconnect()
            await self.redis.close()

        logger.info("Cache connection closed.")

    async def set(self, *path: Any, model: msgspec.Struct | dict[str, Any], **kwargs: Any) -> None:
        """Set a value in the cache."""
        key = ":".join(map(str, path))

        if isinstance(model, msgspec.Struct):
            data = msgspec.json.encode(model)
        else:
            data = orjson.dumps(model)

        await self.redis.set(key, data, ex=kwargs.pop("ex", 300), **kwargs)
        logger.debug(f"Set cache for key: {key!r}")

    async def get[T: msgspec.Struct | dict[str, Any]](
        self, *path: Any, model_cls: type[T], **kwargs: Any
    ) -> T | None:
        """Get a value from the cache."""
        key = ":".join(map(str, path))
        data = await self.redis.get(key, **kwargs)

        if data is None:
            logger.debug(f"Cache miss for key: {key!r}")
            return None

        if isinstance(model_cls, type) and issubclass(model_cls, msgspec.Struct):
            return msgspec.json.decode(data, type=model_cls)
        else:
            return orjson.loads(data)

    async def delete(self, *path: str) -> None:
        """Delete a value from the cache."""
        key = ":".join(map(str, path))

        await self.redis.delete(key)
        logger.debug(f"Deleted cache for key: {key!r}")

    async def hash_set(
        self,
        *path: Any,
        model: msgspec.Struct | dict[str, Any],
        keys: Iterable[str],
        **kwargs: Any,
    ) -> None:
        """Set a value in a hash in the cache."""
        name = ":".join(map(str, path))
        data = msgspec.to_builtins(model) if isinstance(model, msgspec.Struct) else model

        async with self.redis.pipeline() as pipe:
            await pipe.hset(
                name, mapping={k: orjson.dumps(v).decode() for k, v in data.items() if k in keys}
            )  # type: ignore
            await pipe.hexpire(name, kwargs.pop("ex", 300), *keys)

            await pipe.execute()

        logger.debug(f"Set hash cache for key: {name!r}")

    async def hash_get[T: msgspec.Struct | dict[str, Any]](
        self, *path: Any, model_cls: type[T], keys: Iterable[str]
    ) -> tuple[T | None, builtins.set[str]]:
        """Get a value from a hash in the cache."""
        name = ":".join(map(str, path))

        if not await self.redis.exists(name):
            logger.debug(f"Hash cache miss for key: {name!r}")
            return (None, set(keys))

        ordered_keys = sorted(keys)
        data = await self.redis.hmget(name, ordered_keys)  # type: ignore

        mapping: dict[str, Any] = {}
        unretrieved_keys: set[str] = set()

        for key, value in zip(ordered_keys, data, strict=False):
            if value is not None:
                mapping[key] = orjson.loads(value)
            else:
                unretrieved_keys.add(key)

        logger.debug(
            f"Hash cache retrieved for key: {name!r}, keys: {list(mapping.keys())}, unretrieved: {list(unretrieved_keys)}"
        )

        if get_origin(model_cls) is dict:
            return (mapping, unretrieved_keys)  # type: ignore

        elif issubclass(model_cls, msgspec.Struct):
            if unretrieved_keys:
                return (None, unretrieved_keys)

            model = msgspec.convert(mapping, type=model_cls)
            return (model, unretrieved_keys)

        else:
            raise ValueError("model_cls must be a subclass of msgspec.Struct or dict")

    async def hash_del(self, *path: Any, keys: Iterable[str]) -> None:
        """Delete a value from a hash in the cache."""
        name = ":".join(map(str, path))

        await self.redis.hdel(name, *keys)  # type: ignore
        logger.debug(f"Deleted hash cache for key: {name!r}, keys: {list(keys)}")
