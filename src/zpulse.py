from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime, timezone


@dataclass
class ZPulseInput:
    uptime_pct: float
    signal_score: float          # 0–1 in your current semantics
    detect_ts: datetime
    execute_ts: datetime
    last_update_ts: datetime
    now_ts: Optional[datetime] = None
    max_latency_ms: float = 5000
    max_freshness_sec: float = 3600


@dataclass
class ZPulseResult:
    zpulse: float
    badge: str
    uptime_score: float
    signal_score: float
    latency_score: float
    freshness_score: float
    meta: Dict[str, Any] = field(default_factory=dict)


def safe_now(tz=None) -> datetime:
    return datetime.now(tz or timezone.utc)


def compute_zpulse(input_data: ZPulseInput) -> ZPulseResult:
    now = input_data.now_ts or safe_now()

    # Latency (ms) — clamp negative
    latency_ms = (input_data.execute_ts - input_data.detect_ts).total_seconds() * 1000.0
    latency_ms = max(0.0, latency_ms)

    if input_data.max_latency_ms > 0:
        over = max(0.0, latency_ms - input_data.max_latency_ms)
        latency_score = max(0.0, 1.0 - (over / input_data.max_latency_ms))
    else:
        latency_score = 1.0 if latency_ms <= 0 else 0.0

    # Freshness (sec) — clamp negative
    freshness_sec = (now - input_data.last_update_ts).total_seconds()
    freshness_sec = max(0.0, freshness_sec)

    if input_data.max_freshness_sec > 0:
        over = max(0.0, freshness_sec - input_data.max_freshness_sec)
        freshness_score = max(0.0, 1.0 - (over / input_data.max_freshness_sec))
    else:
        freshness_score = 1.0 if freshness_sec <= 0 else 0.0

    uptime_score = max(0.0, min(1.0, input_data.uptime_pct / 100.0))
    signal_score = max(0.0, min(1.0, input_data.signal_score))  # 0–1

    zpulse_val = (
        uptime_score * 0.3
        + signal_score * 0.3
        + latency_score * 0.2
        + freshness_score * 0.2
    )

    if zpulse_val >= 0.9:
        badge = "ELITE"
    elif zpulse_val >= 0.7:
        badge = "HEALTHY"
    elif zpulse_val >= 0.5:
        badge = "DEGRADED"
    else:
        badge = "CRITICAL"

    return ZPulseResult(
        zpulse=round(zpulse_val, 4),
        badge=badge,
        uptime_score=round(uptime_score, 4),
        signal_score=round(signal_score, 4),
        latency_score=round(latency_score, 4),
        freshness_score=round(freshness_score, 4),
        meta={
            "latency_ms": latency_ms,
            "freshness_sec": freshness_sec,
            "computed_at": now.isoformat(),
        },
    )


def log_sheet_fallback(
    idempotency_key: str,
    source: str,
    error: str,
    payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "event_type": "zpulse_fallback",
        "idempotency_key": idempotency_key,
        "source": source,
        "error_type": error,
        "timestamp": safe_now().isoformat(),
        "payload": payload or {},
        "status": "persisted_locally",
    }
