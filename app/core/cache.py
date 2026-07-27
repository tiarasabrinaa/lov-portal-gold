import json
from datetime import date
from decimal import Decimal
from functools import lru_cache

import redis.asyncio as redis
from google.cloud import bigquery

from app.core.config import settings
from app.core.database import run_query


@lru_cache
def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True,
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
    """Return query rows from Redis if cached, otherwise query BigQuery and cache the result."""
    r = get_redis_client()
    cached = await r.get(cache_key)
    if cached is not None:
        return json.loads(cached)

    rows = await run_query(client, sql, params)
    await r.set(cache_key, json.dumps(rows, default=_json_default), ex=settings.cache_ttl_seconds)
    return rows
