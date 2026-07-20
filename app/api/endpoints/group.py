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
        SELECT
            group_id,
            comp_id,
            parent_comp_id,
            group_name,
            relationship_type,
            ownership_level,
            gold_load_ts
        FROM {qualified_table("comp_group")}
        ORDER BY group_name, comp_id
        """,
        GroupRead,
    )
