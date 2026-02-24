import unittest
from unittest.mock import MagicMock, patch
import sys
import json

# Mock external dependencies that are not installed
sys.modules["gspread"] = MagicMock()
sys.modules["oauth2client"] = MagicMock()
sys.modules["oauth2client.service_account"] = MagicMock()

# Now we can import the module under test
from src.eventbus import handle_zpulse_event

class TestEventBus(unittest.TestCase):

    def setUp(self):
        self.sample_event = {
            "id": "evt_test_123",
            "idempotency_key": "ik_test_123",
            "source": "automated_test"
        }

    @patch("src.eventbus.gspread")
    @patch("src.eventbus.ServiceAccountCredentials")
    def test_full_happy_path(self, mock_creds, mock_gspread):
        # Setup mocks for success path
        mock_client = MagicMock()
        mock_sheet = MagicMock()
        mock_gspread.authorize.return_value = mock_client
        mock_client.open.return_value.sheet1 = mock_sheet

        # Call the function
        result = handle_zpulse_event(self.sample_event)

        # Verify result
        self.assertEqual(result["status"], "success")
        self.assertGreater(result["zpulse"], 90)

        # Verify sheet interaction
        mock_gspread.authorize.assert_called_once()
        mock_sheet.append_row.assert_called_once()

        # Check that append_row was called with correct data structure
        args, _ = mock_sheet.append_row.call_args
        row_data = args[0]
        self.assertEqual(row_data[1], "ik_test_123")  # idempotency_key
        self.assertEqual(row_data[2], "automated_test")  # source
        print("✅ Full pipeline test passed")

    @patch("src.eventbus.gspread")
    @patch("src.eventbus.ServiceAccountCredentials")
    def test_sheet_failure_fallback(self, mock_creds, mock_gspread):
        # Setup mocks to raise an exception
        mock_gspread.authorize.side_effect = Exception("Auth failed")

        # Call the function
        result = handle_zpulse_event(self.sample_event)

        # Verify fallback result
        self.assertEqual(result["status"], "fallback_emitted")

        # Verify attempt was made
        mock_gspread.authorize.assert_called_once()
        print("✅ Fallback test passed")

if __name__ == "__main__":
    unittest.main()
