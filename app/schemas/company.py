from datetime import date

from pydantic import BaseModel


class CompanyRead(BaseModel):
    stock_code: str
    company_name: str
    company_number: str
    ipo_date: date
    is_top_1000: bool
    is_pks: bool
    kota_kabupaten: str
    create_date: date
    create_by: str
    update_date: date
    update_by: str
    id_group: int