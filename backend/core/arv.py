from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime
import math

from pydantic import BaseModel

# ====================== DATA MODELS ======================
@dataclass
class SubjectProperty:
    sqft: int
    beds: int
    baths: float
    year_built: int
    lot_size: float
    condition: str  # "poor", "average", "good", "excellent"
    lat: float
    lon: float

@dataclass
class Comp:
    sale_price: float
    sale_date: datetime
    sqft: int
    beds: int
    baths: float
    year_built: int
    lot_size: float
    condition: str
    lat: float
    lon: float

@dataclass
class ARVResult:
    arv: float
    ppsf_weighted: float
    confidence: float
    comps_used: List[Dict[str, Any]]
    adjustments: Dict[str, float]

# ====================== HELPERS ======================
def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 3958.8
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2)
    return R * 2 * math.asin(math.sqrt(a))

# ====================== CORE FUNCTIONS ======================
def score_comp(subject: SubjectProperty, comp: Comp) -> float:
    dist = haversine(subject.lat, subject.lon, comp.lat, comp.lon)
    distance_score = math.exp(-dist / 1.5)          # strong penalty after ~1.5 mi

    days_old = (datetime.now() - comp.sale_date).days
    recency_score = math.exp(-days_old / 180)

    size_score = max(1 - abs(comp.sqft - subject.sqft) / max(subject.sqft, 1000), 0)
    bed_score = max(1 - abs(comp.beds - subject.beds) * 0.2, 0)
    bath_score = max(1 - abs(comp.baths - subject.baths) * 0.15, 0)

    cond_map = {"poor":1, "average":2, "good":3, "excellent":4}
    cond_diff = abs(cond_map.get(subject.condition.lower(),2) - cond_map.get(comp.condition.lower(),2))
    condition_score = max(1 - cond_diff * 0.3, 0)

    score = (0.35 * distance_score +
             0.25 * recency_score +
             0.20 * size_score +
             0.08 * bed_score +
             0.07 * bath_score +
             0.05 * condition_score)
    return round(max(score, 0.0), 4)

def normalize_ppsf(subject: SubjectProperty, comp: Comp) -> float:
    base = comp.sale_price / comp.sqft if comp.sqft > 0 else 0
    bed_adj = (subject.beds - comp.beds) * 12500
    bath_adj = (subject.baths - comp.baths) * 8500
    cond_map = {"poor":1, "average":2, "good":3, "excellent":4}
    cond_diff = cond_map.get(subject.condition.lower(),2) - cond_map.get(comp.condition.lower(),2)
    cond_adj = cond_diff * 18000
    return round(base + (bed_adj + bath_adj + cond_adj) / subject.sqft, 2)

def compute_confidence(scores: List[float], comps: List[Comp]) -> float:
    if not scores:
        return 0.0
    n = len(scores)
    count_factor = min(n / 8, 1.0)
    similarity_factor = sum(scores) / n

    avg_days = sum((datetime.now() - c.sale_date).days for c in comps) / n
    recency_factor = math.exp(-avg_days / 150)

    ppsfs = [c.sale_price / c.sqft for c in comps]
    mean = sum(ppsfs) / n
    std = math.sqrt(sum((x-mean)**2 for x in ppsfs)/n) if mean > 0 else 0
    variance_factor = max(0, 1 - std / mean * 1.5) if mean > 0 else 0.5

    return round(100 * (0.25*count_factor + 0.30*similarity_factor + 0.25*recency_factor + 0.20*variance_factor), 1)

# ====================== MAIN ENGINE ======================
def compute_arv(subject: SubjectProperty, comps: List[Comp]) -> ARVResult:
    if not comps:
        return ARVResult(0, 0, 0, [], {})
    scored = [(c, score_comp(subject, c)) for c in comps]
    scored = [(c, s) for c, s in scored if s > 0.1]
    if not scored:
        return ARVResult(0, 0, 0, [], {})

    total_score = sum(s for _, s in scored)
    weighted_ppsf = sum((s/total_score) * normalize_ppsf(subject, c) for c, s in scored)

    comps_used = [{
        "sale_price": c.sale_price,
        "sale_date": c.sale_date.isoformat(),
        "sqft": c.sqft,
        "distance_miles": round(haversine(subject.lat, subject.lon, c.lat, c.lon), 2),
        "score": s,
        "adj_ppsf": normalize_ppsf(subject, c)
    } for c, s in scored]

    return ARVResult(
        arv=round(weighted_ppsf * subject.sqft, 0),
        ppsf_weighted=round(weighted_ppsf, 2),
        confidence=compute_confidence([s for _,s in scored], [c for c,_ in scored]),
        comps_used=comps_used,
        adjustments={"bed_adj_dollars":12500, "bath_adj_dollars":8500, "cond_adj_dollars":18000}
    )
