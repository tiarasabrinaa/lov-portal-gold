from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db
from app.schemas.group import GroupRead

router = APIRouter()


@router.get("/", summary="Get all group data")
async def get_all_group(db: AsyncSession = Depends(get_db)) -> list[GroupRead]:
    return await fetch_all(
        db,
        """
        SELECT
            group_code,
            group_name,
            create_date,
            create_by,
            update_date,
            update_by
        FROM gold_group
        ORDER BY group_code
        """,
        GroupRead,
    )