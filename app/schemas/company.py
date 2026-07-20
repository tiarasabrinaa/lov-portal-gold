from datetime import date, datetime

from pydantic import BaseModel


class CompanyRead(BaseModel):
    comp_id: str
    comp_code: str | None = None
    comp_name: str
    comp_short_name: str | None = None
    comp_type: str | None = None
    npwp: str | None = None
    nib: str | None = None
    kbli_code: str | None = None
    industry_sector: str | None = None
    incorporation_date: date | None = None
    comp_status: str | None = None
    source_system: str | None = None
    gold_load_ts: datetime
