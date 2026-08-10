from datetime import date

from pydantic import BaseModel


class NatureOfBusinessRead(BaseModel):
    nob_id: str
    master_code: str | None = None
    master_description: str | None = None
    source_system: str | None = None
    original_code: str | None = None
    original_description: str | None = None
    snapshot_date: date | None = None
