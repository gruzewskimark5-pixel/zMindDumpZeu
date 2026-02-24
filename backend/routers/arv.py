from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
from backend.core.arv import compute_arv, SubjectProperty, Comp

router = APIRouter(prefix="/arv", tags=["ARV"])

class ARVRequest(BaseModel):
    subject: dict
    comps: List[dict]

@router.post("/")
def calculate_arv(req: ARVRequest):
    subject = SubjectProperty(**req.subject)
    comps = [Comp(**{**c, "sale_date": datetime.fromisoformat(c["sale_date"].replace("Z","+00:00"))}) for c in req.comps]
    return compute_arv(subject, comps)
