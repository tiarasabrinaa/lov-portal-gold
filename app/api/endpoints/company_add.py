from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db
from app.schemas.company_add import CompanyAddRead

router = APIRouter()


@router.get("/", summary="Get all company address data")
async def get_all_company_add(db: AsyncSession = Depends(get_db)) -> list[CompanyAddRead]:
    return await fetch_all(
        db,
        """
        SELECT
            address_type,
            create_date,
            create_by,
            update_date,
            update_by,
            id_post_code
        FROM gold_company_add
        ORDER BY id_post_code, address_type
        """,
        CompanyAddRead,
    )