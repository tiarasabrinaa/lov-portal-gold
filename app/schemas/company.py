from datetime import date

from pydantic import BaseModel


class CompanyRead(BaseModel):
    employer_id: str
    group_id: str | None = None
    nob_id: str | None = None
    cif: str
    stock_code: str | None = None
    employer_name: str
    ipo_date: date | None = None
    is_top_1000: bool | None = None
    is_pks: bool | None = None
    tier: str | None = None
    group_name: str | None = None
    cl_account: str | None = None
    cl_loan_type: str | None = None
    primary_address_detail: str | None = None
    primary_address_subdistrict: str | None = None
    primary_address_district: str | None = None
    primary_address_city: str | None = None
    primary_address_province: str | None = None
    primary_address_postcode: str | None = None
    primary_contact: str | None = None
    shareholder_count: int | None = None
    top_shareholder_name: str | None = None
    top_shareholder_pct: float | None = None
    account_count: int | None = None
    primary_account_number: str | None = None
    snapshot_date: date
