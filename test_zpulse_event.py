# test_zpulse_event.py
from eventbus import handle_zpulse_event

def test_zpulse_event_basic():
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
    print("Result:", result)

    assert result["status"] == "success"
    assert "zpulse" in result
    assert "badge" in result
    assert isinstance(result["zpulse"], float)
    assert isinstance(result["badge"], str)

    # Optional: sanity check that scores are within bounds
    assert 0.0 <= result["zpulse"] <= 1.0

if __name__ == "__main__":
    test_zpulse_event_basic()
    print("Test passed!")
