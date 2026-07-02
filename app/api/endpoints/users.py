from fastapi import APIRouter

router = APIRouter()


@router.get("/me", summary="Get current user")
def read_current_user() -> dict[str, str]:
    return {"id": "demo-user", "email": "demo@example.com"}


@router.get("/profile", summary="Get profile summary")
def read_profile() -> dict[str, str]:
    return {"display_name": "Demo User", "role": "customer"}