from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest

router = APIRouter()


@router.post("/register", summary="Register a new user")
async def register_user(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    _ = db
    return {"message": f"User {payload.email} registered"}


@router.post("/login", summary="Login a user")
async def login_user(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    _ = db
    return {"message": f"User {payload.email} authenticated"}