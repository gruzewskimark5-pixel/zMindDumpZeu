from typing import Dict, Any, List

def detect_tee_line_choice(geometry: Dict[str, Any]) -> Dict[str, Any]:
    # Rules:
    # - If two landing zones differ by > 15 yards in width → decision point
    # - If hazard proximity differs by > 10 yards → decision point
    # - If dogleg angle > 25° → decision point
    lzs = geometry.get("landing_zones", [])
    angle = geometry.get("dogleg_angle_deg", 0)

    if len(lzs) >= 2:
        width_diff = abs(lzs[0].get("fairway_width", 0) - lzs[1].get("fairway_width", 0))
        # Hazard proximity logic simplified for v0.1
        if width_diff > 15:
            return {"type": "teeline_choice", "consequence_weight": 0.4}

    if angle > 25:
        return {"type": "teeline_choice", "consequence_weight": 0.3}

    return {}

def detect_layup_vs_attack(geometry: Dict[str, Any]) -> Dict[str, Any]:
    # Rules:
    # - Par 5 OR long par 4
    # - Hazard within 20 yards of green
    # - Forced carry > 150 yards
    par = geometry.get("par", 4)
    dist = geometry.get("distance_yards", 0)
    forced_carry = geometry.get("forced_carry_yards", 0)

    if (par == 5) or (par == 4 and dist > 440):
        return {"type": "layupvs_attack", "consequence_weight": 0.5}

    if forced_carry > 150:
        return {"type": "layupvs_attack", "consequence_weight": 0.6}

    return {}

def detect_recovery_vs_hero(geometry: Dict[str, Any]) -> Dict[str, Any]:
    # Rules:
    # - Hazard density > 0.4
    # - Rough penalty > threshold (simplified)
    # - Obstruction angle > 20° (simplified)
    hazard_density = geometry.get("hazard_density", 0.0)

    if hazard_density > 0.4:
        return {"type": "recoveryvs_hero", "consequence_weight": 0.35}

    return {}

def detect_greenside_choice(geometry: Dict[str, Any]) -> Dict[str, Any]:
    # Rules:
    # - Multi-tier green (simplified)
    # - Bunker within 5 yards
    # - False front or runoff
    # Use LZ hazards as green proxy if needed or geometry flags
    # Simplified for v0.1
    hazard_density = geometry.get("hazard_density", 0.0)
    if hazard_density > 0.6:
        return {"type": "greenside_choice", "consequence_weight": 0.2}
    return {}

def detect_all_decision_points(geometry: Dict[str, Any]) -> List[Dict[str, Any]]:
    points = []

    p1 = detect_tee_line_choice(geometry)
    if p1: points.append(p1)

    p2 = detect_layup_vs_attack(geometry)
    if p2: points.append(p2)

    p3 = detect_recovery_vs_hero(geometry)
    if p3: points.append(p3)

    p4 = detect_greenside_choice(geometry)
    if p4: points.append(p4)

    return points
