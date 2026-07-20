from datetime import datetime

from pydantic import BaseModel


class CompanyContRead(BaseModel):
    cont_id: str
    comp_id: str
    contact_type: str | None = None
    contact_value: str | None = None
    pic_name: str | None = None
    is_primary: bool | None = None
    gold_load_ts: datetime
