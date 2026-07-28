from google.cloud import bigquery

from app.core.cache import get_cached_rows
from app.core.database import qualified_table

EMPLOYERS_CACHE_KEY = "lov:company:employers:all"

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
    branch_address1,
    branch_address2,
    branch_telephone,
    branch_email,
    account_number,
    currency,
    product_code,
    account_type,
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


async def get_all_employer_rows(client: bigquery.Client) -> list[dict]:
    """Full gold_employer_profile list, Redis-cached (TTL settings.cache_ttl_seconds).

    Dipakai bareng oleh company.py (all/by-name/by-employer-id) dan
    company_cif.py (by-cif) supaya cache-nya satu, ga duplikat hit BigQuery.
    """
    return await get_cached_rows(
        EMPLOYERS_CACHE_KEY,
        client,
        f"""
        SELECT {EMPLOYER_PROFILE_COLUMNS}
        FROM {qualified_table("gold_employer_profile")}
        ORDER BY employer_name
        """,
    )
