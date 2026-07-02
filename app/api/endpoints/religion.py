from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db
from app.schemas.religion import ReligionRead

router = APIRouter()


@router.get("/", summary="Get all religion data")
async def get_all_religion(db: AsyncSession = Depends(get_db)) -> list[ReligionRead]:
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
        FROM gold_religion
        ORDER BY master_code
        """,
        ReligionRead,
    )