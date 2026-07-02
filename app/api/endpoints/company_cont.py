from fastapi import APIRouter, Depends, Path
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.company_cont import CompanyContRead

router = APIRouter()


@router.get("/{code}/contacts", summary="Get contact data by company")
async def get_company_contacts(
    code: str = Path(..., min_length=1, description="Company stock code"),
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
            gcc.id_company
        FROM gold_company_cont gcc
        JOIN gold_company gc ON gc.id = gcc.id_company
        WHERE gc.stock_code = :code
        ORDER BY gcc.id_company, gcc.contact_type
        """
    )
    result = await db.execute(query, {"code": code})
    rows = result.mappings().all()
    return [CompanyContRead(**row) for row in rows]