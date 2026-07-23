from fastapi import APIRouter, Depends, HTTPException
from google.cloud import bigquery

from app.core.database import get_db, qualified_table, run_query
from app.schemas.company import CompanyRead

router = APIRouter()

_EMPLOYER_COLUMNS = """
  employer_id,
  group_id,
  nob_id,
  cif,
  employer_name,
  employer_code,
  stock_code,
  ipo_date,
  sector,
  sub_sector,
  industry                     STRING,
  subindustry                  STRING,
  kbli                         STRING,
  is_top_1000                  BOOL,
  is_pks                       BOOL,
  tier                         STRING,
  group_name                   STRING,
  primary_email                STRING,
  primary_contact_no           STRING,
  cl_account                   STRING,
  cl_loan_type                 STRING,
  shareholder_count            INT64,
  top_shareholder_name         STRING,
  top_shareholder_percentage   NUMERIC,
  account_count                INT64,
  primary_address_postcode     STRING,
  primary_address_rt           STRING,
  primary_address_rw           STRING,
  primary_address_detail       STRING,
  primary_address_subdistrict  STRING,
  primary_address_district,
  primary_address_city,
  primary_address_province,
  snapshot_date
"""


@router.get("/", summary="Get company data")
async def get_company_data(client: bigquery.Client = Depends(get_db)) -> list[CompanyRead]:
    query = f"""
        SELECT
            {_EMPLOYER_COLUMNS}
        FROM {qualified_table("employer")}
        ORDER BY employer_name
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
            {_EMPLOYER_COLUMNS}
        FROM {qualified_table("employer")}
        WHERE LOWER(employer_name) LIKE LOWER(@q)
        ORDER BY employer_name
        LIMIT @limit
    """
    params = [
        bigquery.ScalarQueryParameter("q", "STRING", f"%{q}%"),
        bigquery.ScalarQueryParameter("limit", "INT64", limit),
    ]
    rows = await run_query(client, query, params)
    return [CompanyRead(**row) for row in rows]


@router.get("/by-region", summary="Search company by city and/or province")
async def get_company_by_region(
    city: str | None = None,
    province: str | None = None,
    client: bigquery.Client = Depends(get_db),
) -> list[CompanyRead]:
    if not city and not province:
        raise HTTPException(status_code=400, detail="Provide at least one of: city, province")

    conditions = []
    params: list[bigquery.ScalarQueryParameter] = []
    if city:
        conditions.append("LOWER(primary_address_city) = LOWER(@city)")
        params.append(bigquery.ScalarQueryParameter("city", "STRING", city))
    if province:
        conditions.append("LOWER(primary_address_province) = LOWER(@province)")
        params.append(bigquery.ScalarQueryParameter("province", "STRING", province))

    query = f"""
        SELECT
            {_EMPLOYER_COLUMNS}
        FROM {qualified_table("employer")}
        WHERE {" AND ".join(conditions)}
        ORDER BY employer_name
    """
    rows = await run_query(client, query, params)
    return [CompanyRead(**row) for row in rows]


@router.get("/by-cif-status", summary="Filter company by whether CIF is present")
async def get_company_by_cif_status(
    has_cif: bool = True,
    client: bigquery.Client = Depends(get_db),
) -> list[CompanyRead]:
    condition = "cif IS NOT NULL AND cif != ''" if has_cif else "cif IS NULL OR cif = ''"
    query = f"""
        SELECT
            {_EMPLOYER_COLUMNS}
        FROM {qualified_table("employer")}
        WHERE {condition}
        ORDER BY employer_name
    """
    rows = await run_query(client, query)
    return [CompanyRead(**row) for row in rows]
