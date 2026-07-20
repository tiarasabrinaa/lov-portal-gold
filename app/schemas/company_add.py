from datetime import datetime

from pydantic import BaseModel


class CompanyAddRead(BaseModel):
    addr_id: str
    comp_id: str
    addr_type: str | None = None
    address_line: str | None = None
    rt_rw: str | None = None
    kelurahan: str | None = None
    kecamatan: str | None = None
    kabupaten_kota: str | None = None
    provinsi: str | None = None
    postal_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_primary: bool | None = None
    gold_load_ts: datetime
