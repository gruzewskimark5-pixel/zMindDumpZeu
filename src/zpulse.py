import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zPulse")

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    logger.warning("Google libraries not found. Running in mock mode.")

class ZPulseClient:
    def __init__(self, credentials_path="google-credentials.json", sheet_id=None):
        self.credentials_path = credentials_path
        self.sheet_id = sheet_id or os.environ.get("ZPULSE_SHEET_ID")
        self.service = None
        self.sheet = None

    def connect(self):
        if not GOOGLE_AVAILABLE:
             logger.info("[MOCK] Connected to Google Sheets (Mock).")
             return

        if not os.path.exists(self.credentials_path):
            logger.warning(f"Credentials file not found at {self.credentials_path}. Running in mock mode.")
            return

        try:
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_path, scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=creds)
            self.sheet = self.service.spreadsheets()
            logger.info("Connected to Google Sheets.")
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {e}")

    def log_event(self, event_type, data):
        if not self.sheet:
            logger.info(f"[MOCK] Logged event: {event_type} - {data}")
            return

        if not self.sheet_id:
            logger.error("Sheet ID not provided.")
            return

        try:
            values = [[event_type, json.dumps(data)]]
            body = {'values': values}
            self.sheet.values().append(
                spreadsheetId=self.sheet_id, range="A:B",
                valueInputOption="RAW", body=body
            ).execute()
            logger.info(f"Logged event to sheet: {event_type}")
        except Exception as e:
            logger.error(f"Failed to log event: {e}")

if __name__ == "__main__":
    client = ZPulseClient()
    client.connect()
    client.log_event("TEST_EVENT", {"status": "wired"})
