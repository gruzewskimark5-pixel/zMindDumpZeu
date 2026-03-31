import unittest
from di_engine import compute_g, compute_r, compute_v, compute_p, compute_di, classify_di, compute_confidence
from decision_detector import detect_all_decision_points
from dispersion_model import simulate_strokes

class TestDIEngine(unittest.TestCase):

    # --- 1A. Geometry Complexity (G) Unit Tests ---
    def test_g_basic_geometry(self):
        geom = {
            "distance_yards": 420,
            "landing_zones": [{"fairway_width": 28}],
            "hazard_density": 0.40,
            "dogleg_angle_deg": 24.3
        }
        g = compute_g(geom)
        self.assertAlmostEqual(g, 0.45, delta=0.03)

    def test_g_narrow_fairway_high_hazard(self):
        geom = {
            "distance_yards": 445,
            "landing_zones": [{"fairway_width": 20}],
            "hazard_density": 0.70,
            "dogleg_angle_deg": 0.0
        }
        g = compute_g(geom)
        self.assertAlmostEqual(g, 0.55, delta=0.03)

    # --- 1B. Risk Gradient (R) Unit Tests ---
    def test_r_balanced_risk(self):
        risk = {
            "aggressive_line": {"hazard_prob": 0.30, "hazard_penalty": 1.0},
            "conservative_line": {"hazard_prob": 0.12, "hazard_penalty": 0.5}
        }
        r = compute_r(risk)
        self.assertAlmostEqual(r, 0.55, delta=0.05)

    def test_r_committed_line_high_risk(self):
        risk = {
            "aggressive_line": {"hazard_prob": 0.45, "hazard_penalty": 1.0},
            "conservative_line": {"hazard_prob": 0.10, "hazard_penalty": 0.6}
        }
        r = compute_r(risk)
        self.assertAlmostEqual(r, 0.85, delta=0.05)

    # --- 1C. Outcome Variance (V) Unit Tests ---
    def test_v_low_variance(self):
        v = compute_v({"std_dev": 0.40})
        self.assertAlmostEqual(v, 0.25, delta=0.03)

    def test_v_high_variance_wind(self):
        v = compute_v({"std_dev": 1.10})
        self.assertAlmostEqual(v, 0.73, delta=0.05)

    # --- 1D. Decision Pressure (P) Unit Tests ---
    def test_p_two_decisions_moderate_consequence(self):
        pressure = {
            "decision_points": 2,
            "avgconsequenceweight": 0.35
        }
        p = compute_p(pressure)
        self.assertAlmostEqual(p, 0.35, delta=0.03)

    def test_p_three_decisions_high_consequence(self):
        pressure = {
            "decision_points": 3,
            "avgconsequenceweight": 0.45
        }
        p = compute_p(pressure)
        self.assertAlmostEqual(p, 0.55, delta=0.04)

    # --- 2. INTEGRATION TESTS ---
    def test_integration_hole_3(self):
        # Target: G: 0.45, R: 0.55, V: 0.35, P: 0.50, DI: 0.49
        g, r, v, p = 0.45, 0.55, 0.35, 0.50
        di = compute_di(g, r, v, p)
        self.assertAlmostEqual(di, 0.49, delta=0.03)

    def test_integration_hole_7(self):
        # Target: G: 0.60, R: 0.50, V: 0.75, P: 0.50, DI: 0.59
        g, r, v, p = 0.60, 0.50, 0.75, 0.50
        di = compute_di(g, r, v, p)
        self.assertAlmostEqual(di, 0.59, delta=0.04)

    def test_integration_hole_14(self):
        # Target: G: 0.53, R: 0.87, V: 0.40, P: 0.57, DI: 0.60
        g, r, v, p = 0.53, 0.87, 0.40, 0.57
        di = compute_di(g, r, v, p)
        self.assertAlmostEqual(di, 0.60, delta=0.03)
        self.assertEqual(classify_di(di), "High DI")

if __name__ == '__main__':
    unittest.main()
