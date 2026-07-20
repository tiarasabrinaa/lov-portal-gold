from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table
from app.schemas.religion import ReligionRead

router = APIRouter()


@router.get("/", summary="Get all religion data")
async def get_all_religion(client: bigquery.Client = Depends(get_db)) -> list[ReligionRead]:
    return await fetch_all(
        client,
        f"""
        SELECT
            master_code,
            source_system,
            original_code,
            original_description,
            create_date,
            create_by,
            update_date,
            update_by
        FROM {qualified_table("religion")}
        ORDER BY master_code
        """,
        ReligionRead,
    )
