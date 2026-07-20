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
            master_code,
            source_system,
            original_code,
            original_description,
            create_date,
            create_by,
            update_date,
            update_by
        FROM {qualified_table("nature_of_business")}
        ORDER BY master_code
        """,
        NatureOfBusinessRead,
    )
