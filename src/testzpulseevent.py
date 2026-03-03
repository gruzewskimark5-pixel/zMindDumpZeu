from eventbus import handle_zpulse_event, parse_zpulse_input

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

def test_parse_zpulse_input_failures():
    print("Running test_parse_zpulse_input_failures...")

    # Missing mandatory detect_ts
    payload_no_detect = {
        "execute_ts": "2026-02-23T05:27:56Z",
        "lastupdatets": "2026-02-23T05:27:54Z",
    }
    assert parse_zpulse_input(payload_no_detect) is None

    # Invalid timestamp format
    payload_bad_ts = {
        "detect_ts": "not-a-date",
        "execute_ts": "2026-02-23T05:27:56Z",
        "lastupdatets": "2026-02-23T05:27:54Z",
    }
    assert parse_zpulse_input(payload_bad_ts) is None

    # Invalid data type for float
    payload_bad_float = {
        "uptime_pct": "invalid",
        "detect_ts": "2026-02-23T05:27:55Z",
        "execute_ts": "2026-02-23T05:27:56Z",
        "lastupdatets": "2026-02-23T05:27:54Z",
    }
    assert parse_zpulse_input(payload_bad_float) is None

    # None payload (should trigger TypeError or AttributeError, caught by except)
    assert parse_zpulse_input(None) is None # type: ignore

    print("test_parse_zpulse_input_failures passed!")

def test_handle_zpulse_event_with_invalid_payload():
    print("Running test_handle_zpulse_event_with_invalid_payload...")

    event = {
        "idempotency_key": "fail-test",
        "source": "trading_detector",
        "payload": {
            "uptime_pct": 99.5,
            # Missing detect_ts
        },
    }

    result = handle_zpulse_event(event)
    assert result["status"] == "error_fallback"
    assert "event" in result
    assert result["event"]["error_type"] == "handler_error: Invalid ZPulseInput data"
    print("test_handle_zpulse_event_with_invalid_payload passed!")

if __name__ == "__main__":
    testzpulseevent_basic()
    test_parse_zpulse_input_failures()
    test_handle_zpulse_event_with_invalid_payload()
