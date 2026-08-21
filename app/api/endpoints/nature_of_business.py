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
            business_date,
            int_indcode,
            corp_short_desc,
            corp_desc,
            risk_level,
            update_date
        FROM {qualified_table("nob")}
        ORDER BY nob_id
        """,
        NatureOfBusinessRead,
    )


@router.get("/{nob_id}", summary="Get nature of business data by id")
async def get_nature_of_business_by_id(
    nob_id: str,
    client: bigquery.Client = Depends(get_db),
) -> list[NatureOfBusinessRead]:
    return await fetch_all(
        client,
        f"""
        SELECT
            nob_id,
            business_date,
            int_indcode,
            corp_short_desc,
            corp_desc,
            risk_level,
            update_date
        FROM {qualified_table("nob")}
        WHERE nob_id = @nob_id
        """,
        NatureOfBusinessRead,
        [bigquery.ScalarQueryParameter("nob_id", "STRING", nob_id)],
    )
