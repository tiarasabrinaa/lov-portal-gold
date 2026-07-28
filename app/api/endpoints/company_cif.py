from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._company_columns import (
    ADDRESS_COLUMNS,
    EMPLOYER_ACCOUNT_COLUMNS,
    STAKEHOLDER_COLUMNS,
    get_all_employer_rows,
)
from app.core.database import get_db, qualified_table, run_query
from app.schemas.company import AddressRead, EmployerAccountRead, EmployerProfileRead, StakeholderRead

router = APIRouter()


@router.get("/employer/{cif}", summary="Get employer profile by cif")
async def get_employer_by_cif(
    cif: str, client: bigquery.Client = Depends(get_db)
) -> list[EmployerProfileRead]:
    rows = await get_all_employer_rows(client)
    matches = [row for row in rows if row["cif"] == cif]
    return [EmployerProfileRead(**row) for row in matches]


@router.get("/account/{cif}", summary="Get employer accounts by cif")
async def get_accounts_by_cif(
    cif: str, client: bigquery.Client = Depends(get_db)
) -> list[EmployerAccountRead]:
    query = f"""
        SELECT {EMPLOYER_ACCOUNT_COLUMNS}
        FROM {qualified_table("gold_employer_account")}
        WHERE cif = @cif
        ORDER BY account_id
    """
    params = [bigquery.ScalarQueryParameter("cif", "STRING", cif)]
    rows = await run_query(client, query, params)
    return [EmployerAccountRead(**row) for row in rows]


@router.get("/stakeholder/{cif}", summary="Get stakeholders by cif")
async def get_stakeholders_by_cif(
    cif: str, client: bigquery.Client = Depends(get_db)
) -> list[StakeholderRead]:
    query = f"""
        SELECT {STAKEHOLDER_COLUMNS}
        FROM {qualified_table("gold_stakeholder")}
        WHERE cif = @cif
        ORDER BY stakeholder_id
    """
    params = [bigquery.ScalarQueryParameter("cif", "STRING", cif)]
    rows = await run_query(client, query, params)
    return [StakeholderRead(**row) for row in rows]


@router.get("/address/{cif}", summary="Get addresses by cif")
async def get_addresses_by_cif(
    cif: str, client: bigquery.Client = Depends(get_db)
) -> list[AddressRead]:
    query = f"""
        SELECT {ADDRESS_COLUMNS}
        FROM {qualified_table("gold_address")}
        WHERE cif = @cif
        ORDER BY is_primary DESC
    """
    params = [bigquery.ScalarQueryParameter("cif", "STRING", cif)]
    rows = await run_query(client, query, params)
    return [AddressRead(**row) for row in rows]
