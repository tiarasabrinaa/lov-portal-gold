from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.core.database import get_db, qualified_table, run_query
from app.schemas.company import CompanyRead

router = APIRouter()

@router.get("/", summary="Get company data")
async def get_company_data(client: bigquery.Client = Depends(get_db)) -> list[CompanyRead]:
    query = f"""
        SELECT
            comp_id,
            comp_code,
            comp_name,
            comp_short_name,
            comp_type,
            npwp,
            nib,
            kbli_code,
            industry_sector,
            incorporation_date,
            comp_status,
            source_system,
            gold_load_ts
        FROM {qualified_table("comp")}
        ORDER BY comp_name
    """
    rows = await run_query(client, query)
    return [CompanyRead(**row) for row in rows]


@router.get("/search", summary="Search company by name")
async def search_company(
    q: str,
    limit: int = 10,
    client: bigquery.Client = Depends(get_db),
) -> list[CompanyRead]:
    query = f"""
        SELECT
            comp_id,
            comp_code,
            comp_name,
            comp_short_name,
            comp_type,
            npwp,
            nib,
            kbli_code,
            industry_sector,
            incorporation_date,
            comp_status,
            source_system,
            gold_load_ts
        FROM {qualified_table("comp")}
        WHERE LOWER(comp_name) LIKE LOWER(@q)
        ORDER BY comp_name
        LIMIT @limit
    """
    params = [
        bigquery.ScalarQueryParameter("q", "STRING", f"%{q}%"),
        bigquery.ScalarQueryParameter("limit", "INT64", limit),
    ]
    rows = await run_query(client, query, params)
    return [CompanyRead(**row) for row in rows]
