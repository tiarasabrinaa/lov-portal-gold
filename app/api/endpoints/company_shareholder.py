from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.core.database import get_db, qualified_table, run_query
from app.schemas.shareholder import ShareholderRead

router = APIRouter()


@router.get("/shareholders/top", summary="Get top shareholders by amount")
async def get_top_shareholders(
    limit: int = 10,
    client: bigquery.Client = Depends(get_db),
) -> list[ShareholderRead]:
    query = f"""
        SELECT
            s.shareholder_id,
            s.employer_id,
            e.employer_name,
            s.shareholder_name,
            s.shareholder_amount,
            s.shareholder_percentage,
            s.shareholder_type,
            s.snapshot_date
        FROM {qualified_table("employer_shareholder")} s
        JOIN {qualified_table("employer")} e ON e.employer_id = s.employer_id
        ORDER BY s.shareholder_amount DESC
        LIMIT @limit
    """
    params = [bigquery.ScalarQueryParameter("limit", "INT64", limit)]
    rows = await run_query(client, query, params)
    return [ShareholderRead(**row) for row in rows]
