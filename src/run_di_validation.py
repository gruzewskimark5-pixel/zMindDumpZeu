from di_engine import compute_g, compute_r, compute_v, compute_p, compute_di, classify_di, compute_confidence
from decision_detector import detect_all_decision_points
from dispersion_model import simulate_strokes
import json

def run_di_validation():
    print("Running DI Engine v0.1 — Validation: (3, 7, 14)")

    # Target: DI ≈ 0.49
    hole_3_geometry = {
        "hole_id": "miakka_3",
        "par": 4,
        "distance_yards": 395,
        "landing_zones": [{"lz_id": 1, "distance": 270, "fairway_width": 24}],
        "dogleg_angle_deg": 18,
        "hazard_density": 0.55
    }
    risk_model_3 = {
        "aggressive_line": {"hazard_prob": 0.35, "hazard_penalty": 0.75},
        "conservative_line": {"hazard_prob": 0.10, "hazard_penalty": 0.3}
    }

    # Target: DI ≈ 0.59
    hole_7_geometry = {
        "hole_id": "miakka_7",
        "par": 3,
        "distance_yards": 188,
        "landing_zones": [{"lz_id": 1, "distance": 188, "fairway_width": 28}],
        "dogleg_angle_deg": 35, # Elevated/Exposed signal
        "hazard_density": 0.85
    }
    risk_model_7 = {
        "aggressive_line": {"hazard_prob": 0.40, "hazard_penalty": 0.7},
        "conservative_line": {"hazard_prob": 0.15, "hazard_penalty": 0.3}
    }

    # Target: DI ≈ 0.60
    hole_14_geometry = {
      "hole_id": "miakka_14",
      "par": 4,
      "distance_yards": 425,
      "landing_zones": [{"lz_id": 1, "distance": 265, "fairway_width": 24}],
      "dogleg_angle_deg": 8,
      "hazard_density": 0.70
    }
    risk_model_14 = {
        "aggressive_line": {"hazard_prob": 0.45, "hazard_penalty": 1.0},
        "conservative_line": {"hazard_prob": 0.10, "hazard_penalty": 0.6}
    }

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
