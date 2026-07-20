from datetime import datetime

from pydantic import BaseModel


class PostCodeRead(BaseModel):
    postal_code: str
    kelurahan: str | None = None
    kecamatan: str | None = None
    kabupaten_kota: str | None = None
    provinsi: str | None = None
    gold_load_ts: datetime
