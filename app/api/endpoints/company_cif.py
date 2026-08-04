from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._company_columns import (
    ADDRESS_COLUMNS,
    EMPLOYER_ACCOUNT_COLUMNS,
    STAKEHOLDER_COLUMNS,
    get_employer_by_cif as bq_get_employer_by_cif,
)
from app.core.database import get_db, qualified_table, run_query
from app.schemas.company import AddressRead, EmployerAccountRead, EmployerProfileRead, StakeholderRead

router = APIRouter()


@router.get("/employer/{cif}", summary="Get employer profile by cif")
async def get_employer_by_cif(cif: str, client: bigquery.Client = Depends(get_db)) -> list[EmployerProfileRead]:
    rows = await bq_get_employer_by_cif(client, cif)
    return [EmployerProfileRead(**row) for row in rows]


@router.get("/account/{cif}", summary="Get employer accounts by cif")
async def get_accounts_by_cif(cif: str, client: bigquery.Client = Depends(get_db)) -> list[EmployerAccountRead]:
    rows = await run_query(
        client,
        f"""
        SELECT {EMPLOYER_ACCOUNT_COLUMNS}
        FROM {qualified_table('gold_employer_account')}
        WHERE cif = @cif
        ORDER BY account_id
        """,
        [bigquery.ScalarQueryParameter("cif", "STRING", cif)],
    )
    return [EmployerAccountRead(**row) for row in rows]


@router.get("/stakeholder/{cif}", summary="Get stakeholders by cif")
async def get_stakeholders_by_cif(cif: str, client: bigquery.Client = Depends(get_db)) -> list[StakeholderRead]:
    rows = await run_query(
        client,
        f"""
        SELECT {STAKEHOLDER_COLUMNS}
        FROM {qualified_table('gold_stakeholder')}
        WHERE cif = @cif
        ORDER BY stakeholder_id
        """,
        [bigquery.ScalarQueryParameter("cif", "STRING", cif)],
    )
    return [StakeholderRead(**row) for row in rows]


@router.get("/address/{cif}", summary="Get addresses by cif")
async def get_addresses_by_cif(cif: str, client: bigquery.Client = Depends(get_db)) -> list[AddressRead]:
    rows = await run_query(
        client,
        f"""
        SELECT {ADDRESS_COLUMNS}
        FROM {qualified_table('gold_address')}
        WHERE cif = @cif
        ORDER BY is_primary DESC
        """,
        [bigquery.ScalarQueryParameter("cif", "STRING", cif)],
    )
    return [AddressRead(**row) for row in rows]