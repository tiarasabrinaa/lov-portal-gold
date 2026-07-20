from fastapi import APIRouter, Depends, Path
from google.cloud import bigquery

from app.core.database import get_db, qualified_table, run_query
from app.schemas.company_cont import CompanyContRead

router = APIRouter()


@router.get("/{code}/contacts", summary="Get contact data by company")
async def get_company_contacts(
    code: str = Path(..., min_length=1, description="Company code (comp_code)"),
    client: bigquery.Client = Depends(get_db),
) -> list[CompanyContRead]:
    query = f"""
        SELECT
            cc.cont_id,
            cc.comp_id,
            cc.contact_type,
            cc.contact_value,
            cc.pic_name,
            cc.is_primary,
            cc.gold_load_ts
        FROM {qualified_table("comp_cont")} cc
        JOIN {qualified_table("comp")} c ON c.comp_id = cc.comp_id
        WHERE c.comp_code = @code
        ORDER BY cc.comp_id, cc.contact_type
    """
    params = [bigquery.ScalarQueryParameter("code", "STRING", code)]
    rows = await run_query(client, query, params)
    return [CompanyContRead(**row) for row in rows]
