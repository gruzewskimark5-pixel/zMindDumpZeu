from di_engine import compute_g, compute_r, compute_v, compute_p, compute_di, classify_di, compute_confidence
from decision_detector import detect_all_decision_points
from dispersion_model import simulate_strokes
import json

def run_di_hole14():
    print("Running DI Engine v0.1 — Validation: Hole 14 (Defining Hole)")

    # Pure committed line, narrow window, water in play, no true bailout. Precision > creativity.
    # Assumed geometry (v0.1 test profile)
    hole_14_geometry = {
      "hole_id": "miakka_14",
      "par": 4,
      "distance_yards": 425,
      "landing_zones": [
        {
          "lz_id": 1,
          "distance": 265,
          "fairway_width": 24, # Narrower for ~70 DI target
          "hazard_proximity": {
            "left": 10,
            "right": 12,
            "carry": 230
          },
          "hazard_types": ["water", "bunker"]
        }
      ],
      "dogleg_angle_deg": 8,
      "forced_carry_yards": 230,
      "hazard_density": 0.70 # Precision, commitment, no real bailout
    }

    # Risk Model
    # Pure committed line, narrow window, water in play, no true bailout.
    # Precision > creativity.
    risk_model_14 = {
        "hole_id": "miakka_14",
        "aggressive_line": {
            "target_lz": 1,
            "hazard_prob": 0.45,
            "hazard_penalty": 1.0 # water-dominant
        },
        "conservative_line": {
            "target_lz": 1, # no true bailout if you want par
            "hazard_prob": 0.10,
            "hazard_penalty": 0.6 # bunker/rough mix
        }
    }

    # P Component: Decision Point Detection
    # Pure committed line, narrow window, water in play, no true bailout.
    # Precision > creativity.
    dps = detect_all_decision_points(hole_14_geometry)
    decision_pressure_14 = {
        "hole_id": "miakka_14",
        "decision_points": dps
    }

    # R & V Backbone: Dispersion Model Simulation
    # Precision hole → outcomes cluster tightly around 4, with some 5s and a few 6s.
    sim_results = simulate_strokes(hole_14_geometry, iterations=5000)
    outcome_variance_14 = {
        "hole_id": "miakka_14",
        "sample_size": sim_results["sample_size"],
        "score_distribution": sim_results["score_distribution"],
        "std_dev": sim_results["std_dev"],
        "variance_fluctuation": sim_results["variance_fluctuation"]
    }

    # Component Computation
    g = compute_g(hole_14_geometry)
    r = compute_r(risk_model_14)
    v = compute_v(outcome_variance_14)
    p = compute_p(decision_pressure_14)

    # DI Assembly
    di = compute_di(g, r, v, p)
    classification = classify_di(di)
    confidence = compute_confidence(outcome_variance_14, 0.4) # sim-heavy

    output = {
        "hole_id": "miakka_14",
        "G": g,
        "R": r,
        "V": v,
        "P": p,
        "DI": di,
        "DI_100": int(di * 100),
        "confidence": confidence,
        "classification": classification,
        "operator_notes": "Precision, commitment, no real bailout if you want par."
    }

    print(json.dumps(output, indent=2))
    return output

if __name__ == "__main__":
    run_di_hole14()
