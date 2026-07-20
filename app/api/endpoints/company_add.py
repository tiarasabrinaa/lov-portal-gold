from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table
from app.schemas.company_add import CompanyAddRead

router = APIRouter()


@router.get("/", summary="Get all company address data")
async def get_all_company_add(client: bigquery.Client = Depends(get_db)) -> list[CompanyAddRead]:
    return await fetch_all(
        client,
        f"""
        SELECT
            addr_id,
            comp_id,
            addr_type,
            address_line,
            rt_rw,
            kelurahan,
            kecamatan,
            kabupaten_kota,
            provinsi,
            postal_code,
            latitude,
            longitude,
            is_primary,
            gold_load_ts
        FROM {qualified_table("comp_addr")}
        ORDER BY comp_id, addr_type
        """,
        CompanyAddRead,
    )
