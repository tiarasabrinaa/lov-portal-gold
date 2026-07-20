from datetime import date, datetime

from pydantic import BaseModel


class NatureOfBusinessRead(BaseModel):
    nob_id: str
    master_code: str | None = None
    source_system: str | None = None
    original_code: str | None = None
    original_sector: str | None = None
    original_sub_sector: str | None = None
    original_industry: str | None = None
    original_sub_industry: str | None = None
    kbli: str | None = None
    individual_type: str | None = None
    effective_date: date | None = None
    expiry_date: date | None = None
    is_current: bool | None = None
    create_date: datetime | None = None
    create_by: str | None = None
    update_date: datetime | None = None
    update_by: str | None = None
