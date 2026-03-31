import unittest
from datetime import datetime, timezone
from jules.client import JulesClient
from jules.models import RivalryEvent

class MockAuth:
    def apply(self, h):
        h["Authorization"] = "Bearer test"
        return h

class MockTransport:
    def __init__(self):
        self.last_payload = None
    def request(self, method, path, json_payload=None):
        self.last_payload = json_payload
        if "rounds/r1" in path:
            return {"id": "r1", "courseid": "c1", "starttime": "2026-03-31T10:00:00Z", "status": "IN_PROGRESS"}
        if "rivalry" in path:
            return {"status": "ok", "eventid": "e1"}
        return {}

class TestJulesSDK(unittest.TestCase):
    def setUp(self):
        self.client = JulesClient("https://api.jules.com", "test-key")
        self.client.transport = MockTransport()
        self.client.transport.auth = MockAuth()

    def test_getround(self):
        r = self.client.getround("r1")
        self.assertEqual(r.id, "r1")

    def test_submit_event(self):
        e = RivalryEvent(
            sourceeventid="e1",
            playeraid="p1",
            playerbid="p2",
            eventtype="LEAD_CHANGE",
            baseweight=0.2,
            eventts=datetime.now(timezone.utc)
        )
        ack = self.client.submit_event(e)
        self.assertEqual(ack.eventid, "e1")

if __name__ == "__main__":
    unittest.main()
