from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db
from app.schemas.education import EducationRead

router = APIRouter()


@router.get("/", summary="Get all education data")
async def get_all_education(db: AsyncSession = Depends(get_db)) -> list[EducationRead]:
    return await fetch_all(
        db,
        """
        SELECT
            master_code,
            source_system,
            original_code,
            original_description,
            create_date,
            create_by,
            update_date,
            update_by
        FROM gold_education
        ORDER BY master_code
        """,
        EducationRead,
    )

@router.get("/{master_code}", summary="Get education data by master code")
async def get_education_by_master_code(master_code: str, db: AsyncSession = Depends(get_db)) -> list[EducationRead]:
    return await fetch_all(
        db,
        """
        SELECT
            master_code,
            source_system,
            original_code,
            original_description,
            create_date,
            create_by,
            update_date,
            update_by
        FROM gold_education
        WHERE master_code = :master_code
        ORDER BY master_code
        """,
        EducationRead,
        {"master_code": master_code},
    ) 