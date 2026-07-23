from datetime import date

from pydantic import BaseModel


class CompanyAddRead(BaseModel):
    address_id: str
    postcode_id: str | None = None
    employer_id: str
    employer_name: str | None = None
    group_name: str | None = None
    address_type: str | None = None
    rt: str | None = None
    rw: str | None = None
    address_detail: str | None = None
    subdistrict: str | None = None
    district: str | None = None
    city: str | None = None
    province: str | None = None
    snapshot_date: date
