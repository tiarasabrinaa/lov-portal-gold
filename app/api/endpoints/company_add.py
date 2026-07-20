from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table
from app.schemas.company_add import CompanyAddRead

router = APIRouter()


@router.get("/", summary="Get all company address data")
async def get_all_company_add(client: bigquery.Client = Depends(get_db)) -> list[CompanyAddRead]:
    return await fetch_all(
        client,
        f"""
        SELECT
            address_id,
            employer_id,
            address_type,
            address_detail,
            subdistrict,
            district,
            city,
            province,
            postcode,
            postcode_id,
            is_primary,
            is_current,
            effective_date,
            expiry_date
        FROM {qualified_table("employer_address")}
        ORDER BY employer_id, address_type
        """,
        CompanyAddRead,
    )
