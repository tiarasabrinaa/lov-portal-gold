import psycopg
from psycopg.rows import dict_row

from app.core.config import settings


def _conninfo() -> str:
    return (
        f"host={settings.postgres_host} port={settings.postgres_port} "
        f"dbname={settings.postgres_db} user={settings.postgres_user} "
        f"password={settings.postgres_password}"
    )


async def run_pg_query(sql: str, params: dict | tuple | None = None) -> list[dict]:
    """Query Postgres (transactional copy of BigQuery, disinkronin lewat sync job bulanan).

    Buka 1 koneksi baru tiap panggilan - cukup buat volume traffic sekarang.
    Kalau traffic-nya udah gede, ganti ke connection pool (psycopg_pool).
    """
    async with await psycopg.AsyncConnection.connect(_conninfo(), row_factory=dict_row) as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql, params)
            rows = await cur.fetchall()
            return list(rows)
