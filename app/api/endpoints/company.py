from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.company import CompanyRead

router = APIRouter()


@router.get("/get_data", summary="Get company data")
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