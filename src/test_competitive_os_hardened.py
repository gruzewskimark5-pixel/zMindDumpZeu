import unittest
from rivalry_engine import compute_performance_delta, compute_di_weighted_context, compute_identity_divergence, compute_event_triggers, update_rhi, get_heat_band, update_momentum, update_streaming_variance, compute_priority
from league_engine import get_format_for_di, get_scoring_multiplier, get_rivalry_trigger, get_broadcast_priority
from scheduling_engine import calculate_pairing_priority, schedule_optimized_round

class TestCompetitiveOSHardened(unittest.TestCase):

    # --- 1. Hardened Rivalry Engine ---
    def test_ema_momentum(self):
        # Initial momentum 0, current event delta 0.8, gamma 0.3
        self.assertEqual(update_momentum(0, 0.8), 0.24)
        self.assertEqual(update_momentum(0.24, 0.8), 0.408)

    def test_streaming_variance_welford(self):
        count, mean, m2, var = update_streaming_variance(1, 1.0, 0.0, 2.0)
        self.assertEqual(var, 0.5)
        count, mean, m2, var = update_streaming_variance(count, mean, m2, 3.0)
        self.assertEqual(var, 1.0)

    def test_update_rhi_nonlinear(self):
        # current = 0.4, D=0.8, DI=0.5, ID=0.5, E=0.5, Decay=0.0
        new_rhi, momentum, delta = update_rhi(0.4, 0.8, 0.5, 0.5, 0.5, 0.0, 0.0)
        self.assertAlmostEqual(new_rhi, 0.7304, delta=0.001)
        self.assertEqual(get_heat_band(new_rhi), "Volatile")

    # --- 2. Apex Scheduling Engine ---
    def test_calculate_pairing_priority(self):
        # RHI=0.7, DI=0.6, Prox=1.0 (default), Conf=1.0 (default)
        # 0.7 * 0.6 * 1.0 * 1.0 = 0.42
        self.assertAlmostEqual(calculate_pairing_priority(0.7, 0.6), 0.42, delta=0.001)

if __name__ == '__main__':
    unittest.main()
