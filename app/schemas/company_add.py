from datetime import date

from pydantic import BaseModel


class CompanyAddRead(BaseModel):
    address_type: str
    create_date: date
    create_by: str
    update_date: date
    update_by: str
    id_post_code: int