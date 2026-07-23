from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table
from app.schemas.ownership_profile import OwnershipProfileRead

router = APIRouter()


@router.get("/", summary="Get all company ownership/shareholder profile data")
async def get_all_company_ownership(client: bigquery.Client = Depends(get_db)) -> list[OwnershipProfileRead]:
    return await fetch_all(
        client,
        f"""
        SELECT
            stakeholder_id,
            employer_id,
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
        FROM {qualified_table("view_employer_ownership_profile")}
        ORDER BY employer_id, ownership_amount DESC
        """,
        OwnershipProfileRead,
    )
