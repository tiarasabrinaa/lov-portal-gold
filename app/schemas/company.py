from datetime import date

from pydantic import BaseModel


class CompanyRead(BaseModel):
    employer_id: str
    group_id: str | None = None
    nob_id: str | None = None
    cif: str
    employer_name: str
    employer_code: str | None = None
    stock_code: str | None = None
    ipo_date: date | None = None
    sector: str | None = None
    sub_sector: str | None = None
    industry: str | None = None
    subindustry: str | None = None
    kbli: str | None = None
    is_top_1000: bool | None = None
    is_pks: bool | None = None
    tier: str | None = None
    group_name: str | None = None
    primary_email: str | None = None
    primary_contact_no: str | None = None
    cl_account: str | None = None
    cl_loan_type: str | None = None
    shareholder_count: int | None = None
    top_shareholder_name: str | None = None
    top_shareholder_percentage: float | None = None
    account_count: int | None = None
    primary_address_postcode: str | None = None
    primary_address_rt: str | None = None
    primary_address_rw: str | None = None
    primary_address_detail: str | None = None
    primary_address_subdistrict: str | None = None
    primary_address_district: str | None = None
    primary_address_city: str | None = None
    primary_address_province: str | None = None
    snapshot_date: date
