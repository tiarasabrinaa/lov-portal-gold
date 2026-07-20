import asyncio
import os
from collections.abc import AsyncGenerator
from functools import lru_cache

from google.cloud import bigquery

from app.core.config import settings


@lru_cache
def get_bq_client() -> bigquery.Client:
    if settings.google_application_credentials:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
    return bigquery.Client(project=settings.bigquery_project, location=settings.bigquery_location)


async def get_db() -> AsyncGenerator[bigquery.Client, None]:
    yield get_bq_client()


def qualified_table(table_name: str) -> str:
    return f"`{settings.bigquery_project}.{settings.bigquery_dataset}.{table_name}`"


async def run_query(
    client: bigquery.Client,
    sql: str,
    params: list[bigquery.ScalarQueryParameter] | None = None,
) -> list[dict]:
    job_config = bigquery.QueryJobConfig(query_parameters=params or [])

    def _execute() -> list[dict]:
        rows = client.query(sql, job_config=job_config).result()
        return [dict(row.items()) for row in rows]

    return await asyncio.to_thread(_execute)
