import logging
import json
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dataclasses import dataclass
from typing import Any, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zPulse")

@dataclass
class ZPulseResult:
    zpulse: float
    badge: str
    uptime_score: float
    signal_score: float
    latency_score: float
    freshness_score: float
    meta: Dict[str, Any]

def safe_now(tz: Optional[datetime.timezone] = None) -> datetime.datetime:
    """Returns current UTC time."""
    return datetime.datetime.now(datetime.timezone.utc)

def _write_to_sheet(idempotency_key: str, source: str, result: ZPulseResult) -> bool:
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("google-credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("zPulse_Health_Log").sheet1   # create this sheet once

        row = [
            safe_now(None).isoformat(),
            idempotency_key,
            source,
            result.zpulse,
            result.badge,
            result.uptime_score,
            result.signal_score,
            result.latency_score,
            result.freshness_score,
            json.dumps(result.meta)
        ]
        sheet.append_row(row)
        logger.info(f"Sheet write SUCCESS: zpulse={result.zpulse}")
        return True
    except Exception as e:
        logger.error(f"Sheet write FAILED: {e}")
        return False

def handle_zpulse_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handles a zPulse event.

    This function processes the event, calculates scores (mocked here),
    and attempts to write the result to a Google Sheet.
    """
    logger.info(f"Handling event: {event}")

    # Mock processing logic to generate a result
    # In a real scenario, this would involve complex logic
    result = ZPulseResult(
        zpulse=95.5,
        badge="ELITE",
        uptime_score=99.9,
        signal_score=98.0,
        latency_score=15.0,
        freshness_score=100.0,
        meta={"event_id": event.get("id", "unknown")}
    )

    success = _write_to_sheet(
        idempotency_key=event.get("idempotency_key", "unknown_key"),
        source=event.get("source", "unknown_source"),
        result=result
    )

    if success:
        return {
            "status": "success",
            "zpulse": result.zpulse,
            "result": result
        }
    else:
        # Fallback logic could go here
        logger.warning("Falling back due to sheet write failure")
        return {
            "status": "fallback_emitted",
            "zpulse": result.zpulse,
            "result": result
        }

if __name__ == "__main__":
    # Example usage
    sample_event = {
        "id": "evt_123",
        "idempotency_key": "ik_123",
        "source": "manual_test"
    }
    print(handle_zpulse_event(sample_event))
