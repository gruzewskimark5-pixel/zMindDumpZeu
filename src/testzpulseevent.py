from eventbus import handle_zpulse_event

def testzpulseevent_basic():
    event = {
        "event_type": "zpulse_compute",
        "idempotency_key": "test-123",
        "source": "trading_detector",
        "payload": {
            "uptime_pct": 99.5,
            "signal_score": 92.1,
            "detect_ts": "2026-02-23T05:27:55Z",
            "execute_ts": "2026-02-23T05:27:56Z",
            "lastupdatets": "2026-02-23T05:27:54Z",
        },
    }

    result = handle_zpulse_event(event)
    assert result["status"] == "success"
    assert "zpulse" in result
    assert "badge" in result
    print("testzpulseevent_basic passed!")
    print(f"Result: {result}")

if __name__ == "__main__":
    testzpulseevent_basic()
