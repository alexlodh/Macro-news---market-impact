import unittest
from src.fetchers import get_fingerprint
from src.config import Config
from src.models import Headline, Classification, ClassifiedItem

class TestMacroAgent(unittest.TestCase):

    def test_fingerprint_logic(self):
        f1 = get_fingerprint("Title A", "http://a.com")
        f2 = get_fingerprint("Title A", "http://a.com")
        f3 = get_fingerprint("Title B", "http://b.com")
        
        self.assertEqual(f1, f2)
        self.assertNotEqual(f1, f3)

    def test_classification_model(self):
        # Ensure we can instantiate properly
        c = Classification(
            topic="inflation",
            stance="hawkish",
            relevance="high",
            relevance_score=9,
            expected_impact="rates",
            impact_direction="Bullish Yields",
            rationale="News implies higher CPI",
            confidence="high"
        )
        self.assertEqual(c.relevance_score, 9)

    def test_config_defaults(self):
        cfg = Config()
        self.assertTrue(len(cfg.feeds) > 0)
        self.assertTrue(1 <= cfg.relevance_threshold <= 10)

if __name__ == '__main__':
    unittest.main()
