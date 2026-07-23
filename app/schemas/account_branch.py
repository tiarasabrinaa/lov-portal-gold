from datetime import date

from pydantic import BaseModel


class AccountBranchRead(BaseModel):
    account_id: str
    cif: str | None = None
    branch_code: str | None = None
    employer_name: str | None = None
    group_name: str | None = None
    account_number: str | None = None
    currency: str | None = None
    product_code: str | None = None
    account_type: str | None = None
    creation_bank_no: str | None = None
    is_sharia: bool | None = None
    branch_name: str | None = None
    branch_address1: str | None = None
    branch_address2: str | None = None
    branch_telephone: str | None = None
    branch_email: str | None = None
    primary_address_postcode: str | None = None
    primary_address_rt_rw: str | None = None
    primary_address_detail: str | None = None
    primary_address_subdistrict: str | None = None
    primary_address_district: str | None = None
    primary_address_city: str | None = None
    primary_address_province: str | None = None
    snapshot_date: date
