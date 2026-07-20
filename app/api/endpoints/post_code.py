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
            post_code_id,
            kode_pos,
            kode_kemendagri,
            kode_dati,
            address_detail,
            subdistrict,
            district,
            city,
            province,
            val_kemendagri,
            val_pos,
            flag,
            create_date,
            create_by,
            update_date,
            update_by
        FROM {qualified_table("postcode")}
        ORDER BY kode_pos
        """,
        PostCodeRead,
    )
