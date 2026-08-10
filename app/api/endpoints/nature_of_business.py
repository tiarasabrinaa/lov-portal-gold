from fastapi import APIRouter, Depends, Query
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
            master_description,
            source_system,
            original_code,
            original_description,
            snapshot_date
        FROM {qualified_table("nob")}
        ORDER BY master_code
        """,
        NatureOfBusinessRead,
    )


@router.get("/{master_code}", summary="Get nature of business data by master code")
async def get_nature_of_business_by_master_code(
    master_code: str,
    source_system: str | None = Query(None, description="Filter by source system, e.g. SIBS, ASCEND"),
    client: bigquery.Client = Depends(get_db),
) -> list[NatureOfBusinessRead]:
    params = [bigquery.ScalarQueryParameter("master_code", "STRING", master_code)]
    source_filter = ""
    if source_system:
        source_filter = "AND source_system = @source_system"
        params.append(bigquery.ScalarQueryParameter("source_system", "STRING", source_system))

    return await fetch_all(
        client,
        f"""
        SELECT
            nob_id,
            master_code,
            master_description,
            source_system,
            original_code,
            original_description,
            snapshot_date
        FROM {qualified_table("nob")}
        WHERE master_code = @master_code
        {source_filter}
        ORDER BY master_code
        """,
        NatureOfBusinessRead,
        params,
    )
