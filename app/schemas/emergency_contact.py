from datetime import date, datetime

from pydantic import BaseModel


class EmergencyContactRead(BaseModel):
    emer_cont_id: str
    master_code: str | None = None
    source_system: str | None = None
    original_code: str | None = None
    original_contact_name: str | None = None
    effective_date: date | None = None
    expiry_date: date | None = None
    is_current: bool | None = None
    original_destination_code: str | None = None
    original_phone_number: str | None = None
    original_phone_number_extension: str | None = None
    original_phone_type: str | None = None
    original_sequence: int | None = None
    create_date: datetime | None = None
    create_by: str | None = None
    update_date: datetime | None = None
    update_by: str | None = None
