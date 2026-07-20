from pydantic import BaseModel


class GroupRead(BaseModel):
    group_id: str
    group_name: str | None = None
