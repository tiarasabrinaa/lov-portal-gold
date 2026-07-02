from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(
    title="LOV Portal API",
    version="0.1.0",
    description="FastAPI scaffold with Swagger UI enabled for API development.",
)

app.include_router(api_router, prefix="/lov/v1")


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {"message": "LOV Portal API is running"}
