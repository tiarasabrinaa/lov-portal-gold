from datetime import date

from fastapi import APIRouter, Depends
from google.cloud import bigquery
from pydantic import BaseModel

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table, run_query

router = APIRouter()


class EmployerRead(BaseModel):
    employer_id: str
    group_id: str | None = None
    nob_id: str | None = None
    cif: str
    employer_code: str | None = None
    employer_name: str
    primary_telephone: str | None = None
    primary_email: str | None = None
    tiering: str | None = None
    is_pks: bool | None = None
    is_ntb: bool | None = None
    snapshot_date: date


class AccountRead(BaseModel):
    account_id: str
    employer_id: str | None = None
    cif: str | None = None
    branch_code: str | None = None
    account_number: str | None = None
    currency: str | None = None
    product_code: str | None = None
    account_type: str | None = None
    is_sharia: bool | None = None
    snapshot_date: date


class BranchRead(BaseModel):
    branch_id: str
    branch_code: str | None = None
    branch_name: str | None = None
    branch_address1: str | None = None
    branch_address2: str | None = None
    branch_telephone: str | None = None
    branch_email: str | None = None
    snapshot_date: date


class AddressRead(BaseModel):
    address_id: str
    postcode_id: str | None = None
    employer_id: str | None = None
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


_EMPLOYER_COLUMNS = """
    employer_id,
    group_id,
    nob_id,
    cif,
    employer_code,
    employer_name,
    primary_telephone,
    primary_email,
    tiering,
    is_pks,
    is_ntb,
    snapshot_date
"""

_ACCOUNT_COLUMNS = """
    account_id,
    employer_id,
    cif,
    branch_code,
    account_number,
    currency,
    product_code,
    account_type,
    is_sharia,
    snapshot_date
"""

_BRANCH_COLUMNS = """
    branch_id,
    branch_code,
    branch_name,
    branch_address1,
    branch_address2,
    branch_telephone,
    branch_email,
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
# employer
# ------------------------------------------------------------
@router.get("/employers", summary="Get all employer")
async def get_all_employers(client: bigquery.Client = Depends(get_db)) -> list[EmployerRead]:
    return await fetch_all(
        client,
        f"""
        SELECT {_EMPLOYER_COLUMNS}
        FROM {qualified_table("employer")}
        ORDER BY employer_name
        """,
        EmployerRead,
    )


@router.get("/employers/by-name", summary="Get employer by name")
async def get_employer_by_name(
    name: str,
    client: bigquery.Client = Depends(get_db),
) -> list[EmployerRead]:
    query = f"""
        SELECT {_EMPLOYER_COLUMNS}
        FROM {qualified_table("employer")}
        WHERE LOWER(employer_name) LIKE LOWER(@name)
        ORDER BY employer_name
    """
    params = [bigquery.ScalarQueryParameter("name", "STRING", f"%{name}%")]
    rows = await run_query(client, query, params)
    return [EmployerRead(**row) for row in rows]


@router.get("/employers/by-account-number", summary="Get employer by account number")
async def get_employer_by_account_number(
    account_number: str,
    client: bigquery.Client = Depends(get_db),
) -> list[EmployerRead]:
    query = f"""
        SELECT
            e.employer_id,
            e.group_id,
            e.nob_id,
            e.cif,
            e.employer_code,
            e.employer_name,
            e.primary_telephone,
            e.primary_email,
            e.tiering,
            e.is_pks,
            e.is_ntb,
            e.snapshot_date
        FROM {qualified_table("employer")} e
        JOIN {qualified_table("employer_account")} a ON a.employer_id = e.employer_id
        WHERE a.account_number = @account_number
        ORDER BY e.employer_name
    """
    params = [bigquery.ScalarQueryParameter("account_number", "STRING", account_number)]
    rows = await run_query(client, query, params)
    return [EmployerRead(**row) for row in rows]


# ------------------------------------------------------------
# employer_account
# ------------------------------------------------------------
@router.get("/accounts", summary="Get all account")
async def get_all_accounts(client: bigquery.Client = Depends(get_db)) -> list[AccountRead]:
    return await fetch_all(
        client,
        f"""
        SELECT {_ACCOUNT_COLUMNS}
        FROM {qualified_table("employer_account")}
        ORDER BY account_id
        """,
        AccountRead,
    )


@router.get("/accounts/by-employer-name", summary="Get all account by employer name")
async def get_accounts_by_employer_name(
    name: str,
    client: bigquery.Client = Depends(get_db),
) -> list[AccountRead]:
    query = f"""
        SELECT
            a.account_id,
            a.employer_id,
            a.cif,
            a.branch_code,
            a.account_number,
            a.currency,
            a.product_code,
            a.account_type,
            a.is_sharia,
            a.snapshot_date
        FROM {qualified_table("employer_account")} a
        JOIN {qualified_table("employer")} e ON e.employer_id = a.employer_id
        WHERE LOWER(e.employer_name) LIKE LOWER(@name)
        ORDER BY a.account_id
    """
    params = [bigquery.ScalarQueryParameter("name", "STRING", f"%{name}%")]
    rows = await run_query(client, query, params)
    return [AccountRead(**row) for row in rows]


# ------------------------------------------------------------
# branch
# ------------------------------------------------------------
@router.get("/branches", summary="Get all branch")
async def get_all_branches(client: bigquery.Client = Depends(get_db)) -> list[BranchRead]:
    return await fetch_all(
        client,
        f"""
        SELECT {_BRANCH_COLUMNS}
        FROM {qualified_table("branch")}
        ORDER BY branch_name
        """,
        BranchRead,
    )


# ------------------------------------------------------------
# address
# ------------------------------------------------------------
@router.get("/addresses", summary="Get all address")
async def get_all_addresses(client: bigquery.Client = Depends(get_db)) -> list[AddressRead]:
    return await fetch_all(
        client,
        f"""
        SELECT {_ADDRESS_COLUMNS}
        FROM {qualified_table("address")}
        ORDER BY employer_id, is_primary DESC
        """,
        AddressRead,
    )


@router.get("/addresses/by-name", summary="Get all employer address by name")
async def get_addresses_by_employer_name(
    name: str,
    client: bigquery.Client = Depends(get_db),
) -> list[AddressRead]:
    query = f"""
        SELECT
            ad.address_id,
            ad.postcode_id,
            ad.employer_id,
            ad.cif,
            ad.is_primary,
            ad.rt,
            ad.rw,
            ad.address_detail,
            ad.subdistrict,
            ad.district,
            ad.city,
            ad.province,
            ad.snapshot_date
        FROM {qualified_table("address")} ad
        JOIN {qualified_table("employer")} e ON e.employer_id = ad.employer_id
        WHERE LOWER(e.employer_name) LIKE LOWER(@name)
        ORDER BY ad.employer_id, ad.is_primary DESC
    """
    params = [bigquery.ScalarQueryParameter("name", "STRING", f"%{name}%")]
    rows = await run_query(client, query, params)
    return [AddressRead(**row) for row in rows]
