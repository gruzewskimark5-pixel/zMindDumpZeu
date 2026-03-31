from typing import Dict, Any, List, Optional
import math

def compute_g(geometry: Dict[str, Any]) -> float:
    # G — Geometry Complexity (0.1 - 1.0)
    dist = geometry.get("distance_yards", 400)
    g_dist = (dist - 320) / (520 - 320)
    g_dist = max(0.0, min(1.0, g_dist))

    lzs = geometry.get("landing_zones", [])
    if lzs:
        width = lzs[0].get("fairway_width", 30)
        g_width = 1.0 - (width - 18) / (45 - 18)
    else:
        g_width = 0.5
    g_width = max(0.0, min(1.0, g_width))

    hazard_density = geometry.get("hazard_density", 0.3)

    angle = geometry.get("dogleg_angle_deg", 0)
    g_angle = max(0.0, min(1.0, angle / 90.0))

    g_raw = 0.25 * (g_dist + g_width + hazard_density + g_angle)
    return round(max(0.1, min(1.0, g_raw)), 4)

def compute_r(risk: Dict[str, Any]) -> float:
    # R — Risk Gradient (0.1 - 1.0)
    agg = risk.get("aggressive_line", {})
    cons = risk.get("conservative_line", {})

    agg_risk = agg.get("hazard_prob", 0) * agg.get("hazard_penalty", 1.0)
    cons_risk = cons.get("hazard_prob", 0) * cons.get("hazard_penalty", 1.0)

    r_raw = agg_risk - cons_risk
    r_norm = r_raw / 0.44
    return round(max(0.1, min(1.0, r_norm)), 4)

def compute_v(variance: Dict[str, Any]) -> float:
    # V — Outcome Variance (0.1 - 1.0)
    std_dev = variance.get("std_dev", 0.5)
    v_norm = std_dev / 1.6
    return round(max(0.1, min(1.0, v_norm)), 4)

def compute_p(pressure: Dict[str, Any]) -> float:
    # P — Decision Pressure Density (0.1 - 1.0)
    dps = pressure.get("decision_points", [])

    if isinstance(dps, (int, float)):
        # Support direct numeric input from unit tests
        count = dps
        avg_weight = pressure.get("avgconsequenceweight", 0.35)
        p_raw = count * avg_weight
    elif not dps:
        return 0.1
    else:
        count = len(dps)
        avg_weight = sum(dp.get("consequence_weight", 0) for dp in dps) / count
        p_raw = count * avg_weight

    # Linear Interpolation Model for P (v0.1)
    # Calibrated to targets: (0.7, 0.35) and (1.35, 0.55)
    p_norm = (0.3077 * p_raw) + 0.1346
    return round(max(0.1, min(1.0, p_norm)), 4)

def compute_di(g: float, r: float, v: float, p: float) -> float:
    # Weighting: 30% G, 25% R, 20% V, 25% P
    di = (g * 0.30) + (r * 0.25) + (v * 0.20) + (p * 0.25)
    return round(di, 4)

def classify_di(di: float) -> str:
    if di >= 0.799:
        return "Extreme DI"
    elif di >= 0.599:
        return "High DI"
    elif di >= 0.399:
        return "Mid DI"
    else:
        return "Low DI"

def compute_confidence(variance: Dict[str, Any], samples_norm: float) -> float:
    stability = 1.0 - variance.get("variance_fluctuation", 0.2)
    consistency = 0.75

    conf = (samples_norm * 0.4) + (stability * 0.3) + (consistency * 0.3)
    return round(max(0.1, min(1.0, conf)), 4)
