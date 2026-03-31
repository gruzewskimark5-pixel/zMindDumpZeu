from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class RivalryEvent:
    sourceeventid: str
    playeraid: str
    playerbid: str
    eventtype: str
    baseweight: float
    eventts: datetime
    roundid: Optional[str] = None
    holenumber: Optional[int] = None
    di: Optional[float] = None

@dataclass
class EventAck:
    status: str
    eventid: str

@dataclass
class BatchAck:
    status: str
    accepted: int
    failed: int

@dataclass
class Round:
    id: str
    courseid: str
    starttime: datetime
    status: str

@dataclass
class LeaderboardEntry:
    playerid: str
    score: int
    position: int

@dataclass
class Leaderboard:
    roundid: str
    entries: List[LeaderboardEntry]
