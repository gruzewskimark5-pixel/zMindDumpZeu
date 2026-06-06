import unittest
from unittest.mock import patch
from datetime import datetime, timezone
from zpulse import logsheetfallback

class TestZPulseFallback(unittest.TestCase):
    @patch('zpulse.safe_now')
    def test_logsheetfallback_with_payload(self, mock_safe_now):
        # Setup
        mock_now = datetime(2026, 2, 23, 12, 0, 0, tzinfo=timezone.utc)
        mock_safe_now.return_value = mock_now

        idempotency_key = "test-key-123"
        source = "test-source"
        error = "test-error"
        payload = {"key": "value"}

        # Execute
        result = logsheetfallback(idempotency_key, source, error, payload)

        # Assert
        expected = {
            "event_type": "zpulse_fallback",
            "idempotency_key": idempotency_key,
            "source": source,
            "error_type": error,
            "timestamp": mock_now.isoformat(),
            "payload": payload,
            "status": "persisted_locally",
        }
        self.assertEqual(result, expected)

    @patch('zpulse.safe_now')
    def test_logsheetfallback_without_payload(self, mock_safe_now):
        # Setup
        mock_now = datetime(2026, 2, 23, 12, 0, 0, tzinfo=timezone.utc)
        mock_safe_now.return_value = mock_now

        idempotency_key = "test-key-456"
        source = "test-source-2"
        error = "test-error-2"

        # Execute
        result = logsheetfallback(idempotency_key, source, error, payload=None)

        # Assert
        expected = {
            "event_type": "zpulse_fallback",
            "idempotency_key": idempotency_key,
            "source": source,
            "error_type": error,
            "timestamp": mock_now.isoformat(),
            "payload": {},
            "status": "persisted_locally",
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
