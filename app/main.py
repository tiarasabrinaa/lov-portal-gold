import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google.api_core.exceptions import GoogleAPIError

from app.api.router import api_router, api_router_v2

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

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    elapsed = time.time() - start_time
    print(f"{request.method} {request.url.path} took {elapsed:.4f} seconds")
    return response


app.include_router(api_router, prefix="/lov/v1")
app.include_router(api_router_v2, prefix="/lov/v2")


@app.exception_handler(GoogleAPIError)
async def handle_bigquery_error(request: Request, exc: GoogleAPIError) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": f"Gagal ambil data dari BigQuery: {exc}"})


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {"message": "LOV Portal API is running"}
