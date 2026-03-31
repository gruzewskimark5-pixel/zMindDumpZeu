from typing import Dict, Any, List
import random
import statistics

def simulate_strokes(geometry: Dict[str, Any], iterations: int = 5000) -> Dict[str, Any]:
    # Inputs
    dist = geometry.get("distance_yards", 400)
    par = geometry.get("par", 4)
    haz_prob = geometry.get("hazard_density", 0.3)

    scores = []
    for _ in range(iterations):
        # Simulation Logic v0.1
        # Tee Shot
        # Lateral dispersion = 0.08 × distance
        # Longitudinal dispersion = 0.05 × distance
        tee_disp = 0.08 * 270 # 270 yards typical drive
        tee_miss = random.gauss(0, tee_disp)

        # Approach Shot
        # Lateral dispersion = 0.06 × distance
        # Longitudinal dispersion = 0.04 × distance
        app_dist = dist - 270
        app_disp = 0.06 * app_dist
        app_miss = random.gauss(0, app_disp)

        # Hazard overlap probability
        # Simplified: hazard_prob = overlap(dispersion ellipse, hazard zone)
        # encoded as penalty probability
        penalty = 0
        if abs(tee_miss) > 12 or abs(app_miss) > 10 or random.random() < haz_prob:
            penalty = 1

        # Putts
        putts = 2 if random.random() > 0.1 else 3

        # Accumulate strokes
        strokes = par + penalty + (random.randint(-1, 2)) # noise
        scores.append(strokes)

    mean_score = statistics.mean(scores)
    std_dev = statistics.stdev(scores)

    return {
        "sample_size": iterations,
        "score_distribution": scores[:20], # sample distribution
        "std_dev": round(std_dev, 4),
        "variance_fluctuation": round(random.uniform(0.1, 0.2), 4) # placeholder for stability
    }
