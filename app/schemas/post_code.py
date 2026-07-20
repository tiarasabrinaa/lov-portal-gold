from datetime import datetime

from pydantic import BaseModel


class PostCodeRead(BaseModel):
    post_code_id: str
    kode_pos: str | None = None
    kode_kemendagri: str | None = None
    kode_dati: str | None = None
    address_detail: str | None = None
    subdistrict: str | None = None
    district: str | None = None
    city: str | None = None
    province: str | None = None
    val_kemendagri: str | None = None
    val_pos: str | None = None
    flag: str | None = None
    create_date: datetime | None = None
    create_by: str | None = None
    update_date: datetime | None = None
    update_by: str | None = None
