from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db
from app.schemas.post_code import PostCodeRead

router = APIRouter()


@router.get("/", summary="Get all post code data")
async def get_all_post_code(db: AsyncSession = Depends(get_db)) -> list[PostCodeRead]:
    return await fetch_all(
        db,
        """
        SELECT
            kode_pos,
            kode_kemendagri,
            kode_dati,
            kelurahan,
            kecamatan,
            kota_kabupaten,
            provinsi,
            create_date,
            create_by,
            update_date,
            update_by
        FROM gold_post_code
        ORDER BY kode_pos
        """,
        PostCodeRead,
    )