from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.company import CompanyRead

router = APIRouter()


@router.get("/", summary="Get company data")
async def get_company_data(db: AsyncSession = Depends(get_db)) -> list[CompanyRead]:
    query = text(
        """
        SELECT
            stock_code,
            company_name,
            company_number,
            ipo_date,
            is_top_1000,
            is_pks,
            kota_kabupaten,
            create_date,
            create_by,
            update_date,
            update_by,
            id_group
        FROM gold_company
        ORDER BY id_group, stock_code
        """
    )
    result = await db.execute(query)
    rows = result.mappings().all()
    return [CompanyRead(**row) for row in rows]

@router.get("/search", summary="Search company by name")
async def search_company(
    q: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
) -> list[CompanyRead]:
    query = text(
        """
        SELECT
            stock_code, company_name, company_number, ipo_date,
            is_top_1000, is_pks, kota_kabupaten, create_date,
            create_by, update_date, update_by, id_group
        FROM gold_company
        WHERE LOWER(company_name) LIKE LOWER(:q)
        ORDER BY company_name
        LIMIT :limit
        """
    )
    result = await db.execute(query, {"q": f"%{q}%", "limit": limit})
    rows = result.mappings().all()
    return [CompanyRead(**row) for row in rows]