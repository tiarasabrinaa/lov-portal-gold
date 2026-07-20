from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table
from app.schemas.job_title import JobTitleRead

router = APIRouter()


@router.get("/", summary="Get all job title data")
async def get_all_job_title(client: bigquery.Client = Depends(get_db)) -> list[JobTitleRead]:
    return await fetch_all(
        client,
        f"""
        SELECT
            job_title_id,
            master_code,
            source_system,
            original_code,
            original_description,
            create_date,
            create_by,
            update_date,
            update_by
        FROM {qualified_table("job_title")}
        ORDER BY master_code
        """,
        JobTitleRead,
    )
