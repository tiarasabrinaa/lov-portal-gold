from collections.abc import Sequence

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_all(session: AsyncSession, sql: str, schema: type[BaseModel]) -> list[BaseModel]:
    result = await session.execute(text(sql))
    return [schema(**row) for row in result.mappings().all()]


def order_by_or_default(columns: Sequence[str]) -> str:
    return ", ".join(columns)