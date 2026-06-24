import unittest
from unittest.mock import patch
from datetime import datetime
from zpulse import logsheetfallback

class TestZPulseFallback(unittest.TestCase):
    @patch('zpulse.safe_now')
    def test_logsheetfallback(self, mock_safe_now):
        mock_safe_now.return_value = datetime(2023, 1, 1, 12, 0, 0)

        result = logsheetfallback(
            idempotency_key="key123",
            source="source456",
            error="some_error",
            payload={"test": "data"}
        )

        expected = {
            "event_type": "zpulse_fallback",
            "idempotency_key": "key123",
            "source": "source456",
            "error_type": "some_error",
            "timestamp": "2023-01-01T12:00:00",
            "payload": {"test": "data"},
            "status": "persisted_locally",
        }
        self.assertEqual(result, expected)

    @patch('zpulse.safe_now')
    def test_logsheetfallback_with_timestamp_iso(self, mock_safe_now):
        # safe_now should not be called if timestamp_iso is provided
        mock_safe_now.side_effect = Exception("safe_now should not be called")

        result = logsheetfallback(
            idempotency_key="key123",
            source="source456",
            error="some_error",
            payload={"test": "data"},
            timestamp_iso="2023-05-05T15:30:00"
        )

        expected = {
            "event_type": "zpulse_fallback",
            "idempotency_key": "key123",
            "source": "source456",
            "error_type": "some_error",
            "timestamp": "2023-05-05T15:30:00",
            "payload": {"test": "data"},
            "status": "persisted_locally",
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
