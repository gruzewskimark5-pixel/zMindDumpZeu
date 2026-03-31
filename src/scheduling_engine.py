from typing import Dict, Any, List, Optional
import math

# --- Hardened Competitive OS v0.1: Apex Scheduling Engine ---

def calculate_pairing_priority(rhi: float, di: float, proximity: float = 1.0, confidence: float = 1.0) -> float:
    # Objective Function: Score(pair) = RHI_sym * DI_context * Proximity * Confidence
    # RHI = [0, 1], DI = [0, 1], Proximity = [0, 1], Confidence = [0, 1]
    priority = rhi * di * proximity * confidence
    return round(priority, 4)

def compute_proximity(score_a: int, score_b: int, tau: float = 2.5) -> float:
    # Proximity(i,j) = exp(-|strokes_i - strokes_j| / tau)
    diff = abs(score_a - score_b)
    prox = math.exp(-diff / tau)
    return round(prox, 4)

def get_group_score(players: List[Dict[str, Any]], rhi_matrix: Dict[str, Dict[str, float]], di_context: float) -> float:
    # GroupScore(g, s) = Σ_{i<j in g} PairScore(i,j,s)
    total_score = 0.0
    for i in range(len(players)):
        for j in range(i + 1, len(players)):
            p1, p2 = players[i], players[j]
            # Use max(RHI_ab, RHI_ba) as symmetric proxy
            rhi_ab = rhi_matrix.get(p1["id"], {}).get(p2["id"], 0.1)
            rhi_ba = rhi_matrix.get(p2["id"], {}).get(p1["id"], 0.1)
            rhi_sym = max(rhi_ab, rhi_ba)

            # Assume proximity 1.0 for initial scheduling (unless leaderboard provided)
            prox = compute_proximity(p1.get("score", 0), p2.get("score", 0)) if "score" in p1 and "score" in p2 else 1.0
            conf = p1.get("confidence", 0.8) # Simplification for v0.1

            total_score += calculate_pairing_priority(rhi_sym, di_context, prox, conf)

    return round(total_score, 4)

def schedule_optimized_round(
    player_pool: List[Dict[str, Any]],
    rhi_matrix: Dict[str, Dict[str, float]],
    slots: List[Dict[str, Any]],
    group_size: int = 3
) -> List[Dict[str, Any]]:
    # Greedy Solver Strategy for Apex Scheduler v0.1

    available_players = list(player_pool)
    schedule = []

    # Sort slots by DI context descending to place hottest groups in highest pressure slots
    sorted_slots = sorted(slots, key=lambda x: x["di_context"], reverse=True)

    for slot in sorted_slots:
        slot_id = slot["slot_id"]
        di_context = slot["di_context"]

        # Build one group per slot for simplicity in v0.1 demo
        if not available_players: break

        # Seed group with top available pair by RHI
        best_seed = None
        best_rhi = -1.0

        for i in range(len(available_players)):
            for j in range(i + 1, len(available_players)):
                p1, p2 = available_players[i], available_players[j]
                rhi = max(rhi_matrix.get(p1["id"], {}).get(p2["id"], 0.1),
                          rhi_matrix.get(p2["id"], {}).get(p1["id"], 0.1))
                if rhi > best_rhi:
                    best_rhi = rhi
                    best_seed = [p1, p2]

        if not best_seed: break

        current_group = list(best_seed)
        for p in current_group: available_players.remove(p)

        # Expand group to group_size
        while len(current_group) < group_size and available_players:
            best_addition = None
            max_inc_score = -1.0

            for p in available_players:
                inc_score = get_group_score(current_group + [p], rhi_matrix, di_context)
                if inc_score > max_inc_score:
                    max_inc_score = inc_score
                    best_addition = p

            if best_addition:
                current_group.append(best_addition)
                available_players.remove(best_addition)
            else:
                break

        schedule.append({
            "slot_id": slot_id,
            "di_context": di_context,
            "group": [p["id"] for p in current_group],
            "group_score": get_group_score(current_group, rhi_matrix, di_context)
        })

    return schedule
