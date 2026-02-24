# test_zpulse_event.py
from eventbus import handle_zpulse_event

event = {
    "event_type": "zpulse_compute",
    "idempotency_key": "test-123",
    "source": "trading_detector",
    "payload": {
        "uptime_pct": 99.5,
        "signal_score": 92.1,
        "detect_ts": "2026-02-23T05:27:55Z",
        "execute_ts": "2026-02-23T05:27:56Z",
        "last_update_ts": "2026-02-23T05:27:54Z"
    }
}

result = handle_zpulse_event(event)
print(result)
