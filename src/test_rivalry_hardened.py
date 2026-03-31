import unittest
from rivalry_engine import compute_performance_delta, compute_di_weighted_context, compute_identity_divergence, compute_event_triggers, apply_decay, update_rhi, get_heat_band, update_momentum, update_streaming_variance

class TestRivalryEngineHardened(unittest.TestCase):

    def test_ema_momentum(self):
        # Initial momentum 0, current event delta 0.8, gamma 0.3
        # (1-0.3)*0 + 0.3*0.8 = 0.24
        self.assertEqual(update_momentum(0, 0.8), 0.24)
        # Next step: (1-0.3)*0.24 + 0.3*0.8 = 0.168 + 0.24 = 0.408
        self.assertEqual(update_momentum(0.24, 0.8), 0.408)

    def test_streaming_variance_welford(self):
        # x = [1, 2, 3]
        # count=1, mean=1, m2=0
        # step 2: count=2, delta=2-1=1, mean=1+1/2=1.5, delta2=2-1.5=0.5, m2=0 + 1*0.5=0.5
        # var = 0.5/(2-1) = 0.5. (stdev=0.707)
        count, mean, m2, var = update_streaming_variance(1, 1.0, 0.0, 2.0)
        self.assertEqual(var, 0.5)
        # step 3: count=3, delta=3-1.5=1.5, mean=1.5+1.5/3=2, delta2=3-2=1, m2=0.5 + 1.5*1=2.0
        # var = 2.0/(3-1) = 1.0. (stdev=1.0)
        count, mean, m2, var = update_streaming_variance(count, mean, m2, 3.0)
        self.assertEqual(var, 1.0)

    def test_update_rhi_nonlinear(self):
        # current = 0.4, D=0.8, DI=0.5, ID=0.5, E=0.5, Decay=0.0
        # delta_event = 0.3*0.8 + 0.25*0.5 + 0.25*0.5 + 0.2*0.5 = 0.24 + 0.125 + 0.125 + 0.1 = 0.59
        # new_momentum = 0.3 * 0.59 = 0.177
        # new_rhi = 0.4 + (0.5 * 0.59) + (0.2 * 0.177) = 0.4 + 0.295 + 0.0354 = 0.7304
        new_rhi, momentum, delta = update_rhi(0.4, 0.8, 0.5, 0.5, 0.5, 0.0, 0.0)
        self.assertAlmostEqual(new_rhi, 0.7304, delta=0.001)

if __name__ == '__main__':
    unittest.main()
