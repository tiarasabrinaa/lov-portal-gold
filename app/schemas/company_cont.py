from datetime import date

from pydantic import BaseModel


class CompanyContRead(BaseModel):
    contact_id: str
    employer_id: str
    contact_type: str | None = None
    contact_value: str | None = None
    is_primary: bool | None = None
    snapshot_date: date | None = None
