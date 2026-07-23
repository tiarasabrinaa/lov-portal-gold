from datetime import date

from pydantic import BaseModel


class OwnershipProfileRead(BaseModel):
    stakeholder_id: str
    employer_id: str
    employer_name: str | None = None
    stock_code: str | None = None
    group_name: str | None = None
    sector: str | None = None
    shareholder_type: str | None = None
    stakeholder_name: str | None = None
    ownership_amount: float | None = None
    ownership_percentage: float | None = None
    designation: str | None = None
    snapshot_date: date
