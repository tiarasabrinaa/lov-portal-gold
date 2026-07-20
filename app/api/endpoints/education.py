from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table
from app.schemas.education import EducationRead

router = APIRouter()


@router.get("/", summary="Get all education data")
async def get_all_education(client: bigquery.Client = Depends(get_db)) -> list[EducationRead]:
    return await fetch_all(
        client,
        f"""
        SELECT
            education_id,
            master_code,
            source_system,
            original_code,
            original_description,
            create_date,
            create_by,
            update_date,
            update_by
        FROM {qualified_table("education")}
        ORDER BY master_code
        """,
        EducationRead,
    )


@router.get("/{master_code}", summary="Get education data by master code")
async def get_education_by_master_code(
    master_code: str, client: bigquery.Client = Depends(get_db)
) -> list[EducationRead]:
    return await fetch_all(
        client,
        f"""
        SELECT
            education_id,
            master_code,
            source_system,
            original_code,
            original_description,
            create_date,
            create_by,
            update_date,
            update_by
        FROM {qualified_table("education")}
        WHERE master_code = @master_code
        ORDER BY master_code
        """,
        EducationRead,
        [bigquery.ScalarQueryParameter("master_code", "STRING", master_code)],
    )
