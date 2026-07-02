from datetime import date

from pydantic import BaseModel


class OccupationRead(BaseModel):
    master_code: str
    source_system: str
    original_code: str
    original_description: str
    create_date: date
    create_by: str
    update_date: date
    update_by: str