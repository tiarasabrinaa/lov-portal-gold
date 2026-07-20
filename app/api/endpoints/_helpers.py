from collections.abc import Sequence

from google.cloud import bigquery
from pydantic import BaseModel

from app.core.database import run_query


async def fetch_all(
    client: bigquery.Client,
    sql: str,
    schema: type[BaseModel],
    params: list[bigquery.ScalarQueryParameter] | None = None,
) -> list[BaseModel]:
    rows = await run_query(client, sql, params)
    return [schema(**row) for row in rows]


def order_by_or_default(columns: Sequence[str]) -> str:
    return ", ".join(columns)
