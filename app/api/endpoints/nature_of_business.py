from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table
from app.schemas.nature_of_business import NatureOfBusinessRead

router = APIRouter()


@router.get("/", summary="Get all nature of business data")
async def get_all_nature_of_business(client: bigquery.Client = Depends(get_db)) -> list[NatureOfBusinessRead]:
    return await fetch_all(
        client,
        f"""
        SELECT
            nob_id,
            master_code,
            source_system,
            original_code,
            original_sector,
            original_sub_sector,
            original_industry,
            original_sub_industry,
            kbli,
            individual_type,
            effective_date,
            expiry_date,
            is_current,
            create_date,
            create_by,
            update_date,
            update_by
        FROM {qualified_table("nob")}
        ORDER BY master_code
        """,
        NatureOfBusinessRead,
    )
