from datetime import date

from pydantic import BaseModel


class GroupRead(BaseModel):
    group_code: str
    group_name: str
    create_date: date
    create_by: str
    update_date: date
    update_by: str