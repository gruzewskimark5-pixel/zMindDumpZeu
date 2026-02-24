from dataclasses import dataclass
from backend.core.arv import compute_arv, SubjectProperty, Comp
from backend.core.rehab import estimate_rehab

@dataclass
class OfferResult:
    max_offer: float
    arv: float
    rehab: float
    projected_profit: float
    rule_used: str
    confidence: float

def calculate_offer(subject: SubjectProperty, comps: list, rehab_scope: str = "medium",
                    profit_target: float = 25000, holding_months: int = 6) -> OfferResult:
    arv_result = compute_arv(subject, comps)
    rehab = estimate_rehab(subject.sqft, subject.condition, rehab_scope)

    # Classic 70% rule + extras
    as_is_value = arv_result.arv - rehab.total_rehab
    max_offer_70 = round(as_is_value * 0.70 - profit_target - (holding_months * 1500), 0)  # rough holding cost

    # More aggressive 75% for strong deals
    max_offer_75 = round(as_is_value * 0.75 - profit_target - (holding_months * 1500), 0)

    max_offer = max(max_offer_70, max_offer_75) if max_offer_75 > 0 else max_offer_70
    projected_profit = round(arv_result.arv - rehab.total_rehab - max_offer, 0)

    return OfferResult(
        max_offer=max_offer,
        arv=arv_result.arv,
        rehab=rehab.total_rehab,
        projected_profit=projected_profit,
        rule_used="70/75 hybrid",
        confidence=min(arv_result.confidence, rehab.confidence)
    )
