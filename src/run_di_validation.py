from di_engine import compute_g, compute_r, compute_v, compute_p, compute_di, classify_di, compute_confidence
from decision_detector import detect_all_decision_points
from dispersion_model import simulate_strokes
import json

def run_di_validation():
    print("Running DI Engine v0.1 — Validation: (3, 7, 14)")

    # 🧩 Hole 3 — “First Decision Tree” (v0.1 representative)
    # Design intent: early fork, introduces strategy without being lethal.
    # Target DI: 45–55.
    hole_3_geometry = {
        "hole_id": "miakka_3",
        "par": 4,
        "distance_yards": 395,
        "landing_zones": [
            {"lz_id": 1, "distance": 270, "fairway_width": 24, "hazard_proximity": {"left": 10, "right": 8, "carry": 0}, "hazard_types": ["bunker", "rough"]},
            {"lz_id": 2, "distance": 245, "fairway_width": 32, "hazard_proximity": {"left": 20, "right": 18, "carry": 0}, "hazard_types": ["rough"]}
        ],
        "dogleg_angle_deg": 18,
        "forced_carry_yards": 0,
        "hazard_density": 0.55
    }

    # Risk Model
    risk_model_3 = {
        "hole_id": "miakka_3",
        "aggressive_line": {"target_lz": 1, "hazard_prob": 0.35, "hazard_penalty": 0.75},
        "conservative_line": {"target_lz": 2, "hazard_prob": 0.10, "hazard_penalty": 0.3}
    }

    # 🌬 Hole 7 — “Drift Detector” (v0.1 representative)
    # Design intent: wind + exposure + length → tests discipline and control.
    # Target DI: 55–65.
    hole_7_geometry = {
        "hole_id": "miakka_7",
        "par": 3,
        "distance_yards": 188,
        "landing_zones": [
            {"lz_id": 1, "distance": 188, "fairway_width": 28, "hazard_proximity": {"left": 5, "right": 5, "carry": 0}, "hazard_types": ["bunker"]}
        ],
        "dogleg_angle_deg": 0,
        "forced_carry_yards": 0,
        "hazard_density": 0.85 # High hazard density to simulate exposure + wind dispersion impact
    }

    # Risk Model
    risk_model_7 = {
        "hole_id": "miakka_7",
        "aggressive_line": {"target_lz": 1, "hazard_prob": 0.40, "hazard_penalty": 0.7},
        "conservative_line": {"target_lz": 1, "hazard_prob": 0.15, "hazard_penalty": 0.3}
    }

    # 🔥 Hole 14 — “Committed-line Test” (v0.1 locked)
    # Design intent: pure commitment, precision under pressure.
    # Target DI: 60-75 (Defining Hole)
    hole_14_geometry = {
      "hole_id": "miakka_14",
      "par": 4,
      "distance_yards": 425,
      "landing_zones": [
        {"lz_id": 1, "distance": 265, "fairway_width": 24, "hazard_proximity": {"left": 10, "right": 12, "carry": 230}, "hazard_types": ["water", "bunker"]}
      ],
      "dogleg_angle_deg": 8,
      "forced_carry_yards": 230,
      "hazard_density": 0.70
    }

    # Risk Model
    risk_model_14 = {
        "hole_id": "miakka_14",
        "aggressive_line": {"target_lz": 1, "hazard_prob": 0.45, "hazard_penalty": 1.0},
        "conservative_line": {"target_lz": 1, "hazard_prob": 0.10, "hazard_penalty": 0.6}
    }

    # Results
    holes = [(hole_3_geometry, risk_model_3), (hole_7_geometry, risk_model_7), (hole_14_geometry, risk_model_14)]

    print("| Hole | G | R | V | P | DI_100 | Classification |")
    print("|------|---|---|---|---|--------|----------------|")

    for geom, risk in holes:
        dps = detect_all_decision_points(geom)
        sim_results = simulate_strokes(geom, iterations=5000)

        g = compute_g(geom)
        r = compute_r(risk)
        v = compute_v({"std_dev": sim_results["std_dev"]})
        p = compute_p({"decision_points": dps})

        di = compute_di(g, r, v, p)
        di_100 = int(di * 100)
        classification = classify_di(di)

        print(f"| {geom['hole_id']} | {g} | {r} | {v} | {p} | {di_100} | {classification} |")

if __name__ == "__main__":
    run_di_validation()
