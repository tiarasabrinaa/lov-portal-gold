import asyncio
import json
import logging
from datetime import date
from decimal import Decimal
from functools import lru_cache

import redis.asyncio as redis
from google.cloud import bigquery

from app.core.config import settings
from app.core.database import run_query

logger = logging.getLogger(__name__)

_REDIS_TIMEOUT_SECONDS = 1.0


    @lru_cache
def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
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


async def get_cached_rows(
    cache_key: str,
    client: bigquery.Client,
    sql: str,
    params: list[bigquery.ScalarQueryParameter] | None = None,
) -> list[dict]:
    """Return query rows from Redis if cached, otherwise query BigQuery and cache the result.

    Redis di sini cuma optimisasi, bukan dependency wajib - kalau Redis ga
    kereach (mis. Cloud Run tanpa Redis nempel), fallback diam-diam ke
    BigQuery langsung tiap request, bukan 500.
    """
    r = get_redis_client()

    try:
        cached = await asyncio.wait_for(r.get(cache_key), timeout=_REDIS_TIMEOUT_SECONDS)
    except (redis.RedisError, TimeoutError, OSError) as exc:
        logger.warning("Redis GET gagal (%s), fallback ke BigQuery tanpa cache", exc)
        cached = None

    if cached is not None:
        return json.loads(cached)

    rows = await run_query(client, sql, params)

    try:
        await asyncio.wait_for(
            r.set(cache_key, json.dumps(rows, default=_json_default), ex=settings.cache_ttl_seconds),
            timeout=_REDIS_TIMEOUT_SECONDS,
        )
    except (redis.RedisError, TimeoutError, OSError) as exc:
        logger.warning("Redis SET gagal (%s), lanjut tanpa cache", exc)

    return rows
