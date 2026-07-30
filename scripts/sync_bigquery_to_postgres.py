"""Sync BigQuery (gold_* tables, lov_gold dataset) -> Postgres (transactional copy).

Strategi: FULL REFRESH. Tiap tabel di-truncate lalu diisi ulang total dari
BigQuery - lebih simpel & lebih aman dibanding "update yang berubah doang"
(ga ada risiko baris yang kelewat). Cocok karena BigQuery cuma berubah
per periode tertentu (bukan tiap detik), jadi ga masalah kalau Postgres
"diganti total" tiap kali sync jalan.

Jalanin manual:
    docker exec lov-portal-api python3 scripts/sync_bigquery_to_postgres.py

Nanti di production, script ini yang dibungkus jadi image buat Cloud Run
Job, dipicu Cloud Scheduler on a schedule (misal bulanan).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import psycopg  # noqa: E402

from app.core.config import settings  # noqa: E402
from app.core.database import get_bq_client, qualified_table  # noqa: E402

# Urutan INSERT (parent dulu baru child, sesuai FK) dan urutan TRUNCATE
# (child dulu baru parent, biar ga kena constraint violation).
TABLES_PARENT_TO_CHILD = [
    "gold_employer_profile",
    "gold_employer_account",
    "gold_stakeholder",
    "gold_address",
]

TABLE_COLUMNS = {
    "gold_employer_profile": [
        "employer_id", "group_id", "nob_id", "cif", "employer_name", "employer_code",
        "industry", "tiering_code", "tiering_label", "group_name",
        "primary_email", "primary_contact_no", "snapshot_date",
    ],
    "gold_employer_account": [
        "account_id", "cif", "employer_id", "employer_name", "group_id", "group_name",
        "branch_code", "branch_name", "branch_address_detail", "branch_address_village_district",
        "branch_address_city", "branch_address_province", "branch_telephone", "branch_email",
        "account_number", "currency", "product_code", "is_sharia", "snapshot_date",
    ],
    "gold_stakeholder": [
        "stakeholder_id", "cif", "employer_id", "employer_name", "group_id", "group_name",
        "stock_code", "industry", "shareholder_type", "stakeholder_name",
        "ownership_amount", "ownership_percentage", "designation", "snapshot_date",
    ],
    "gold_address": [
        "address_id", "employer_id", "cif", "postcode_id", "postcode", "is_primary",
        "rt", "rw", "address_detail", "subdistrict", "district", "city", "province",
        "snapshot_date",
    ],
}


def _pg_conninfo() -> str:
    return (
        f"host={settings.postgres_host} port={settings.postgres_port} "
        f"dbname={settings.postgres_db} user={settings.postgres_user} "
        f"password={settings.postgres_password}"
    )


def fetch_bq_rows(table: str) -> list[dict]:
    client = get_bq_client()
    columns = ", ".join(TABLE_COLUMNS[table])
    query = f"SELECT {columns} FROM {qualified_table(table)}"
    return [dict(row.items()) for row in client.query(query).result()]


def sync() -> None:
    with psycopg.connect(_pg_conninfo()) as pg_conn:
        with pg_conn.cursor() as cur:
            # Truncate child -> parent biar ga kena FK constraint violation.
            for table in reversed(TABLES_PARENT_TO_CHILD):
                cur.execute(f"TRUNCATE TABLE {table} CASCADE")

            total = 0
            for table in TABLES_PARENT_TO_CHILD:
                rows = fetch_bq_rows(table)
                columns = TABLE_COLUMNS[table]
                placeholders = ", ".join(["%s"] * len(columns))
                col_list = ", ".join(columns)
                insert_sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})"

                values = [tuple(row[col] for col in columns) for row in rows]
                if values:
                    cur.executemany(insert_sql, values)

                print(f"{table}: {len(rows)} baris disync dari BigQuery")
                total += len(rows)

        pg_conn.commit()
    print(f"Selesai. Total {total} baris disync ke Postgres.")


if __name__ == "__main__":
    sync()
