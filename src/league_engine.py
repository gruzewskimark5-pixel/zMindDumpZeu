from typing import Dict, Any, List

def get_format_for_di(di: float) -> str:
    if di <= 0.35:
        return "Stroke Play (Execution)"
    elif di <= 0.55:
        return "Match Play (Decision-Balanced)"
    elif di <= 0.70:
        return "Team Formats / Alt-Shot"
    else:
        return "Feature Matches Only"

def get_scoring_multiplier(di: float) -> float:
    if di <= 0.35:
        return 1.0
    elif di <= 0.55:
        return 1.25
    elif di <= 0.70:
        return 1.5
    else:
        return 2.0

def get_rivalry_trigger(g: float, r: float, v: float, p: float) -> str:
    # Trigger logic: identifies the dominant difficulty factor
    components = {
        "Compression (Skill vs Skill)": g,
        "Ignition (Risk/Reward)": r,
        "Volatility (Conditions)": v,
        "Escalation (Cognitive Load)": p
    }
    return max(components, key=components.get)

def get_broadcast_priority(di: float) -> str:
    if di >= 0.60:
        return "Tier 1: Dedicated camera, live DI overlay, predictive graphics"
    elif di >= 0.45:
        return "Tier 2: Shared camera, decision-tree overlays"
    elif di >= 0.30:
        return "Tier 3: Standard coverage"
    else:
        return "Tier 4: Minimal coverage (reset holes)"

def get_player_identity_hash(performance_by_di: Dict[str, float]) -> Dict[str, float]:
    # Placeholder for player identity mapping
    return {
        "execution_score": performance_by_di.get("low_di", 0.0),
        "decision_score": performance_by_di.get("mid_di", 0.0),
        "pressure_score": performance_by_di.get("high_di", 0.0),
        "chaos_score": performance_by_di.get("extreme_di", 0.0)
    }

def generate_league_match_spec(hole_data: Dict[str, Any]) -> Dict[str, Any]:
    di = hole_data.get("DI", 0.5)
    g, r, v, p = hole_data.get("G", 0), hole_data.get("R", 0), hole_data.get("V", 0), hole_data.get("P", 0)

    return {
        "hole_id": hole_data.get("hole_id"),
        "format": get_format_for_di(di),
        "multiplier": get_scoring_multiplier(di),
        "rivalry_trigger": get_rivalry_trigger(g, r, v, p),
        "broadcast_priority": get_broadcast_priority(di)
    }
