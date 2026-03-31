from datetime import datetime
from typing import List, Optional

from .transport import HttpTransport
from .models import (
    RivalryEvent,
    EventAck,
    BatchAck,
    Round,
    Leaderboard,
    LeaderboardEntry,
)
from .retry import retry_request


class JulesClient:
    def __init__(self, baseurl: str, apikey: str):
        from .auth import ApiKeyAuth

        self.transport = HttpTransport(
            baseurl=baseurl,
            auth=ApiKeyAuth(api_key=apikey)
        )

    # -----------------------------
    # Submit a single rivalry event
    # -----------------------------
    def submit_event(self, event: RivalryEvent) -> EventAck:
        def _call():
            payload = {
                "sourceeventid": event.sourceeventid,
                "playeraid": event.playeraid,
                "playerbid": event.playerbid,
                "roundid": event.roundid,
                "holenumber": event.holenumber,
                "di": event.di,
                "eventtype": event.eventtype,
                "baseweight": event.baseweight,
                "eventts": event.eventts.isoformat(),
            }
            data = self.transport.request(
                "POST",
                "/events/rivalry",
                json_payload=payload
            )
            return EventAck(
                status=data.get("status", "ok"),
                eventid=data.get("eventid", event.sourceeventid)
            )

        return retry_request(_call)

    # -----------------------------
    # Submit a batch of events
    # -----------------------------
    def submit_batch(self, events: List[RivalryEvent]) -> BatchAck:
        def _call():
            payload = [
                {
                    "sourceeventid": e.sourceeventid,
                    "playeraid": e.playeraid,
                    "playerbid": e.playerbid,
                    "roundid": e.roundid,
                    "holenumber": e.holenumber,
                    "di": e.di,
                    "eventtype": e.eventtype,
                    "baseweight": e.baseweight,
                    "eventts": e.eventts.isoformat(),
                }
                for e in events
            ]

            data = self.transport.request(
                "POST",
                "/events/rivalry/batch",
                json_payload=payload
            )

            return BatchAck(
                status=data.get("status", "ok"),
                accepted=data.get("accepted", 0),
                failed=data.get("failed", 0)
            )

        return retry_request(_call)

    # -----------------------------
    # Fetch a round
    # -----------------------------
    def getround(self, roundid: str) -> Round:
        def _call():
            data = self.transport.request(
                "GET",
                f"/rounds/{roundid}"
            )
            return Round(
                id=data["id"],
                courseid=data["courseid"],
                starttime=datetime.fromisoformat(data["starttime"]),
                status=data["status"]
            )

        return retry_request(_call)

    # -----------------------------
    # Fetch leaderboard
    # -----------------------------
    def getleaderboard(self, roundid: str) -> Leaderboard:
        def _call():
            data = self.transport.request(
                "GET",
                f"/rounds/{roundid}/leaderboard"
            )
            entries = [
                LeaderboardEntry(
                    playerid=e["playerid"],
                    score=e["score"],
                    position=e["position"]
                )
                for e in data.get("entries", [])
            ]
            return Leaderboard(roundid=roundid, entries=entries)

        return retry_request(_call)
