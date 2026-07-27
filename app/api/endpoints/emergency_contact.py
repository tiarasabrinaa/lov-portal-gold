from fastapi import APIRouter, Depends
from google.cloud import bigquery

from app.api.endpoints._helpers import fetch_all
from app.core.database import get_db, qualified_table
from app.schemas.emergency_contact import EmergencyContactRead

router = APIRouter()

@router.get("/", summary="Get all emergency contact data")
async def get_all_emergency_contact(client: bigquery.Client = Depends(get_db)) -> list[EmergencyContactRead]:
    return await fetch_all(
        client,
        f"""    
        SELECT
            emer_cont_id,
            master_code,
            source_system,
            original_code,
            original_contact_name,
            effective_date,
            expiry_date,
            is_current,
            original_destination_code,
            original_phone_number,
            original_phone_number_extension,
            original_phone_type,
            original_sequence,
            create_date,
            create_by,
            update_date,
            update_by
        FROM {qualified_table("emergency_contact")}
        ORDER BY master_code
        """,
        EmergencyContactRead,
    )
