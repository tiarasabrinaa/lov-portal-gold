from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router

app = FastAPI(
    title="LOV Portal API",
    version="0.1.0",
    description="FastAPI scaffold with Swagger UI enabled for API development.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/lov/v1")


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {"message": "LOV Portal API is running"}
