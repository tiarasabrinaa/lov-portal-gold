from app.core.cache import get_cached_rows
from app.core.postgres import run_pg_query

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


async def get_employer_page(name: str | None, page: int, page_size: int) -> tuple[list[dict], int]:
    """Query 1 halaman gold_employer_profile langsung dari Postgres (LIMIT/OFFSET di SQL,
    bukan tarik semua baris terus dipotong di Python - itu yang bikin lemot di 800rb baris).

    Cache-nya PER KOMBINASI (name, page, page_size) - bukan 1 cache buat seluruh tabel -
    jadi tiap entry cache-nya kecil (cuma segede 1 halaman), bukan ratusan MB.
    """
    cache_key = f"lov:company:employers:name={name or ''}:page={page}:size={page_size}"

    async def _fetch() -> dict:
        where_clause = ""
        where_params: list = []
        if name:
            where_clause = "WHERE employer_name ILIKE %s"
            where_params.append(f"%{name}%")

        count_rows = await run_pg_query(
            f"SELECT COUNT(*) AS total FROM gold_employer_profile {where_clause}",
            tuple(where_params),
        )
        total = count_rows[0]["total"]

        offset = (page - 1) * page_size
        rows = await run_pg_query(
            f"""
            SELECT {EMPLOYER_PROFILE_COLUMNS}
            FROM gold_employer_profile
            {where_clause}
            ORDER BY employer_name
            LIMIT %s OFFSET %s
            """,
            tuple(where_params + [page_size, offset]),
        )
        return {"rows": rows, "total": total}

    result = await get_cached_rows(cache_key, _fetch)
    return result["rows"], result["total"]


async def get_employer_by_cif(cif: str) -> list[dict]:
    cache_key = f"lov:company:employer:cif={cif}"

    async def _fetch() -> list[dict]:
        return await run_pg_query(
            f"SELECT {EMPLOYER_PROFILE_COLUMNS} FROM gold_employer_profile WHERE cif = %s",
            (cif,),
        )

    return await get_cached_rows(cache_key, _fetch)


async def get_employer_by_employer_id(employer_id: str) -> list[dict]:
    cache_key = f"lov:company:employer:employer_id={employer_id}"

    async def _fetch() -> list[dict]:
        return await run_pg_query(
            f"SELECT {EMPLOYER_PROFILE_COLUMNS} FROM gold_employer_profile WHERE employer_id = %s",
            (employer_id,),
        )

    return await get_cached_rows(cache_key, _fetch)
