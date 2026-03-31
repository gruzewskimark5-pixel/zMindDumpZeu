import unittest
from rivalry_engine import compute_performance_delta, compute_di_weighted_context, compute_identity_divergence, compute_event_triggers, apply_decay, update_rhi, get_heat_band

class TestRivalryEngine(unittest.TestCase):

    def test_compute_performance_delta(self):
        # A beats B by 3 -> positive for A vs B
        # score_B - score_A = 3. 3/5 = 0.6. (0.6+1)/2 = 0.8
        self.assertEqual(compute_performance_delta(70, 73), 0.8)

    def test_compute_di_weighted_context(self):
        # Shared holes: score_b - score_a = 1 on DI 0.6 hole
        shared_holes = [{"score_a": 4, "score_b": 5, "DI": 0.6}]
        # 1 * 0.6 = 0.6. 0.6/10 = 0.06. (0.06+1)/2 = 0.53
        self.assertEqual(compute_di_weighted_context(shared_holes), 0.53)

    def test_compute_identity_divergence(self):
        a = {"execution": 0.8, "decision": 0.4, "pressure": 0.9, "chaos": 0.1}
        b = {"execution": 0.2, "decision": 0.9, "pressure": 0.3, "chaos": 0.8}
        # (0.6 + 0.5 + 0.6 + 0.7) / 4 = 2.4 / 4 = 0.6
        self.assertEqual(compute_identity_divergence(a, b), 0.6)

    def test_compute_event_triggers(self):
        events = [{"weight": 0.15}, {"weight": 0.20}]
        self.assertEqual(compute_event_triggers(events), 0.35)

    def test_apply_decay(self):
        # 30 days = full decay (1.0). 7 days = 0.2333
        now = 100 * 24 * 3600
        last = 93 * 24 * 3600
        self.assertAlmostEqual(apply_decay(last, now), 0.2333, delta=0.01)

    def test_update_rhi(self):
        # Base formula: 0.30 D + 0.25 DI + 0.25 ID + 0.20 E - 0.15 Decay
        # current = 0.4. D = 0.8. DI = 0.53. ID = 0.6. E = 0.35. Decay = 0.23
        # 0.3*0.8 + 0.25*0.53 + 0.25*0.6 + 0.2*0.35 - 0.15*0.23
        # 0.24 + 0.1325 + 0.15 + 0.07 - 0.0345 = 0.558
        new_rhi = update_rhi(0.4, 0.8, 0.53, 0.6, 0.35, 0.23)
        self.assertAlmostEqual(new_rhi, 0.4 + 0.558, delta=0.001)

    def test_get_heat_band(self):
        self.assertEqual(get_heat_band(0.1), "Cold")
        self.assertEqual(get_heat_band(0.3), "Warm")
        self.assertEqual(get_heat_band(0.5), "Hot")
        self.assertEqual(get_heat_band(0.7), "Volatile")
        self.assertEqual(get_heat_band(0.9), "Nuclear")

if __name__ == '__main__':
    unittest.main()
