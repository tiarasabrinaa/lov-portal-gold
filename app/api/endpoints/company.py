from fastapi import APIRouter, Depends, Query
from google.cloud import bigquery

from app.api.endpoints._company_columns import (
    ADDRESS_COLUMNS,
    EMPLOYER_ACCOUNT_COLUMNS,
    STAKEHOLDER_COLUMNS,
    get_all_employer_rows,
)
from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table, run_query
from app.schemas.company import (
    AddressRead,
    EmployerAccountRead,
    EmployerProfileRead,
    PaginatedEmployers,
    StakeholderRead,
)

router = APIRouter()


def _paginate(rows: list[dict], page: int, page_size: int) -> PaginatedEmployers:
    start = (page - 1) * page_size
    end = start + page_size
    return PaginatedEmployers(
        items=[EmployerProfileRead(**row) for row in rows[start:end]],
        total=len(rows),
        page=page,
        page_size=page_size,
    )


# ------------------------------------------------------------
# gold_employer_profile
#
# "all" / "by-name" baca dari 1 cache Redis (list lengkap employer,
# TTL settings.cache_ttl_seconds) dan filter di Python - biar "ngetik
# per huruf" (typeahead) responnya instan tanpa nembak BigQuery tiap
# keystroke. Lookup by-cif ada di router terpisah: company_cif.py.
# ------------------------------------------------------------
@router.get("/employers", summary="Get all employer profiles (paginated)")
async def get_all_employers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    client: bigquery.Client = Depends(get_db),
) -> PaginatedEmployers:
    rows = await get_all_employer_rows(client)
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
    rows = await get_all_employer_rows(client)
    needle = name.lower()
    matches = [row for row in rows if needle in (row["employer_name"] or "").lower()]
    return _paginate(matches, page, page_size)


@router.get("/employers/by-employer-id/{employer_id}", summary="Get employer profile by employer_id")
async def get_employer_by_employer_id(
    employer_id: str, client: bigquery.Client = Depends(get_db)
) -> list[EmployerProfileRead]:
    rows = await get_all_employer_rows(client)
    matches = [row for row in rows if row["employer_id"] == employer_id]
    return [EmployerProfileRead(**row) for row in matches]


# ------------------------------------------------------------
# gold_employer_account
# ------------------------------------------------------------
@router.get("/accounts", summary="Get all employer accounts")
async def get_all_accounts(client: bigquery.Client = Depends(get_db)) -> list[EmployerAccountRead]:
    return await fetch_all(
        client,
        f"""
        SELECT {EMPLOYER_ACCOUNT_COLUMNS}
        FROM {qualified_table("gold_employer_account")}
        ORDER BY account_id
        """,
        EmployerAccountRead,
    )


@router.get("/accounts/by-employer-id/{employer_id}", summary="Get employer accounts by employer_id")
async def get_accounts_by_employer_id(
    employer_id: str, client: bigquery.Client = Depends(get_db)
) -> list[EmployerAccountRead]:
    query = f"""
        SELECT {EMPLOYER_ACCOUNT_COLUMNS}
        FROM {qualified_table("gold_employer_account")}
        WHERE employer_id = @employer_id
        ORDER BY account_id
    """
    params = [bigquery.ScalarQueryParameter("employer_id", "STRING", employer_id)]
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
        SELECT {STAKEHOLDER_COLUMNS}
        FROM {qualified_table("gold_stakeholder")}
        ORDER BY stakeholder_id
        """,
        StakeholderRead,
    )


@router.get("/stakeholders/by-employer-id/{employer_id}", summary="Get stakeholders by employer_id")
async def get_stakeholders_by_employer_id(
    employer_id: str, client: bigquery.Client = Depends(get_db)
) -> list[StakeholderRead]:
    query = f"""
        SELECT {STAKEHOLDER_COLUMNS}
        FROM {qualified_table("gold_stakeholder")}
        WHERE employer_id = @employer_id
        ORDER BY stakeholder_id
    """
    params = [bigquery.ScalarQueryParameter("employer_id", "STRING", employer_id)]
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
        SELECT {ADDRESS_COLUMNS}
        FROM {qualified_table("gold_address")}
        ORDER BY employer_id, is_primary DESC
        """,
        AddressRead,
    )


@router.get("/addresses/by-employer-id/{employer_id}", summary="Get addresses by employer_id")
async def get_addresses_by_employer_id(
    employer_id: str, client: bigquery.Client = Depends(get_db)
) -> list[AddressRead]:
    query = f"""
        SELECT {ADDRESS_COLUMNS}
        FROM {qualified_table("gold_address")}
        WHERE employer_id = @employer_id
        ORDER BY is_primary DESC
    """
    params = [bigquery.ScalarQueryParameter("employer_id", "STRING", employer_id)]
    rows = await run_query(client, query, params)
    return [AddressRead(**row) for row in rows]
