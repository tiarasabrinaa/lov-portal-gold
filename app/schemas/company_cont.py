from datetime import date

from pydantic import BaseModel


class CompanyContRead(BaseModel):
    contact_type: str
    contact_value: str
    create_date: date
    create_by: str
    update_date: date
    update_by: str
    id_company: int