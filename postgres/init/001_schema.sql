-- ============================================================
-- Skema Postgres "gold" layer - salinan transaksional dari BigQuery
-- dataset lov_gold, disinkronin lewat scripts/sync_bigquery_to_postgres.py
-- (full refresh: truncate + reload, dijalanin terjadwal/manual).
--
-- Kolom & tipe SENGAJA disamain persis sama skema live BigQuery per
-- 2026-07-30 (lihat dummy/ddl-dml-company-atwork-v3.txt buat versi
-- BigQuery-nya). Kalau skema BigQuery berubah lagi, file ini juga
-- harus di-update biar sync job ga gagal insert.
-- ============================================================

CREATE TABLE IF NOT EXISTS gold_employer_profile (
  employer_id          TEXT PRIMARY KEY,
  group_id             TEXT,
  nob_id               TEXT,
  cif                  TEXT NOT NULL,
  employer_name        TEXT NOT NULL,
  employer_code        TEXT,
  industry             TEXT,
  tiering_code         TEXT,
  tiering_label        TEXT,
  group_name           TEXT,
  primary_email        TEXT,
  primary_contact_no   TEXT,
  snapshot_date        DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS gold_employer_account (
  account_id                       TEXT PRIMARY KEY,
  cif                              TEXT,
  employer_id                      TEXT REFERENCES gold_employer_profile(employer_id),
  employer_name                    TEXT,
  group_id                         TEXT,
  group_name                       TEXT,
  branch_code                      TEXT,
  branch_name                      TEXT,
  branch_address_detail            TEXT,
  branch_address_village_district  TEXT,
  branch_address_city              TEXT,
  branch_address_province          TEXT,
  branch_telephone                 TEXT,
  branch_email                     TEXT,
  account_number                   TEXT,
  currency                         TEXT,
  product_code                     TEXT,
  is_sharia                        BOOLEAN,
  snapshot_date                    DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS gold_stakeholder (
  stakeholder_id        TEXT PRIMARY KEY,
  cif                   TEXT,
  employer_id           TEXT NOT NULL REFERENCES gold_employer_profile(employer_id),
  employer_name         TEXT,
  group_id              TEXT,
  group_name            TEXT,
  stock_code            TEXT,
  industry              TEXT,
  shareholder_type      TEXT,
  stakeholder_name      TEXT,
  ownership_amount      NUMERIC,
  ownership_percentage  NUMERIC,
  designation           TEXT,
  snapshot_date         DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS gold_address (
  address_id      TEXT PRIMARY KEY,
  employer_id     TEXT NOT NULL REFERENCES gold_employer_profile(employer_id),
  cif             TEXT,
  postcode_id     TEXT,
  postcode        TEXT,
  is_primary      BOOLEAN,
  rt              TEXT,
  rw              TEXT,
  address_detail  TEXT,
  subdistrict     TEXT,
  district        TEXT,
  city            TEXT,
  province        TEXT,
  snapshot_date   DATE NOT NULL
);
