from dataclasses import dataclass
from typing import Dict

@dataclass
class RehabEstimate:
    total_rehab: float
    breakdown: Dict[str, float]
    confidence: float

def estimate_rehab(subject_sqft: int, condition: str, scope: str = "light") -> RehabEstimate:
    cond_multipliers = {"poor": 1.8, "average": 1.2, "good": 0.85, "excellent": 0.4}
    base_psf = {"light": 35, "medium": 65, "heavy": 110, "full_gut": 160}[scope]

    total = round(subject_sqft * base_psf * cond_multipliers.get(condition.lower(), 1.0), 0)

    breakdown = {
        "kitchen": round(total * 0.22, 0),
        "bathrooms": round(total * 0.18, 0),
        "flooring": round(total * 0.15, 0),
        "paint+trim": round(total * 0.12, 0),
        "roof/hvac/electrical": round(total * 0.20, 0),
        "misc": round(total * 0.13, 0),
    }

    confidence = 85 if len(breakdown) > 0 else 40
    return RehabEstimate(total_rehab=total, breakdown=breakdown, confidence=confidence)
