from datetime import date

from pydantic import BaseModel


class NatureOfBusinessRead(BaseModel):
    nob_id: str
    business_date: date | None = None
    int_indcode: str | None = None
    corp_short_desc: str | None = None
    corp_desc: str | None = None
    risk_level: str | None = None
    update_date: date | None = None
