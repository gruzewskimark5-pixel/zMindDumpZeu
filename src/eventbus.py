from typing import Dict, Any, Optional
from datetime import datetime
import json
import logging

from zpulse import (
    ZPulseInput,
    ZPulseResult,
    compute_zpulse,
    logsheet_fallback,
    safe_now,
)

logger = logging.getLogger(__name__)


def handle_zpulse_event(raw_event: Dict[str, Any]) -> Dict[str, Any]:
    try:
        idempotency_key = raw_event.get("idempotency_key", "unknown")
        source = raw_event.get("source", "unknown")
        payload = raw_event.get("payload", {})

        input_data = _parse_zpulse_input(payload)
        if not input_data:
            raise ValueError("Invalid ZPulseInput data")

        result = compute_zpulse(input_data)

        success = _write_to_sheet(
            idempotency_key=idempotency_key,
            source=source,
            result=result,
        )

        if success:
            return {
                "status": "success",
                "zpulse": result.zpulse,
                "badge": result.badge,
                "idempotency_key": idempotency_key,
            }

        fallback_event = logsheet_fallback(
            idempotency_key=idempotency_key,
            source=source,
            error="sheet_write_failed",
            payload={
                "zpulse_result": _result_to_dict(result),
                "raw_payload": payload,
            },
        )
        return {
            "status": "fallback_emitted",
            "event": fallback_event,
            "idempotency_key": idempotency_key,
        }

    except Exception as e:
        logger.exception(f"zpulse handler failed: {e}")
        fallback_event = logsheet_fallback(
            idempotency_key=raw_event.get("idempotency_key", "unknown"),
            source=raw_event.get("source", "unknown"),
            error=f"handler_error: {str(e)}",
            payload=raw_event.get("payload"),
        )
        return {
            "status": "error_fallback",
            "event": fallback_event,
        }


def _parse_zpulse_input(payload: Dict[str, Any]) -> Optional[ZPulseInput]:
    try:
        return ZPulseInput(
            uptime_pct=float(payload.get("uptime_pct", 0)),
            # Normalizing 0-100 to 0-1 as per user intent
            signal_score=float(payload.get("signal_score", 0)) / 100.0,
            detect_ts=_parse_iso(payload["detect_ts"]),
            execute_ts=_parse_iso(payload["execute_ts"]),
            last_update_ts=_parse_iso(payload["last_update_ts"]),
            now_ts=None,
            max_latency_ms=float(payload.get("max_latency_ms", 5000)),
            max_freshness_sec=float(payload.get("max_freshness_sec", 3600)),
        )
    except (KeyError, ValueError, TypeError):
        logger.warning(f"Failed to parse ZPulseInput: {payload}")
        return None


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _write_to_sheet(idempotency_key: str, source: str, result: ZPulseResult) -> bool:
    try:
        row = [
            safe_now().isoformat(),
            idempotency_key,
            source,
            result.zpulse,
            result.badge,
            result.uptime_score,
            result.signal_score,
            result.latency_score,
            result.freshness_score,
            json.dumps(result.meta),
        ]
        # sheet.append_row(row)
        logger.info(f"Sheet write stub: zpulse={result.zpulse} badge={result.badge}")
        return True
    except Exception as e:
        logger.error(f"Sheet write failed: {e}")
        return False


def _result_to_dict(result: ZPulseResult) -> Dict[str, Any]:
    return {
        "uptime_score": result.uptime_score,
        "signal_score": result.signal_score,
        "latency_score": result.latency_score,
        "freshness_score": result.freshness_score,
        "zpulse": result.zpulse,
        "badge": result.badge,
        "meta": result.meta,
    }
