from fastapi import APIRouter, Depends, Query
from google.cloud import bigquery

from app.api.endpoints._company_columns import (
    ADDRESS_COLUMNS,
    EMPLOYER_ACCOUNT_COLUMNS,
    STAKEHOLDER_COLUMNS,
    get_employer_by_employer_id as bq_get_employer_by_employer_id,
    get_employer_page,
    search_employers_by_name,
)
from app.core.database import get_db, qualified_table, run_query
from app.schemas.company import (
    AddressRead,
    EmployerAccountRead,
    EmployerProfileRead,
    PaginatedEmployers,
    StakeholderRead,
)

router = APIRouter()


# ------------------------------------------------------------
# gold_employer_profile
#
# Pure BigQuery, no Redis/Postgres. Pagination & search dilakuin di level
# SQL (LIMIT/OFFSET, LIKE) - bukan tarik semua baris lalu dipotong di
# Python, itu yang bikin lemot begitu datanya ratusan ribu baris.
# Lookup by-cif ada di router terpisah: company_cif.py.
# ------------------------------------------------------------
@router.get("/employers", summary="Get all employer profiles (paginated)")
async def get_all_employers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    client: bigquery.Client = Depends(get_db),
) -> PaginatedEmployers:
    rows, total = await get_employer_page(client, None, page, page_size)
    return PaginatedEmployers(
        items=[EmployerProfileRead(**row) for row in rows], total=total, page=page, page_size=page_size
    )


@router.get(
    "/employer/by-name",
    summary="Get employer profiles by name (substring, case-insensitive, pure BigQuery)",
)
async def get_employer_by_name(
    name: str,
    client: bigquery.Client = Depends(get_db),
) -> PaginatedEmployers:
    rows = await search_employers_by_name(client, name)
    return PaginatedEmployers(
        items=[EmployerProfileRead(**row) for row in rows], total=len(rows), page=1, page_size=len(rows)
    )


@router.get("/employer/by-employer-id/{employer_id}", summary="Get employer profile by employer_id")
async def get_employer_by_employer_id(
    employer_id: str, client: bigquery.Client = Depends(get_db)
) -> list[EmployerProfileRead]:
    rows = await bq_get_employer_by_employer_id(client, employer_id)
    return [EmployerProfileRead(**row) for row in rows]


# ------------------------------------------------------------
# gold_employer_account
# ------------------------------------------------------------
@router.get("/accounts", summary="Get all employer accounts")
async def get_all_accounts(client: bigquery.Client = Depends(get_db)) -> list[EmployerAccountRead]:
    rows = await run_query(
        client,
        f"SELECT {EMPLOYER_ACCOUNT_COLUMNS} FROM {qualified_table('gold_employer_account')} ORDER BY account_id",
    )
    return [EmployerAccountRead(**row) for row in rows]


@router.get("/account/by-employer-id/{employer_id}", summary="Get employer accounts by employer_id")
async def get_accounts_by_employer_id(
    employer_id: str, client: bigquery.Client = Depends(get_db)
) -> list[EmployerAccountRead]:
    rows = await run_query(
        client,
        f"""
        SELECT {EMPLOYER_ACCOUNT_COLUMNS}
        FROM {qualified_table('gold_employer_account')}
        WHERE employer_id = @employer_id
        ORDER BY account_id
        """,
        [bigquery.ScalarQueryParameter("employer_id", "STRING", employer_id)],
    )
    return [EmployerAccountRead(**row) for row in rows]


# ------------------------------------------------------------
# gold_stakeholder
# ------------------------------------------------------------
@router.get("/stakeholders", summary="Get all stakeholders")
async def get_all_stakeholders(client: bigquery.Client = Depends(get_db)) -> list[StakeholderRead]:
    rows = await run_query(
        client,
        f"SELECT {STAKEHOLDER_COLUMNS} FROM {qualified_table('gold_stakeholder')} ORDER BY stakeholder_id",
    )
    return [StakeholderRead(**row) for row in rows]


@router.get("/stakeholder/by-employer-id/{employer_id}", summary="Get stakeholders by employer_id")
async def get_stakeholders_by_employer_id(
    employer_id: str, client: bigquery.Client = Depends(get_db)
) -> list[StakeholderRead]:
    rows = await run_query(
        client,
        f"""
        SELECT {STAKEHOLDER_COLUMNS}
        FROM {qualified_table('gold_stakeholder')}
        WHERE employer_id = @employer_id
        ORDER BY stakeholder_id
        """,
        [bigquery.ScalarQueryParameter("employer_id", "STRING", employer_id)],
    )
    return [StakeholderRead(**row) for row in rows]


# ------------------------------------------------------------
# gold_address
# ------------------------------------------------------------
@router.get("/addresses", summary="Get all addresses")
async def get_all_addresses(client: bigquery.Client = Depends(get_db)) -> list[AddressRead]:
    rows = await run_query(
        client,
        f"""
        SELECT {ADDRESS_COLUMNS}
        FROM {qualified_table('gold_address')}
        ORDER BY employer_id, is_primary DESC
        """,
    )
    return [AddressRead(**row) for row in rows]


@router.get("/address/by-employer-id/{employer_id}", summary="Get addresses by employer_id")
async def get_addresses_by_employer_id(
    employer_id: str, client: bigquery.Client = Depends(get_db)
) -> list[AddressRead]:
    rows = await run_query(
        client,
        f"""
        SELECT {ADDRESS_COLUMNS}
        FROM {qualified_table('gold_address')}
        WHERE employer_id = @employer_id
        ORDER BY is_primary DESC
        """,
        [bigquery.ScalarQueryParameter("employer_id", "STRING", employer_id)],
    )
    return [AddressRead(**row) for row in rows]
