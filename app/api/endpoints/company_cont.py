from fastapi import APIRouter, Depends, Path
from google.cloud import bigquery

from app.core.database import get_db, qualified_table, run_query
from app.schemas.company_cont import CompanyContRead

router = APIRouter()


@router.get("/{code}/contacts", summary="Get contact data by company")
async def get_company_contacts(
    code: str = Path(..., min_length=1, description="Company stock code"),
    client: bigquery.Client = Depends(get_db),
) -> list[CompanyContRead]:
    query = f"""
        SELECT
            ec.contact_id,
            ec.employer_id,
            ec.contact_type,
            ec.contact_value,
            ec.is_primary,
            ec.snapshot_date
        FROM {qualified_table("employer_contact")} ec
        JOIN {qualified_table("employer")} e ON e.employer_id = ec.employer_id
        WHERE e.stock_code = @code
        ORDER BY ec.employer_id, ec.contact_type
    """
    params = [bigquery.ScalarQueryParameter("code", "STRING", code)]
    rows = await run_query(client, query, params)
    return [CompanyContRead(**row) for row in rows]
