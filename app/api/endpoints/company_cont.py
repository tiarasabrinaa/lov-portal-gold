from fastapi import APIRouter, Depends, Path
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.company_cont import CompanyContRead

router = APIRouter()


@router.get("/{id_company}", summary="Get contact data by company")
async def get_all_company_cont(
    id_company: int = Path(..., gt=0, description="Company ID"),
    db: AsyncSession = Depends(get_db),
) -> list[CompanyContRead]:
    query = text(
        """
        SELECT
            contact_type,
            contact_value,
            create_date,
            create_by,
            update_date,
            update_by,
            id_company
        FROM gold_company_cont
        WHERE id_company = :id_company
        ORDER BY id_company, contact_type
        """
    )
    result = await db.execute(query, {"id_company": id_company})
    rows = result.mappings().all()
    return [CompanyContRead(**row) for row in rows]

