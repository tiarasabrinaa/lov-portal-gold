from datetime import date

from pydantic import BaseModel


class ShareholderRead(BaseModel):
    shareholder_id: str
    employer_id: str
    employer_name: str
    shareholder_name: str | None = None
    shareholder_amount: float | None = None
    shareholder_percentage: float | None = None
    shareholder_type: str | None = None
    snapshot_date: date | None = None
