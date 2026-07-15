import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = "1yNHuLQZuFPImBAoc1phm1pYMMOZLQSkBy00I0AHT8pc"


class GoogleSheetsService:

    def __init__(self):
        credentials = Credentials.from_service_account_file(
            "credentials.json",
            scopes=SCOPES
        )

        self.client = gspread.authorize(credentials)
        self.sheet = self.client.open_by_key(SPREADSHEET_ID)

    def test_connection(self):
        worksheet_name = "Connection Test"

        try:
            worksheet = self.sheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = self.sheet.add_worksheet(
                title=worksheet_name,
                rows=100,
                cols=5
            )
            worksheet.append_row(
                ["Timestamp", "Status"]
            )

        worksheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Connected Successfully ✅"
        ])

        return True