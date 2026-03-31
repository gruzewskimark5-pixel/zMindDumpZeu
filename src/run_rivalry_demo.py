from rivalry_engine import compute_performance_delta, compute_di_weighted_context, compute_identity_divergence, compute_event_triggers, update_rhi, get_heat_band
import json
import time

def run_rivalry_demo():
    print("Running Rivalry Heat Engine v0.1 — Demo: Miakka Matchup")

    # Player A: Pressure Strategist
    player_a = {
        "id": "player-a-uuid",
        "traits": {"execution": 0.8, "decision": 0.9, "pressure": 0.95, "chaos": 0.2}
    }

    # Player B: Chaos Maverick
    player_b = {
        "id": "player-b-uuid",
        "traits": {"execution": 0.6, "decision": 0.3, "pressure": 0.7, "chaos": 0.95}
    }

    # Match Result: A beats B by 4 strokes
    # Context: A outperforms B significantly on the high DI stretch (16-18)
    shared_holes = [
        {"hole_id": 16, "DI": 0.68, "score_a": 4, "score_b": 6}, # B blown lead
        {"hole_id": 17, "DI": 0.59, "score_a": 3, "score_b": 3},
        {"hole_id": 18, "DI": 0.62, "score_a": 4, "score_b": 5}  # Walk-off win
    ]

    # Events
    events = [
        {"event_type": "lead_change_high_di", "weight": 0.15, "description": "Lead change on hole 16 (DI 0.68)"},
        {"event_type": "walk_off_win", "weight": 0.20, "description": "Walk-off win on hole 18 (DI 0.62)"},
        {"event_type": "upset", "weight": 0.15, "description": "A upset B"}
    ]

    # Initial RHI: emerging tension
    initial_rhi = 0.35

    # Component Calculation
    d_ab = compute_performance_delta(72, 76)
    di_ab = compute_di_weighted_context(shared_holes)
    id_ab = compute_identity_divergence(player_a["traits"], player_b["traits"])
    e_ab = compute_event_triggers(events)
    decay_ab = 0.05 # Recent interaction

    # Update RHI
    new_rhi = update_rhi(initial_rhi, d_ab, di_ab, id_ab, e_ab, decay_ab)
    band = get_heat_band(new_rhi)

    demo_output = {
        "matchup": "Player A vs Player B",
        "initial_rhi": initial_rhi,
        "delta_performance": d_ab,
        "di_weighted_context": di_ab,
        "identity_divergence": id_ab,
        "event_trigger_sum": e_ab,
        "new_rhi": new_rhi,
        "band": band,
        "narrative": f"A clashing of archetypes ({player_a['id']} vs {player_b['id']}) exploded on the closing stretch. A out-performed B on high DI holes 16 and 18, triggering a {band} shift."
    }

    print(json.dumps(demo_output, indent=2))
    return demo_output

if __name__ == "__main__":
    run_rivalry_demo()
