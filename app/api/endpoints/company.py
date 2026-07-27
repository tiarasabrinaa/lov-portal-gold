from datetime import date

from fastapi import APIRouter, Depends, Query
from google.cloud import bigquery
from pydantic import BaseModel

from app.api.endpoints._helpers import fetch_all
from app.core.cache import get_cached_rows
from app.core.database import get_db, qualified_table, run_query

_EMPLOYERS_CACHE_KEY = "lov:company:employers:all"

router = APIRouter()


class EmployerProfileRead(BaseModel):
    employer_id: str
    group_id: str | None = None
    nob_id: str | None = None
    cif: str
    employer_name: str
    employer_code: str | None = None
    sector: str | None = None
    sub_sector: str | None = None
    industry: str | None = None
    subindustry: str | None = None
    group_name: str | None = None
    primary_email: str | None = None
    primary_contact_no: str | None = None
    snapshot_date: date


class PaginatedEmployers(BaseModel):
    items: list[EmployerProfileRead]
    total: int
    page: int
    page_size: int


class EmployerAccountRead(BaseModel):
    account_id: str
    cif: str | None = None
    branch_code: str | None = None
    branch_name: str | None = None
    branch_address1: str | None = None
    branch_address2: str | None = None
    branch_telephone: str | None = None
    branch_email: str | None = None
    account_number: str | None = None
    currency: str | None = None
    product_code: str | None = None
    account_type: str | None = None
    is_sharia: bool | None = None
    snapshot_date: date


class StakeholderRead(BaseModel):
    stakeholder_id: str
    employer_id: str
    cif: str | None = None
    employer_name: str | None = None
    stock_code: str | None = None
    group_name: str | None = None
    sector: str | None = None
    shareholder_type: str | None = None
    stakeholder_name: str | None = None
    ownership_amount: float | None = None
    ownership_percentage: float | None = None
    designation: str | None = None
    snapshot_date: date


class AddressRead(BaseModel):
    address_id: str
    postcode_id: str | None = None
    employer_id: str
    cif: str | None = None
    is_primary: bool | None = None
    rt: str | None = None
    rw: str | None = None
    address_detail: str | None = None
    subdistrict: str | None = None
    district: str | None = None
    city: str | None = None
    province: str | None = None
    snapshot_date: date


_EMPLOYER_PROFILE_COLUMNS = """
    employer_id,
    group_id,
    nob_id,
    cif,
    employer_name,
    employer_code,
    sector,
    sub_sector,
    industry,
    subindustry,
    group_name,
    primary_email,
    primary_contact_no,
    snapshot_date
"""

_EMPLOYER_ACCOUNT_COLUMNS = """
    account_id,
    cif,
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

_STAKEHOLDER_COLUMNS = """
    stakeholder_id,
    employer_id,
    cif,
    employer_name,
    stock_code,
    group_name,
    sector,
    shareholder_type,
    stakeholder_name,
    ownership_amount,
    ownership_percentage,
    designation,
    snapshot_date
"""

_ADDRESS_COLUMNS = """
    address_id,
    postcode_id,
    employer_id,
    cif,
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


# ------------------------------------------------------------
# gold_employer_profile
#
# Semua endpoint di bawah baca dari 1 cache Redis (list lengkap
# employer, TTL settings.cache_ttl_seconds) dan filter di Python -
# biar "ngetik per huruf" (typeahead) responnya instan tanpa nembak
# BigQuery tiap keystroke. Cache auto-refresh dari BigQuery begitu
# TTL abis / cache kosong.
# ------------------------------------------------------------
async def _get_all_employer_rows(client: bigquery.Client) -> list[dict]:
    return await get_cached_rows(
        _EMPLOYERS_CACHE_KEY,
        client,
        f"""
        SELECT {_EMPLOYER_PROFILE_COLUMNS}
        FROM {qualified_table("gold_employer_profile")}
        ORDER BY employer_name
        """,
    )


def _paginate(rows: list[dict], page: int, page_size: int) -> PaginatedEmployers:
    start = (page - 1) * page_size
    end = start + page_size
    return PaginatedEmployers(
        items=[EmployerProfileRead(**row) for row in rows[start:end]],
        total=len(rows),
        page=page,
        page_size=page_size,
    )


