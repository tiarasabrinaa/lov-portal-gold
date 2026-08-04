import asyncio
import json
import logging
from collections.abc import Awaitable, Callable
from datetime import date
from decimal import Decimal
from functools import lru_cache
from typing import TypeVar

import redis.asyncio as redis

from app.core.config import settings

logger = logging.getLogger(__name__)

_REDIS_TIMEOUT_SECONDS = 1.0


@lru_cache
def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        password=settings.redis_password,
        decode_responses=True,
        socket_connect_timeout=_REDIS_TIMEOUT_SECONDS,
        socket_timeout=_REDIS_TIMEOUT_SECONDS,
    )


def _json_default(value: object) -> str | float:
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    raise TypeError(f"Not JSON serializable: {value!r}")


T = TypeVar("T")


async def get_cached_rows(
    cache_key: str,
    fetch: Callable[[], Awaitable[T]],
) -> T:
    """Return a JSON-serializable value from Redis if cached, otherwise call `fetch` and cache it.

    Sengaja ga terikat ke sumber data manapun (BigQuery/Postgres/dll) -
    caller yang nentuin gimana caranya ambil data lewat `fetch`. Redis di
    sini cuma optimisasi, bukan dependency wajib - kalau Redis ga kereach
    (mis. Cloud Run tanpa Redis nempel), fallback diam-diam ke `fetch()`
    tanpa cache, bukan 500.
    """
    r = get_redis_client()

    try:
        cached = await asyncio.wait_for(r.get(cache_key), timeout=_REDIS_TIMEOUT_SECONDS)
    except (redis.RedisError, TimeoutError, OSError) as exc:
        logger.warning("Redis GET gagal (%s), fallback tanpa cache", exc)
        cached = None

    if cached is not None:
        return json.loads(cached)

    rows = await fetch()

    try:
        await asyncio.wait_for(
            r.set(cache_key, json.dumps(rows, default=_json_default), ex=settings.cache_ttl_seconds),
            timeout=_REDIS_TIMEOUT_SECONDS,
        )
    except (redis.RedisError, TimeoutError, OSError) as exc:
        logger.warning("Redis SET gagal (%s), lanjut tanpa cache", exc)

    return rows