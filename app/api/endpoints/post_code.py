from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table
from app.schemas.post_code import PostCodeRead

router = APIRouter()


@router.get("/", summary="Get all post code data")
async def get_all_post_code(client: bigquery.Client = Depends(get_db)) -> list[PostCodeRead]:
    return await fetch_all(
        client,
        f"""
        SELECT
            postal_code,
            kelurahan,
            kecamatan,
            kabupaten_kota,
            provinsi,
            gold_load_ts
        FROM {qualified_table("postcode")}
        ORDER BY postal_code
        """,
        PostCodeRead,
    )
