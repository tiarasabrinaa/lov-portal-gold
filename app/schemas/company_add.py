from datetime import date

from pydantic import BaseModel


class CompanyAddRead(BaseModel):
    address_id: str
    employer_id: str
    address_type: str | None = None
    address_detail: str | None = None
    subdistrict: str | None = None
    district: str | None = None
    city: str | None = None
    province: str | None = None
    postcode: str | None = None
    postcode_id: str | None = None
    is_primary: bool | None = None
    is_current: bool | None = None
    effective_date: date | None = None
    expiry_date: date | None = None
