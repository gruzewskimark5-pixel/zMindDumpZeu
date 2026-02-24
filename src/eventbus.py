# src/eventbus.py - EventBus handler that wires zpulse.py
# Drop this next to your zpulse.py. Handles parsing → compute → sheet → fallback.

from typing import Dict, Any, Optional
from datetime import datetime
import json
import logging
from zpulse import (
    ZPulseInput,
    compute_zpulse,
    logsheet_fallback,
    safe_now,
    ZPulseResult
)

logger = logging.getLogger(__name__)

def handle_zpulse_event(raw_event: Dict[str, Any]) -> Dict[str, Any]:
    """
    EventBus handler: raw event → ZPulseInput → compute → sheet → fallback.

    Expected raw_event envelope:
    {
        "event_type": "zpulse_compute",
        "idempotency_key": "uuid-v4",
        "source": "detector_name",
        "timestamp": "2026-02-23T05:28:00Z",
        "payload": {
            "uptime_pct": 99.2,
            "signal_score": 87.3,
            "detect_ts": "2026-02-23T05:27:55Z",
            "execute_ts": "2026-02-23T05:27:58Z",
            "last_update_ts": "2026-02-23T05:27:50Z"
        }
    }
    """
    try:
        # Extract idempotency + source for fallback
        idempotency_key = raw_event.get("idempotency_key", "unknown")
        source = raw_event.get("source", "unknown")

        # Parse payload → ZPulseInput (with validation)
        payload = raw_event.get("payload", {})
        input_data = _parse_zpulse_input(payload)

        if not input_data:
            raise ValueError("Invalid ZPulseInput data")

        # Compute ZPulse
        result = compute_zpulse(input_data)

        # Attempt sheet write (your sheet client here)
        success = _write_to_sheet(
            idempotency_key=idempotency_key,
            source=source,
            result=result
        )

        if success:
            return {
                "status": "success",
                "zpulse": result.zpulse,
                "badge": result.badge,
                "idempotency_key": idempotency_key
            }
        else:
            # Sheet failed → emit fallback
            fallback_event = logsheet_fallback(
                idempotency_key=idempotency_key,
                source=source,
                error="sheet_write_failed",
                payload={
                    "zpulse_result": _result_to_dict(result),
                    "raw_payload": payload
                }
            )
            return {
                "status": "fallback_emitted",
                "event": fallback_event,
                "idempotency_key": idempotency_key
            }

    except Exception as e:
        logger.exception(f"zpulse handler failed: {e}")
        fallback_event = logsheet_fallback(
            idempotency_key=raw_event.get("idempotency_key", "unknown"),
            source=raw_event.get("source", "unknown"),
            error=f"handler_error: {str(e)}",
            payload=raw_event.get("payload")
        )
        return {
            "status": "error_fallback",
            "event": fallback_event
        }


def _parse_zpulse_input(payload: Dict[str, Any]) -> Optional[ZPulseInput]:
    """Safely parse dict → ZPulseInput with ISO datetime conversion."""
    try:
        return ZPulseInput(
            uptime_pct=float(payload.get("uptime_pct", 0)),
            signal_score=float(payload.get("signal_score", 0)),
            detect_ts=datetime.fromisoformat(payload["detect_ts"].replace("Z", "+00:00")),
            execute_ts=datetime.fromisoformat(payload["execute_ts"].replace("Z", "+00:00")),
            last_update_ts=datetime.fromisoformat(payload["last_update_ts"].replace("Z", "+00:00")),
            now_ts=None,  # Uses live time
            max_latency_ms=payload.get("max_latency_ms", 5000),
            max_freshness_sec=payload.get("max_freshness_sec", 3600)
        )
    except (KeyError, ValueError, TypeError):
        logger.warning(f"Failed to parse ZPulseInput: {payload}")
        return None


def _write_to_sheet(idempotency_key: str, source: str, result: ZPulseResult) -> bool:
    """
    YOUR SHEET IMPLEMENTATION HERE.
    Replace with gspread, Google Sheets API, or your preferred client.

    Returns True if write succeeded, False if failed (triggers fallback).
    """
    # Example stub - replace with real sheet write
    try:
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
        # sheet.append_row(row)  # <- Your real sheet client
        logger.info(f"Sheet write stub: zpulse={result.zpulse} badge={result.badge}")
        return True
    except Exception as e:
        logger.error(f"Sheet write failed: {e}")
        return False


def _result_to_dict(result: ZPulseResult) -> Dict[str, Any]:
    """Serialize ZPulseResult for fallback JSON."""
    return {
        "uptime_score": result.uptime_score,
        "signal_score": result.signal_score,
        "latency_score": result.latency_score,
        "freshness_score": result.freshness_score,
        "zpulse": result.zpulse,
        "badge": result.badge,
        "meta": result.meta
    }
