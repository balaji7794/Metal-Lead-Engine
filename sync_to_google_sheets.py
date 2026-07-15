import sqlite3
import gspread
from google.oauth2.service_account import Credentials

# -----------------------------
# CONFIGURATION
# -----------------------------
DB_PATH = "database/metal_leads.db"

GOOGLE_SHEET_ID = "1yNHuLQZuFPImBAoc1phm1pYMMOZLQSkBy00I0AHT8pc"

CREDENTIALS_FILE = "credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# -----------------------------
# CONNECT SQLITE
# -----------------------------
print("Connecting to SQLite...")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("✓ SQLite Connected")

# -----------------------------
# CONNECT GOOGLE SHEETS
# -----------------------------
print("Connecting to Google Sheets...")

credentials = Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=SCOPES
)

client = gspread.authorize(credentials)

spreadsheet = client.open_by_key(GOOGLE_SHEET_ID)

print("✓ Google Sheets Connected")

# -----------------------------
# SHOW WORKSHEETS
# -----------------------------
print("\nWorksheets Found:\n")

for ws in spreadsheet.worksheets():
    print("-", ws.title)

# -----------------------------
# READ COMPANIES
# -----------------------------
print("\nReading companies from SQLite...\n")

cursor.execute("""
SELECT
    c.id,
    c.company_code,
    c.company_name,
    c.google_maps_url,

    GROUP_CONCAT(DISTINCT cw.website) AS websites,
    GROUP_CONCAT(DISTINCT cp.phone) AS phones,
    GROUP_CONCAT(DISTINCT ce.email) AS emails,

    c.address,
    c.city,
    c.state,
    c.country,
    c.pincode,
    c.category,
    c.industry_type,
    c.business_type,
    c.msme_type,
    c.products,
    c.scrap_generated,
    c.estimated_consumption_mt,
    c.estimated_scrap_mt,
    c.rating,
    c.reviews,
    c.source,
    c.notes,
    c.lead_status,
    c.priority,
    c.last_contacted,
    c.next_followup,
    c.remarks,
    c.status,
    c.confidence_score,
    c.created_at,
    c.updated_at

FROM companies c

LEFT JOIN company_emails ce
    ON ce.company_id = c.id

LEFT JOIN company_phones cp
    ON cp.company_id = c.id

LEFT JOIN company_websites cw
    ON cw.company_id = c.id

GROUP BY c.id

ORDER BY c.id;
""")

rows = cursor.fetchall()

print(f"Total Companies Found : {len(rows)}")

# -----------------------------
# DATA WORKSHEET
# -----------------------------
worksheet = spreadsheet.worksheet("Data")

print("\nReading existing IDs from Google Sheets...")

existing_ids = set()

values = worksheet.get_all_values()

if len(values) > 1:
    for value in values[1:]:
        if value and value[0].strip():
            existing_ids.add(value[0].strip())

print(f"Existing Rows : {len(existing_ids)}")

# -----------------------------
# PREVIEW
# -----------------------------
if rows:

    print("\nFirst 5 Companies:\n")

    for row in rows[:5]:

        print(f"ID           : {row[0]}")
        print(f"Company Code : {row[1]}")
        print(f"Company Name : {row[2]}")
        print(f"Websites     : {row[4]}")
        print(f"Phones       : {row[5]}")
        print(f"Emails       : {row[6]}")
        print("-" * 60)

# -----------------------------
# SYNC
# -----------------------------
print("\nStarting Google Sheets Sync...\n")

rows_to_upload = []

uploaded = 0
skipped = 0
failed = 0

for row in rows:

    company_id = str(row[0])

    if company_id in existing_ids:
        skipped += 1
        continue

    rows_to_upload.append(list(row))

if rows_to_upload:

    try:

        worksheet.append_rows(
            rows_to_upload,
            value_input_option="RAW"
        )

        uploaded = len(rows_to_upload)

    except Exception as e:

        failed = len(rows_to_upload)

        print("\nERROR")
        print(e)

print("\n===================================")
print("SYNC COMPLETE")
print("===================================")

print(f"SQLite Companies : {len(rows)}")
print(f"Already Exists   : {skipped}")
print(f"Uploaded         : {uploaded}")
print(f"Failed           : {failed}")

conn.close()

print("\nDone.")