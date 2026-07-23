from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table
from app.schemas.account_branch import AccountBranchRead

router = APIRouter()


@router.get("/", summary="Get all company account/branch data")
async def get_all_company_accounts(client: bigquery.Client = Depends(get_db)) -> list[AccountBranchRead]:
    return await fetch_all(
        client,
        f"""
        SELECT
            account_id,
            cif,
            branch_code,
            employer_name,
            group_name,
            account_number,
            currency,
            product_code,
            account_type,
            creation_bank_no,
            is_sharia,
            branch_name,
            branch_address1,
            branch_address2,
            branch_telephone,
            branch_email,
            primary_address_postcode,
            primary_address_rt_rw,
            primary_address_detail,
            primary_address_subdistrict,
            primary_address_district,
            primary_address_city,
            primary_address_province,
            snapshot_date
        FROM {qualified_table("view_account_branch")}
        ORDER BY employer_name, branch_code
        """,
        AccountBranchRead,
    )
