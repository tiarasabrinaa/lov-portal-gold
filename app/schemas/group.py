from datetime import datetime

from pydantic import BaseModel


class GroupRead(BaseModel):
    group_id: str
    comp_id: str
    parent_comp_id: str | None = None
    group_name: str | None = None
    relationship_type: str | None = None
    ownership_level: int | None = None
    gold_load_ts: datetime
