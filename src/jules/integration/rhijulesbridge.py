from datetime import datetime, timezone
from jules.client import JulesClient
from jules.models import RivalryEvent

class RHIJulesBridge:
    """
    Thin integration layer that converts internal RHI events
    into Jules-compatible RivalryEvent objects and submits them.
    """

    def __init__(self, jules_client: JulesClient):
        self.jules = jules_client

    def emitrhievent(
        self,
        sourceeventid: str,
        player_a: str,
        player_b: str,
        eventtype: str,
        baseweight: float,
        di: float = None,
        roundid: str = None,
        holenumber: int = None,
        eventts: datetime = None,
    ):
        evt = RivalryEvent(
            sourceeventid=sourceeventid,
            playeraid=player_a,
            playerbid=player_b,
            roundid=roundid,
            holenumber=holenumber,
            di=di,
            eventtype=eventtype,
            baseweight=baseweight,
            eventts=eventts or datetime.now(timezone.utc),
        )

        return self.jules.submit_event(evt)
