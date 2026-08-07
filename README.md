# LOV Portal API

FastAPI scaffold ready for API development.

## Structure

- One router file per feature in `app/api/endpoints/`
- `/health` for readiness checks
- `/auth` for authentication flows
- `/checkout/get_data` for `gold_company`
- `/post-codes`, `/groups`, `/religions`, `/job-titles`, `/emergency-contacts`, `/educations`, `/occupations`, `/nature-of-businesses`, `/company-contacts`, `/company-addresses`

Copy `.env.example` to `.env` and set your BigQuery project/dataset/credentials. All data reads go straight to BigQuery - no Redis, no Postgres.

## Run

```bash
uvicorn app.main:app --reload
```

## Docker

```bash
docker compose up --build
```

Then open http://127.0.0.1:8000/docs

For daily development (hot reload, no rebuild on every code edit):

```bash
docker compose up
```

After that, just save file changes and refresh `/docs` or your endpoint request.

Rebuild is only needed when dependency or image-level files change, for example `requirements.txt` or `Dockerfile`.

## Docs

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
