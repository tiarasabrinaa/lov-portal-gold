from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table
from app.schemas.occupation import OccupationRead

router = APIRouter()


@router.get("/", summary="Get all occupation data")
async def get_all_occupation(client: bigquery.Client = Depends(get_db)) -> list[OccupationRead]:
    return await fetch_all(
        client,
        f"""
        SELECT
            occupation_id,
            master_code,
            source_system,
            original_code,
            original_description,
            create_date,
            create_by,
            update_date,
            update_by
        FROM {qualified_table("occupation")}
        ORDER BY master_code
        """,
        OccupationRead,
    )
