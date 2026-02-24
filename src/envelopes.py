from typing import Dict, Any, Optional
from zpulse import ZPulseInput, ZPulseResult


def build_zpulse_envelope(
    idempotency_key: str,
    source: str,
    trace_id: Optional[str],
    input_data: ZPulseInput,
    result: ZPulseResult,
    version: str = "zv1.0.0",
) -> Dict[str, Any]:
    return {
        "event_type": "analysis",
        "version": version,
        "idempotency_key": idempotency_key,
        "trace_id": trace_id,
        "source": source,
        "artifact": {
            "kind": "zpulse_score",
            "content": {
                "zpulse": result.zpulse,
                "badge": result.badge,
                "uptime_score": result.uptime_score,
                "signal_score": result.signal_score,
                "latency_score": result.latency_score,
                "freshness_score": result.freshness_score,
            },
            "meta": result.meta or {},
        },
    }
