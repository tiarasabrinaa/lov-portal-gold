from fastapi import APIRouter

from app.api.endpoints._company_columns import (
    ADDRESS_COLUMNS,
    EMPLOYER_ACCOUNT_COLUMNS,
    STAKEHOLDER_COLUMNS,
    get_employer_by_cif as pg_get_employer_by_cif,
)
from app.core.postgres import run_pg_query
from app.schemas.company import AddressRead, EmployerAccountRead, EmployerProfileRead, StakeholderRead

router = APIRouter()


@router.get("/employer/{cif}", summary="Get employer profile by cif")
async def get_employer_by_cif(cif: str) -> list[EmployerProfileRead]:
    rows = await pg_get_employer_by_cif(cif)
    return [EmployerProfileRead(**row) for row in rows]


@router.get("/account/{cif}", summary="Get employer accounts by cif")
async def get_accounts_by_cif(cif: str) -> list[EmployerAccountRead]:
    rows = await run_pg_query(
        f"SELECT {EMPLOYER_ACCOUNT_COLUMNS} FROM gold_employer_account WHERE cif = %s ORDER BY account_id",
        (cif,),
    )
    return [EmployerAccountRead(**row) for row in rows]


@router.get("/stakeholder/{cif}", summary="Get stakeholders by cif")
async def get_stakeholders_by_cif(cif: str) -> list[StakeholderRead]:
    rows = await run_pg_query(
        f"SELECT {STAKEHOLDER_COLUMNS} FROM gold_stakeholder WHERE cif = %s ORDER BY stakeholder_id",
        (cif,),
    )
    return [StakeholderRead(**row) for row in rows]


@router.get("/address/{cif}", summary="Get addresses by cif")
async def get_addresses_by_cif(cif: str) -> list[AddressRead]:
    rows = await run_pg_query(
        f"SELECT {ADDRESS_COLUMNS} FROM gold_address WHERE cif = %s ORDER BY is_primary DESC",
        (cif,),
    )
    return [AddressRead(**row) for row in rows]
