from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table
from app.schemas.group import GroupRead

router = APIRouter()


@router.get("/", summary="Get all group data")
async def get_all_group(client: bigquery.Client = Depends(get_db)) -> list[GroupRead]:
    return await fetch_all(
        client,
        f"""
        SELECT DISTINCT
            group_id,
            group_name
        FROM {qualified_table("gold_employer_profile")}
        WHERE group_id IS NOT NULL
        ORDER BY group_name
        """,
        GroupRead,
    )
