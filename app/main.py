from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google.api_core.exceptions import GoogleAPIError

from app.api.router import api_router

app = FastAPI(
    title="LOV Portal API",
    version="0.1.0",
    description="FastAPI for Serving Layer EDP-LoV to Surrounding.",
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


@app.exception_handler(GoogleAPIError)
async def handle_bigquery_error(request: Request, exc: GoogleAPIError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": f"Gagal ambil data dari BigQuery: {exc}"})


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {"message": "LOV Portal API is running"}