@router.get("/employers", summary="Get all employer profiles (paginated)")
async def get_all_employers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    client: bigquery.Client = Depends(get_db),
) -> PaginatedEmployers:
    rows = await _get_all_employer_rows(client)
    return _paginate(rows, page, page_size)


@router.get(
    "/employers/by-name",
    summary="Get employer profiles by name (substring, case-insensitive, paginated)",
)
async def get_employer_by_name(
    name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    client: bigquery.Client = Depends(get_db),
) -> PaginatedEmployers:
    rows = await _get_all_employer_rows(client)
    needle = name.lower()
    matches = [row for row in rows if needle in (row["employer_name"] or "").lower()]
    return _paginate(matches, page, page_size)


@router.get("/employers/{cif}", summary="Get employer profile by cif")
async def get_employer_by_cif(
    cif: str, client: bigquery.Client = Depends(get_db)
) -> list[EmployerProfileRead]:
    rows = await _get_all_employer_rows(client)
    matches = [row for row in rows if row["cif"] == cif]
    return [EmployerProfileRead(**row) for row in matches]


# ------------------------------------------------------------
# gold_employer_account
# ------------------------------------------------------------
@router.get("/accounts", summary="Get all employer accounts")
async def get_all_accounts(client: bigquery.Client = Depends(get_db)) -> list[EmployerAccountRead]:
    return await fetch_all(
        client,
        f"""
        SELECT {_EMPLOYER_ACCOUNT_COLUMNS}
        FROM {qualified_table("gold_employer_account")}
        ORDER BY account_id
        """,
        EmployerAccountRead,
    )


@router.get("/accounts/{cif}", summary="Get employer accounts by cif")
async def get_accounts_by_cif(
    cif: str, client: bigquery.Client = Depends(get_db)
) -> list[EmployerAccountRead]:
    query = f"""
        SELECT {_EMPLOYER_ACCOUNT_COLUMNS}
        FROM {qualified_table("gold_employer_account")}
        WHERE cif = @cif
        ORDER BY account_id
    """
    params = [bigquery.ScalarQueryParameter("cif", "STRING", cif)]
    rows = await run_query(client, query, params)
    return [EmployerAccountRead(**row) for row in rows]


# ------------------------------------------------------------
# gold_stakeholder
# ------------------------------------------------------------
@router.get("/stakeholders", summary="Get all stakeholders")
async def get_all_stakeholders(client: bigquery.Client = Depends(get_db)) -> list[StakeholderRead]:
    return await fetch_all(
        client,
        f"""
        SELECT {_STAKEHOLDER_COLUMNS}
        FROM {qualified_table("gold_stakeholder")}
        ORDER BY stakeholder_id
        """,
        StakeholderRead,
    )


@router.get("/stakeholders/{cif}", summary="Get stakeholders by cif")
async def get_stakeholders_by_cif(
    cif: str, client: bigquery.Client = Depends(get_db)
) -> list[StakeholderRead]:
    query = f"""
        SELECT {_STAKEHOLDER_COLUMNS}
        FROM {qualified_table("gold_stakeholder")}
        WHERE cif = @cif
        ORDER BY stakeholder_id
    """
    params = [bigquery.ScalarQueryParameter("cif", "STRING", cif)]
    rows = await run_query(client, query, params)
    return [StakeholderRead(**row) for row in rows]


# ------------------------------------------------------------
# gold_address
# ------------------------------------------------------------
@router.get("/addresses", summary="Get all addresses")
async def get_all_addresses(client: bigquery.Client = Depends(get_db)) -> list[AddressRead]:
    return await fetch_all(
        client,
        f"""
        SELECT {_ADDRESS_COLUMNS}
        FROM {qualified_table("gold_address")}
        ORDER BY employer_id, is_primary DESC
        """,
        AddressRead,
    )


@router.get("/addresses/{cif}", summary="Get addresses by cif")
async def get_addresses_by_cif(
    cif: str, client: bigquery.Client = Depends(get_db)
) -> list[AddressRead]:
    query = f"""
        SELECT {_ADDRESS_COLUMNS}
        FROM {qualified_table("gold_address")}
        WHERE cif = @cif
        ORDER BY is_primary DESC
    """
    params = [bigquery.ScalarQueryParameter("cif", "STRING", cif)]
    rows = await run_query(client, query, params)
    return [AddressRead(**row) for row in rows]
