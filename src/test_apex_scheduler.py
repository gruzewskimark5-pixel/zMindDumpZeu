import unittest
from scheduling_engine import calculate_pairing_priority, compute_proximity, get_group_score, schedule_optimized_round

class TestApexScheduler(unittest.TestCase):

    def test_calculate_pairing_priority(self):
        # RHI=0.7, DI=0.6, Prox=0.8, Conf=0.9
        # 0.7 * 0.6 * 0.8 * 0.9 = 0.3024
        self.assertEqual(calculate_pairing_priority(0.7, 0.6, 0.8, 0.9), 0.3024)

    def test_compute_proximity(self):
        # 1 stroke diff, tau 2.5
        # exp(-1/2.5) = exp(-0.4) = 0.6703
        self.assertAlmostEqual(compute_proximity(72, 73, tau=2.5), 0.6703, delta=0.001)
        # 5 strokes diff, tau 2.5
        # exp(-5/2.5) = exp(-2.0) = 0.1353
        self.assertAlmostEqual(compute_proximity(70, 75, tau=2.5), 0.1353, delta=0.001)

    def test_get_group_score(self):
        players = [{"id": "A"}, {"id": "B"}, {"id": "C"}]
        rhi_matrix = {
            "A": {"B": 0.8, "C": 0.5},
            "B": {"A": 0.8, "C": 0.4},
            "C": {"A": 0.5, "B": 0.4}
        }
        # DI=0.6. AB(0.8*0.6) + AC(0.5*0.6) + BC(0.4*0.6)
        # 0.48 + 0.30 + 0.24 = 1.02 (Assuming prox=1.0, conf=1.0)
        score = get_group_score(players, rhi_matrix, 0.6)
        # Assuming get_group_score uses conf=0.8 as in implementation
        # 0.8*(0.8*0.6 + 0.5*0.6 + 0.4*0.6) = 0.8*1.7*0.6 = 0.816
        self.assertAlmostEqual(score, 0.816, delta=0.01)

    def test_schedule_optimized_round(self):
        player_pool = [{"id": f"P{i}"} for i in range(1, 10)]
        rhi_matrix = {
            "P1": {"P2": 0.9, "P3": 0.8},
            "P2": {"P1": 0.9, "P3": 0.7},
            "P3": {"P1": 0.8, "P2": 0.7}
        }
        slots = [
            {"slot_id": "S_final", "di_context": 0.75},
            {"slot_id": "S_early", "di_context": 0.40},
            {"slot_id": "S_mid", "di_context": 0.55}
        ]
        schedule = schedule_optimized_round(player_pool, rhi_matrix, slots, group_size=3)

        # S_final (DI 0.75) should have P1, P2, P3 if they are available and have best RHI
        self.assertEqual(schedule[0]["slot_id"], "S_final")
        self.assertTrue("P1" in schedule[0]["group"])
        self.assertTrue("P2" in schedule[0]["group"])
        self.assertTrue("P3" in schedule[0]["group"])

if __name__ == '__main__':
    unittest.main()
