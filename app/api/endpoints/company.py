from fastapi import APIRouter, Query

from app.api.endpoints._company_columns import (
    ADDRESS_COLUMNS,
    EMPLOYER_ACCOUNT_COLUMNS,
    STAKEHOLDER_COLUMNS,
    get_employer_by_employer_id as pg_get_employer_by_employer_id,
    get_employer_page,
)
from app.core.postgres import run_pg_query
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
# Semua endpoint di modul ini baca dari Postgres (bukan BigQuery lagi -
# BigQuery cuma disentuh sama scripts/sync_bigquery_to_postgres.py, 1x
# per periode sync). Pagination & search dilakuin di level SQL
# (LIMIT/OFFSET, ILIKE + index pg_trgm) - bukan tarik semua baris lalu
# dipotong di Python, itu yang bikin lemot begitu datanya ratusan ribu
# baris. Cache Redis-nya juga per-kombinasi query (nama+halaman), bukan
# 1 cache buat seluruh tabel. Lookup by-cif ada di router terpisah:
# company_cif.py.
# ------------------------------------------------------------
@router.get("/employers", summary="Get all employer profiles (paginated)")
async def get_all_employers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
) -> PaginatedEmployers:
    rows, total = await get_employer_page(None, page, page_size)
    return PaginatedEmployers(
        items=[EmployerProfileRead(**row) for row in rows], total=total, page=page, page_size=page_size
    )


@router.get(
    "/employer/by-name",
    summary="Get employer profiles by name (substring, case-insensitive, paginated)",
)
async def get_employer_by_name(
    name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
) -> PaginatedEmployers:
    rows, total = await get_employer_page(name, page, page_size)
    return PaginatedEmployers(
        items=[EmployerProfileRead(**row) for row in rows], total=total, page=page, page_size=page_size
    )


@router.get("/employer/by-employer-id/{employer_id}", summary="Get employer profile by employer_id")
async def get_employer_by_employer_id(employer_id: str) -> list[EmployerProfileRead]:
    rows = await pg_get_employer_by_employer_id(employer_id)
    return [EmployerProfileRead(**row) for row in rows]


# ------------------------------------------------------------
# gold_employer_account
# ------------------------------------------------------------
@router.get("/accounts", summary="Get all employer accounts")
async def get_all_accounts() -> list[EmployerAccountRead]:
    rows = await run_pg_query(f"SELECT {EMPLOYER_ACCOUNT_COLUMNS} FROM gold_employer_account ORDER BY account_id")
    return [EmployerAccountRead(**row) for row in rows]


@router.get("/account/by-employer-id/{employer_id}", summary="Get employer accounts by employer_id")
async def get_accounts_by_employer_id(employer_id: str) -> list[EmployerAccountRead]:
    rows = await run_pg_query(
        f"SELECT {EMPLOYER_ACCOUNT_COLUMNS} FROM gold_employer_account WHERE employer_id = %s ORDER BY account_id",
        (employer_id,),
    )
    return [EmployerAccountRead(**row) for row in rows]


# ------------------------------------------------------------
# gold_stakeholder
# ------------------------------------------------------------
@router.get("/stakeholders", summary="Get all stakeholders")
async def get_all_stakeholders() -> list[StakeholderRead]:
    rows = await run_pg_query(f"SELECT {STAKEHOLDER_COLUMNS} FROM gold_stakeholder ORDER BY stakeholder_id")
    return [StakeholderRead(**row) for row in rows]


@router.get("/stakeholder/by-employer-id/{employer_id}", summary="Get stakeholders by employer_id")
async def get_stakeholders_by_employer_id(employer_id: str) -> list[StakeholderRead]:
    rows = await run_pg_query(
        f"SELECT {STAKEHOLDER_COLUMNS} FROM gold_stakeholder WHERE employer_id = %s ORDER BY stakeholder_id",
        (employer_id,),
    )
    return [StakeholderRead(**row) for row in rows]


# ------------------------------------------------------------
# gold_address
# ------------------------------------------------------------
@router.get("/addresses", summary="Get all addresses")
async def get_all_addresses() -> list[AddressRead]:
    rows = await run_pg_query(f"SELECT {ADDRESS_COLUMNS} FROM gold_address ORDER BY employer_id, is_primary DESC")
    return [AddressRead(**row) for row in rows]


@router.get("/address/by-employer-id/{employer_id}", summary="Get addresses by employer_id")
async def get_addresses_by_employer_id(employer_id: str) -> list[AddressRead]:
    rows = await run_pg_query(
        f"SELECT {ADDRESS_COLUMNS} FROM gold_address WHERE employer_id = %s ORDER BY is_primary DESC",
        (employer_id,),
    )
    return [AddressRead(**row) for row in rows]
