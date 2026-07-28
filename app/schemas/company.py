from datetime import date

from pydantic import BaseModel


class EmployerProfileRead(BaseModel):
    employer_id: str
    group_id: str | None = None
    nob_id: str | None = None
    cif: str
    employer_name: str
    employer_code: str | None = None
    industry: str | None = None
    tiering_code: str | None = None
    tiering_label: str | None = None
    group_name: str | None = None
    primary_email: str | None = None
    primary_contact_no: str | None = None
    snapshot_date: date


class PaginatedEmployers(BaseModel):
    items: list[EmployerProfileRead]
    total: int
    page: int
    page_size: int


class EmployerAccountRead(BaseModel):
    account_id: str
    cif: str | None = None
    employer_id: str | None = None
    employer_name: str | None = None
    group_id: str | None = None
    group_name: str | None = None
    branch_code: str | None = None
    branch_name: str | None = None
    branch_address1: str | None = None
    branch_address2: str | None = None
    branch_telephone: str | None = None
    branch_email: str | None = None
    account_number: str | None = None
    currency: str | None = None
    product_code: str | None = None
    account_type: str | None = None
    is_sharia: bool | None = None
    snapshot_date: date


class StakeholderRead(BaseModel):
    stakeholder_id: str
    cif: str | None = None
    employer_id: str
    employer_name: str | None = None
    group_id: str | None = None
    group_name: str | None = None
    stock_code: str | None = None
    industry: str | None = None
    shareholder_type: str | None = None
    stakeholder_name: str | None = None
    ownership_amount: float | None = None
    ownership_percentage: float | None = None
    designation: str | None = None
    snapshot_date: date


class AddressRead(BaseModel):
    address_id: str
    employer_id: str
    cif: str | None = None
    postcode_id: str | None = None
    postcode: str | None = None
    is_primary: bool | None = None
    rt: str | None = None
    rw: str | None = None
    address_detail: str | None = None
    subdistrict: str | None = None
    district: str | None = None
    city: str | None = None
    province: str | None = None
    snapshot_date: date
