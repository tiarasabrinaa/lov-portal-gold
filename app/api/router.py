from fastapi import APIRouter

from app.api.endpoints.company import router as company_router
from app.api.endpoints.company_cif import router as company_cif_router
from app.api.endpoints.company_cif_v2 import router as company_cif_v2_router
from app.api.endpoints.company_v2 import router as company_v2_router
from app.api.endpoints.education import router as education_router
from app.api.endpoints.emergency_contact import router as emergency_contact_router
from app.api.endpoints.group import router as group_router
from app.api.endpoints.job_title import router as job_title_router
from app.api.endpoints.health import router as health_router
from app.api.endpoints.nature_of_business import router as nature_of_business_router
from app.api.endpoints.occupation import router as occupation_router
from app.api.endpoints.post_code import router as post_code_router
from app.api.endpoints.religion import router as religion_router
from app.api.endpoints.users import router as users_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(company_router, prefix="/company", tags=["company"])
# company_cif_router (endpoint /{cif}) HARUS didaftarin SETELAH company_router -
# supaya path statis kayak /company/employers/by-name & /by-employer-id/{id}
# ke-match duluan, bukan ketangkep sama {cif} yang sifatnya catch-all.
api_router.include_router(company_cif_router, prefix="/company", tags=["company_cif"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(post_code_router, prefix="/post-codes", tags=["post-code"])
api_router.include_router(group_router, prefix="/groups", tags=["group"])
api_router.include_router(religion_router, prefix="/religions", tags=["religion"])
api_router.include_router(job_title_router, prefix="/job-titles", tags=["job-title"])
api_router.include_router(emergency_contact_router, prefix="/emergency-contacts", tags=["emergency-contact"])
api_router.include_router(education_router, prefix="/educations", tags=["education"])
api_router.include_router(occupation_router, prefix="/occupations", tags=["occupation"])
api_router.include_router(nature_of_business_router, prefix="/nature-of-businesses", tags=["nature-of-business"])


# ------------------------------------------------------------
# v2: BigQuery + Redis cache - buat banding-bandingin sama v1 (pure
# BigQuery, no Redis/Postgres) di company.py/company_cif.py. Mounted
# terpisah di /lov/v2 lewat app.main, router ini cuma isi company +
# company_cif soalnya cuma itu yang punya varian pure (v1) vs cached (v2).
# ------------------------------------------------------------
api_router_v2 = APIRouter()
api_router_v2.include_router(company_v2_router, prefix="/company", tags=["company_v2"])
# company_cif_v2_router (endpoint /{cif}) HARUS didaftarin SETELAH company_v2_router,
# alasan sama kayak v1 - biar path statis ke-match duluan.
api_router_v2.include_router(company_cif_v2_router, prefix="/company", tags=["company_cif_v2"])