import unittest
import time
from eventbus import EventBus
from zpulse import ZPulseClient

class TestEventBus(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()
        self.bus.start()
        self.zpulse = ZPulseClient() # Starts in mock mode if no creds

    def tearDown(self):
        self.bus.stop()

    def test_publish_subscribe(self):
        received = []
        def handler(data):
            received.append(data)

        self.bus.subscribe("TEST_EVENT", handler)
        self.bus.publish("TEST_EVENT", "payload")

        time.sleep(1) # Allow processing
        self.assertEqual(received, ["payload"])

    def test_zpulse_integration(self):
        # Mock integration test
        self.bus.subscribe("LOG_EVENT", lambda d: self.zpulse.log_event("LOG", d))
        self.bus.publish("LOG_EVENT", {"msg": "Integration Test"})
        time.sleep(1)
        # Check logs manually or rely on no exception

if __name__ == '__main__':
    unittest.main()
