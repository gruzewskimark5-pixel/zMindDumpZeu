from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from jules.client import JulesClient
from jules.models import RivalryEvent

app = FastAPI()

# Initialize once (production: load from env)
client = JulesClient(
    baseurl="https://api.jules.test",
    apikey="test-key"
)

# -----------------------------
# Request Models
# -----------------------------
class RivalryEventRequest(BaseModel):
    sourceeventid: str
    playeraid: str
    playerbid: str
    roundid: Optional[str] = None
    holenumber: Optional[int] = None
    di: Optional[float] = None
    eventtype: str
    baseweight: float
    eventts: datetime

# -----------------------------
# Routes
# -----------------------------
@app.post("/emit-event")
def emit_event(req: RivalryEventRequest):
    evt = RivalryEvent(
        sourceeventid=req.sourceeventid,
        playeraid=req.playeraid,
        playerbid=req.playerbid,
        roundid=req.roundid,
        holenumber=req.holenumber,
        di=req.di,
        eventtype=req.eventtype,
        baseweight=req.baseweight,
        eventts=req.eventts,
    )
    ack = client.submit_event(evt)
    return {"status": ack.status, "eventid": ack.eventid}

@app.get("/round/{roundid}")
def getround(roundid: str):
    rnd = client.getround(roundid)
    return {
        "id": rnd.id,
        "courseid": rnd.courseid,
        "starttime": rnd.starttime.isoformat(),
        "status": rnd.status,
    }

@app.get("/leaderboard/{roundid}")
def getleaderboard(roundid: str):
    lb = client.getleaderboard(roundid)
    return {
        "roundid": lb.roundid,
        "entries": [
            {
                "playerid": e.playerid,
                "score": e.score,
                "position": e.position,
            }
            for e in lb.entries
        ],
    }
