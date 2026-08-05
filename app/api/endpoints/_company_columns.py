import time

from google.cloud import bigquery

from app.core.cache import get_cached_rows
from app.core.database import qualified_table, run_query

EMPLOYER_PROFILE_COLUMNS = """
    employer_id,
    group_id,
    nob_id,
    cif,
    employer_name,
    employer_code,
    industry,
    tiering_code,
    tiering_label,
    group_name,
    primary_email,
    primary_contact_no,
    snapshot_date
"""

EMPLOYER_ACCOUNT_COLUMNS = """
    account_id,
    cif,
    employer_id,
    employer_name,
    group_id,
    group_name,
    branch_code,
    branch_name,
    branch_address_detail,
    branch_address_village_district,
    branch_address_city,
    branch_address_province,
    branch_telephone,
    branch_email,
    account_number,
    currency,
    product_code,
    is_sharia,
    snapshot_date
"""

STAKEHOLDER_COLUMNS = """
    stakeholder_id,
    cif,
    employer_id,
    employer_name,
    group_id,
    group_name,
    stock_code,
    industry,
    shareholder_type,
    stakeholder_name,
    ownership_amount,
    ownership_percentage,
    designation,
    snapshot_date
"""

ADDRESS_COLUMNS = """
    address_id,
    employer_id,
    cif,
    postcode_id,
    postcode,
    is_primary,
    rt,
    rw,
    address_detail,
    subdistrict,
    district,
    city,
    province,
    snapshot_date
"""


async def get_employer_page(
    client: bigquery.Client, name: str | None, page: int, page_size: int
) -> tuple[list[dict], int]:
    """Query 1 halaman gold_employer_profile langsung dari BigQuery (LIMIT/OFFSET di SQL,
    bukan tarik semua baris terus dipotong di Python - itu yang bikin lemot di 800rb baris).

    Belum ada Postgres/VM di production, jadi sementara balik baca BigQuery langsung.
    Cache-nya PER KOMBINASI (name, page, page_size), TTL settings.cache_ttl_seconds.
    page/page_size udah divalidasi jadi int sama FastAPI Query(ge=..., le=...) di router,
    aman diinterpolasi langsung ke LIMIT/OFFSET tanpa perlu parameter.
    """
    cache_key = f"lov:company:employers:name={name or ''}:page={page}:size={page_size}"

    async def _fetch() -> dict:
        where_clause = ""
        params: list[bigquery.ScalarQueryParameter] = []
        if name:
            where_clause = "WHERE LOWER(employer_name) LIKE LOWER(@name)"
            params.append(bigquery.ScalarQueryParameter("name", "STRING", f"%{name}%"))

        count_rows = await run_query(
            client,
            f"SELECT COUNT(*) AS total FROM {qualified_table('gold_employer_profile')} {where_clause}",
            params,
        )
        total = count_rows[0]["total"]

        offset = (page - 1) * page_size
        rows = await run_query(
            client,
            f"""
            SELECT {EMPLOYER_PROFILE_COLUMNS}
            FROM {qualified_table('gold_employer_profile')}
            {where_clause}
            ORDER BY employer_name
            LIMIT {page_size} OFFSET {offset}
            """,
            params,
        )
        return {"rows": rows, "total": total}

    result = await get_cached_rows(cache_key, _fetch)
    return result["rows"], result["total"]


async def search_employers_by_name(client: bigquery.Client, name: str) -> list[dict]:
    """Pure BigQuery, no Redis cache - BQ sudah punya caching sendiri per service account."""
    rows = await run_query(
        client,
        f"""
        SELECT {EMPLOYER_PROFILE_COLUMNS}
        FROM {qualified_table('gold_employer_profile')}
        WHERE LOWER(employer_name) LIKE LOWER(@name)
        ORDER BY employer_name
        """,
        [bigquery.ScalarQueryParameter("name", "STRING", f"%{name}%")],
    )
    return rows

async def get_employer_by_cif(client: bigquery.Client, cif: str) -> list[dict]:
    cache_key = f"lov:company:employer:cif={cif}"

    async def _fetch() -> list[dict]:
        return await run_query(
            client,
            f"SELECT {EMPLOYER_PROFILE_COLUMNS} FROM {qualified_table('gold_employer_profile')} WHERE cif = @cif",
            [bigquery.ScalarQueryParameter("cif", "STRING", cif)],
        )

    return await get_cached_rows(cache_key, _fetch)


async def get_employer_by_employer_id(client: bigquery.Client, employer_id: str) -> list[dict]:
    cache_key = f"lov:company:employer:employer_id={employer_id}"
    start_time = time.time()
    async def _fetch() -> list[dict]:
        return await run_query(
            client,
            f"""
            SELECT {EMPLOYER_PROFILE_COLUMNS}
            FROM {qualified_table('gold_employer_profile')}
            WHERE employer_id = @employer_id
            """,
            [bigquery.ScalarQueryParameter("employer_id", "STRING", employer_id)],
        )
    end_time = time.time() - start_time
    print(f"get_employer_by_employer_id took {end_time:.8f} seconds")

    return await get_cached_rows(cache_key, _fetch)