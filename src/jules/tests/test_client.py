from datetime import datetime, timezone
import pytest
from jules.client import JulesClient
from jules.models import RivalryEvent

def testsubmitevent(requests_mock):
    client = JulesClient(baseurl="https://api.jules.test", apikey="test-key")

    requests_mock.post(
        "https://api.jules.test/events/rivalry",
        json={"status": "ok", "eventid": "evt-1"},
        status_code=200,
    )

    evt = RivalryEvent(
        sourceeventid="evt-1",
        playeraid="A",
        playerbid="B",
        roundid=None,
        holenumber=16,
        di=0.62,
        eventtype="LEADCHANGE",
        baseweight=0.2,
        eventts=datetime.now(timezone.utc),
    )

    ack = client.submit_event(evt)

    assert ack.status == "ok"
    assert ack.eventid == "evt-1"


def testgetround(requests_mock):
    client = JulesClient(baseurl="https://api.jules.test", apikey="test-key")

    requests_mock.get(
        "https://api.jules.test/rounds/round-123",
        json={
            "id": "round-123",
            "courseid": "miakka",
            "starttime": "2026-03-30T12:00:00",
            "status": "active",
        },
        status_code=200,
    )

    rnd = client.getround("round-123")

    assert rnd.id == "round-123"
    assert rnd.courseid == "miakka"
    assert rnd.status == "active"
