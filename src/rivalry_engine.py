from typing import Dict, Any, List, Optional
import math
import time

def compute_performance_delta(score_a: float, score_b: float) -> float:
    # Direct performance delta D_AB
    # norm(score_B - score_A) on a band of -5 to +5
    raw = score_b - score_a
    norm_raw = max(-1.0, min(1.0, raw / 5.0))
    d_ab = (norm_raw + 1.0) / 2.0
    return round(d_ab, 4)

def compute_di_weighted_context(shared_holes: List[Dict[str, Any]]) -> float:
    # DI-weighted context DI_AB
    # sum((score_B(h) - score_A(h)) * DI(h))
    # Normalize across -10 to +10 band
    weighted_sum = 0
    for hole in shared_holes:
        diff = hole.get("score_b", 0) - hole.get("score_a", 0)
        di = hole.get("DI", 0.5)
        weighted_sum += diff * di

    norm_weighted = max(-1.0, min(1.0, weighted_sum / 10.0))
    di_ab = (norm_weighted + 1.0) / 2.0
    return round(di_ab, 4)

def compute_identity_divergence(traits_a: Dict[str, float], traits_b: Dict[str, float]) -> float:
    # ID_AB: L1 distance between traits {execution, decision, pressure, chaos}
    keys = ["execution", "decision", "pressure", "chaos"]
    total_diff = 0
    for key in keys:
        total_diff += abs(traits_a.get(key, 0.0) - traits_b.get(key, 0.0))

    id_ab = total_diff / 4.0
    return round(id_ab, 4)

def compute_event_triggers(events: List[Dict[str, Any]]) -> float:
    # E_AB: sum of discrete event weights
    e_ab = sum(event.get("weight", 0.0) for event in events)
    return round(min(1.0, e_ab), 4)

def apply_decay(last_updated: int, current_time: int) -> float:
    # Decay_AB: norm(delta_t)
    # 30 days = full decay (1.0). 7 days = 0.25.
    delta_t_sec = current_time - last_updated
    delta_t_days = delta_t_sec / (24 * 3600)

    decay_ab = min(1.0, delta_t_days / 30.0)
    return round(decay_ab, 4)

def update_rhi(
    current_rhi: float,
    d_ab: float,
    di_ab: float,
    id_ab: float,
    e_ab: float,
    decay_ab: float,
    weights: Optional[Dict[str, float]] = None
) -> float:
    # Base formula: 0.30 D + 0.25 DI + 0.25 ID + 0.20 E - 0.15 Decay
    if not weights:
        weights = {
            "d": 0.30,
            "di": 0.25,
            "id": 0.25,
            "e": 0.20,
            "decay": 0.15
        }

    delta_rhi = (
        weights["d"] * d_ab +
        weights["di"] * di_ab +
        weights["id"] * id_ab +
        weights["e"] * e_ab -
        weights["decay"] * decay_ab
    )

    new_rhi = max(0.0, min(1.0, current_rhi + delta_rhi))
    return round(new_rhi, 4)

def get_heat_band(rhi: float) -> str:
    if rhi >= 0.81: return "Nuclear"
    if rhi >= 0.61: return "Volatile"
    if rhi >= 0.41: return "Hot"
    if rhi >= 0.21: return "Warm"
    return "Cold"
