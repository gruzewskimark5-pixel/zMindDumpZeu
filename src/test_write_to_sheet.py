import unittest
from unittest.mock import patch, MagicMock
from eventbus import write_to_sheet
from zpulse import ZPulseResult

class TestWriteToSheet(unittest.TestCase):
    def setUp(self):
        self.result = ZPulseResult(
            zpulse=0.95,
            badge="ELITE",
            uptime_score=1.0,
            signal_score=0.9,
            latency_score=0.95,
            freshness_score=0.95,
            meta={"latency_ms": 100, "freshness_sec": 60}
        )
        self.idempotency_key = "test-key"
        self.source = "test-source"

    def test_write_to_sheet_success(self):
        """Test that write_to_sheet returns True on success."""
        success = write_to_sheet(
            idempotency_key=self.idempotency_key,
            source=self.source,
            result=self.result
        )
        self.assertTrue(success)

    @patch("eventbus.json.dumps")
    def test_write_to_sheet_failure(self, mock_json_dumps):
        """Test that write_to_sheet returns False on exception."""
        mock_json_dumps.side_effect = Exception("Mocked exception")

        success = write_to_sheet(
            idempotency_key=self.idempotency_key,
            source=self.source,
            result=self.result
        )
        self.assertFalse(success)

if __name__ == "__main__":
    unittest.main()
