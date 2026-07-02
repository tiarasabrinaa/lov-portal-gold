from datetime import date

from pydantic import BaseModel


class PostCodeRead(BaseModel):
    kode_pos: str
    kode_kemendagri: str
    kode_dati: str
    kelurahan: str
    kecamatan: str
    kota_kabupaten: str
    provinsi: str
    create_date: date
    create_by: str
    update_date: date
    update_by: str