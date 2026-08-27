from google.cloud import bigquery

from app.core.database import qualified_table, run_query

EMPLOYER_PROFILE_COLUMNS = """
    e.employer_id,
    e.group_id,
    e.nob_id,
    n.corp_short_desc,
    n.corp_desc,
    e.cif,
    e.employer_name,
    e.employer_code,
    e.tiering_code,
    e.tiering_label,
    e.group_name,
    e.primary_email,
    e.primary_contact_no,
    e.snapshot_date
"""

# nob_id ada di gold_employer_profile & nob - kolom EMPLOYER_PROFILE_COLUMNS
# di atas dikasih alias e./n. biar gak ambigu pas di-JOIN.

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

    Pure BigQuery - page/page_size udah divalidasi jadi int sama
    FastAPI Query(ge=..., le=...) di router, aman diinterpolasi langsung ke LIMIT/OFFSET
    tanpa perlu parameter.
    """
    where_clause = ""
    params: list[bigquery.ScalarQueryParameter] = []
    if name:
        where_clause = "WHERE LOWER(e.employer_name) LIKE LOWER(@name)"
        params.append(bigquery.ScalarQueryParameter("name", "STRING", f"%{name}%"))

    offset = (page - 1) * page_size
    rows = await run_query(
        client,
        f"""
        SELECT
            {EMPLOYER_PROFILE_COLUMNS},
            COUNT(*) OVER() AS total_count
        FROM {qualified_table('gold_employer_profile')} e
        LEFT JOIN {qualified_table('nob')} n ON e.nob_id = n.nob_id
        {where_clause}
        ORDER BY e.employer_name
        LIMIT {page_size} OFFSET {offset}
        """,
        params,
    )

    if rows:
        total = rows[0].pop("total_count")
        for row in rows[1:]:
            row.pop("total_count", None)
        return rows, total

    # halaman kosong (0 match atau offset lewat akhir) - baru scan count terpisah di sini
    count_rows = await run_query(
        client,
        f"SELECT COUNT(*) AS total FROM {qualified_table('gold_employer_profile')} e {where_clause}",
        params,
    )
    return rows, count_rows[0]["total"]


async def get_employer_by_cif(client: bigquery.Client, cif: str) -> list[dict]:
    return await run_query(
        client,
        f"""
        SELECT {EMPLOYER_PROFILE_COLUMNS}
        FROM {qualified_table('gold_employer_profile')} e
        LEFT JOIN {qualified_table('nob')} n ON e.nob_id = n.nob_id
        WHERE e.cif = @cif
        """,
        [bigquery.ScalarQueryParameter("cif", "STRING", cif)],
    )


async def get_employer_by_employer_id(client: bigquery.Client, employer_id: str) -> list[dict]:
    return await run_query(
        client,
        f"""
        SELECT {EMPLOYER_PROFILE_COLUMNS}
        FROM {qualified_table('gold_employer_profile')} e
        LEFT JOIN {qualified_table('nob')} n ON e.nob_id = n.nob_id
        WHERE e.employer_id = @employer_id
        """,
        [bigquery.ScalarQueryParameter("employer_id", "STRING", employer_id)],
    )