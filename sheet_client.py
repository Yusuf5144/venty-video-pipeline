# sheet_client.py
from dotenv import load_dotenv
import os, gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), scope)
sheet = gspread.authorize(creds).open_by_key(os.getenv("SHEET_ID")).sheet1

def get_next_draft():
    for idx, row in enumerate(sheet.get_all_records(), start=2):
        if row.get("status","").lower() == "draft":
            return idx, row.get("skript","")
    return None, None

def update_row(row_idx, col_name, value):
    header = sheet.row_values(1)
    col = header.index(col_name) + 1
    sheet.update_cell(row_idx, col, value)
