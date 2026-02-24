from typing import Dict, Any, Optional
from datetime import datetime
from zpulse import ZPulseInput, compute_zpulse, logsheet_fallback, ZPulseResult
from envelopes import build_zpulse_envelope


def parse_zpulse_input(payload: Dict[str, Any]) -> Optional[ZPulseInput]:
    try:
        return ZPulseInput(
            uptime_pct=float(payload.get("uptime_pct", 0.0)),
            signal_score=float(payload.get("signal_score", 0.0)),
            detect_ts=datetime.fromisoformat(payload.get("detect_ts")),
            execute_ts=datetime.fromisoformat(payload.get("execute_ts")),
            last_update_ts=datetime.fromisoformat(payload.get("last_update_ts")),
            now_ts=datetime.fromisoformat(payload.get("now_ts")) if payload.get("now_ts") else None,
            max_latency_ms=float(payload.get("max_latency_ms", 5000.0)),
            max_freshness_sec=float(payload.get("max_freshness_sec", 3600.0)),
        )
    except Exception:
        return None


def write_to_sheet(idempotency_key: str, source: str, result: ZPulseResult) -> bool:
    # STUB: In a real implementation, this would write to Google Sheets.
    # For now, we simulate success.
    # To simulate failure for testing, one could add a check for a specific key.
    if idempotency_key == "trigger_sheet_failure":
        return False
    return True


def handle_zpulse_event(raw_event: Dict[str, Any]) -> Dict[str, Any]:
    idempotency_key = raw_event.get("idempotency_key", "unknown")
    source = raw_event.get("source", "unknown")
    trace_id = raw_event.get("trace_id")

    payload = raw_event.get("payload", {})

    input_data = parse_zpulse_input(payload)
    if not input_data:
        # build error envelope via logsheet_fallback
        return {
            "status": "error",
            "event": logsheet_fallback(
                idempotency_key=idempotency_key,
                source=source,
                error="invalid_input",
                payload=payload,
            ),
        }

    result = compute_zpulse(input_data)
    envelope = build_zpulse_envelope(
        idempotency_key=idempotency_key,
        source=source,
        trace_id=trace_id,
        input_data=input_data,
        result=result,
    )

    # try sheet write; on failure, emit fallback
    if write_to_sheet(idempotency_key, source, result):
        return {
            "status": "success",
            "event": envelope,
        }

    fallback_event = logsheet_fallback(
        idempotency_key=idempotency_key,
        source=source,
        error="sheet_write_failed",
        payload={"zpulse_envelope": envelope},
    )
    return {
        "status": "fallback_emitted",
        "event": fallback_event,
    }
