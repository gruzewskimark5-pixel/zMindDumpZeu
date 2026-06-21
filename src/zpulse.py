from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime, timezone


# Optimization: Using slots=True reduces memory footprint and improves attribute access
# speeds in Python 3.11+ for these hot-path data models.
# Optimization: Using slots=True removes the __dict__ attribute, significantly reducing
# memory footprint and improving attribute access speed for high-throughput processing paths.
@dataclass(slots=True)
class ZPulseInput:
    uptime_pct: float
    signal_score: float          # 0–1 in your current semantics
    detect_ts: datetime
    execute_ts: datetime
    last_update_ts: datetime
    now_ts: Optional[datetime] = None
    max_latency_ms: float = 5000
    max_freshness_sec: float = 3600


# Optimization: Using slots=True reduces memory footprint and improves attribute access
# speeds in Python 3.11+ for these hot-path data models.
# Optimization: slots=True reduces memory and improves speed for object creation and field access.
@dataclass(slots=True)
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
    if latency_ms < 0.0:
        latency_ms = 0.0

    max_lat = input_data.max_latency_ms
    if max_lat > 0:
        over = latency_ms - max_lat
        if over < 0.0:
            over = 0.0
        latency_score = 1.0 - (over / max_lat)
        if latency_score < 0.0:
            latency_score = 0.0
    else:
        latency_score = 1.0 if latency_ms <= 0 else 0.0

    # Freshness (sec) — clamp negative
    freshness_sec = (now - input_data.last_update_ts).total_seconds()
    if freshness_sec < 0.0:
        freshness_sec = 0.0

    max_fresh = input_data.max_freshness_sec
    if max_fresh > 0:
        over = freshness_sec - max_fresh
        if over < 0.0:
            over = 0.0
        freshness_score = 1.0 - (over / max_fresh)
        if freshness_score < 0.0:
            freshness_score = 0.0
    else:
        freshness_score = 1.0 if freshness_sec <= 0 else 0.0

    # uptime_score
    uptime_val = input_data.uptime_pct / 100.0
    if uptime_val < 0.0:
        uptime_score = 0.0
    elif uptime_val > 1.0:
        uptime_score = 1.0
    else:
        uptime_score = uptime_val

    # signal_score
    signal_val = input_data.signal_score
    if signal_val < 0.0:
        signal_score = 0.0
    elif signal_val > 1.0:
        signal_score = 1.0
    else:
        signal_score = signal_val

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


def logsheetfallback(
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
