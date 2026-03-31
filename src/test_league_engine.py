import unittest
from league_engine import get_format_for_di, get_scoring_multiplier, get_rivalry_trigger, get_broadcast_priority

class TestLeagueEngine(unittest.TestCase):

    def test_get_format_for_di(self):
        self.assertEqual(get_format_for_di(0.30), "Stroke Play (Execution)")
        self.assertEqual(get_format_for_di(0.45), "Match Play (Decision-Balanced)")
        self.assertEqual(get_format_for_di(0.65), "Team Formats / Alt-Shot")
        self.assertEqual(get_format_for_di(0.85), "Feature Matches Only")

    def test_get_scoring_multiplier(self):
        self.assertEqual(get_scoring_multiplier(0.30), 1.0)
        self.assertEqual(get_scoring_multiplier(0.45), 1.25)
        self.assertEqual(get_scoring_multiplier(0.65), 1.5)
        self.assertEqual(get_scoring_multiplier(0.85), 2.0)

    def test_get_rivalry_trigger(self):
        # Trigger logic: identifies the dominant difficulty factor
        # G=0.6, R=0.2, V=0.1, P=0.1 -> Compression
        self.assertEqual(get_rivalry_trigger(0.6, 0.2, 0.1, 0.1), "Compression (Skill vs Skill)")
        # G=0.1, R=0.7, V=0.1, P=0.1 -> Ignition
        self.assertEqual(get_rivalry_trigger(0.1, 0.7, 0.1, 0.1), "Ignition (Risk/Reward)")
        # G=0.1, R=0.1, V=0.8, P=0.1 -> Volatility
        self.assertEqual(get_rivalry_trigger(0.1, 0.1, 0.8, 0.1), "Volatility (Conditions)")
        # G=0.1, R=0.1, V=0.1, P=0.9 -> Escalation
        self.assertEqual(get_rivalry_trigger(0.1, 0.1, 0.1, 0.9), "Escalation (Cognitive Load)")

    def test_get_broadcast_priority(self):
        self.assertTrue("Tier 1" in get_broadcast_priority(0.65))
        self.assertTrue("Tier 2" in get_broadcast_priority(0.50))
        self.assertTrue("Tier 3" in get_broadcast_priority(0.35))
        self.assertTrue("Tier 4" in get_broadcast_priority(0.25))

if __name__ == '__main__':
    unittest.main()
