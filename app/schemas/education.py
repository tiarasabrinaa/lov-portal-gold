from datetime import datetime

from pydantic import BaseModel


class EducationRead(BaseModel):
    education_id: str
    master_code: str | None = None
    source_system: str | None = None
    original_code: str | None = None
    original_description: str | None = None
    create_date: datetime | None = None
    create_by: str | None = None
    update_date: datetime | None = None
    update_by: str | None = None
