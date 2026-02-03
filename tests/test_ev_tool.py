import unittest

from ev_tool.ev import american_to_implied_prob, expected_value
from ev_tool.main import compute_ev, load_models, load_sample_data


class TestEVTool(unittest.TestCase):
    def test_american_to_implied_prob(self) -> None:
        self.assertAlmostEqual(american_to_implied_prob(100), 0.5)
        self.assertAlmostEqual(american_to_implied_prob(-110), 110 / 210)

    def test_expected_value_positive(self) -> None:
        value = expected_value(0.6, 120)
        self.assertGreater(value, 0)

    def test_compute_ev_with_sample(self) -> None:
        payload = load_sample_data()
        projections, odds_list = load_models(payload)
        plays = compute_ev(projections, odds_list)
        self.assertTrue(plays)
        self.assertGreaterEqual(plays[0].expected_value, plays[-1].expected_value)


if __name__ == "__main__":
    unittest.main()
