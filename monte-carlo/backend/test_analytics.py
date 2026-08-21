import unittest
import numpy as np

from backend.analytics import (
    calculate_mean,
    calculate_median,
    calculate_var,
    calculate_tvar,
    calculate_attachment_probability,
    calculate_exhaustion_probability,
    calculate_average_attaching_claims,
    calculate_treaty_utilization,
)


class TestAnalytics(unittest.TestCase):

    def test_mean(self):
        values = np.array([10, 20, 30, 40])

        result = calculate_mean(values)

        self.assertEqual(result, 25.0)

    def test_median(self):
        values = np.array([10, 20, 30, 40])

        result = calculate_median(values)

        self.assertEqual(result, 25.0)

    def test_var(self):
        values = np.array([0, 10, 20, 30, 40])

        result = calculate_var(
            values,
            0.80
        )

        self.assertEqual(result, 32.0)

    def test_tvar(self):
        values = np.array([0, 10, 20, 30, 40])

        result = calculate_tvar(
            values,
            0.80
        )

        self.assertEqual(result, 40.0)

    def test_attachment_probability(self):
        recoveries = np.array([
            0,
            100,
            0,
            200,
            300,
            0,
        ])

        result = calculate_attachment_probability(
            recoveries
        )

        self.assertEqual(
            result,
            3 / 6
        )

    def test_exhaustion_probability(self):
        exhausting_claims = np.array([
            0,
            1,
            0,
            2,
            0,
            0,
            3,
        ])

        result = calculate_exhaustion_probability(
            exhausting_claims
        )

        self.assertEqual(
            result,
            3 / 7
        )

    def test_average_attaching_claims(self):
        attaching_claims = np.array([
            0,
            2,
            0,
            4,
            1,
            0,
        ])

        recoveries = np.array([
            0,
            100,
            0,
            200,
            50,
            0,
        ])

        result = calculate_average_attaching_claims(
            attaching_claims,
            recoveries
        )

        # Only attaching years count:
        # (2 + 4 + 1) / 3 = 7 / 3
        self.assertAlmostEqual(
            result,
            7 / 3
        )

    def test_average_attaching_claims_no_attachment(self):
        attaching_claims = np.array([
            0,
            2,
            1,
            0,
        ])

        recoveries = np.array([
            0,
            0,
            0,
            0,
        ])

        result = calculate_average_attaching_claims(
            attaching_claims,
            recoveries
        )

        self.assertEqual(
            result,
            0.0
        )

    def test_treaty_utilization(self):
        recoveries = np.array([
            0,
            100,
            200,
            300,
        ])

        treaty_limit = 1000

        result = calculate_treaty_utilization(
            recoveries,
            treaty_limit
        )

        self.assertEqual(
            result,
            0.15
        )

    def test_treaty_utilization_invalid_limit(self):
        recoveries = np.array([
            100,
            200,
        ])

        with self.assertRaises(ValueError):
            calculate_treaty_utilization(
                recoveries,
                0
            )

    def test_var_invalid_confidence_level(self):
        values = np.array([
            10,
            20,
            30,
        ])

        with self.assertRaises(ValueError):
            calculate_var(
                values,
                1.0
            )

    def test_tvar_invalid_confidence_level(self):
        values = np.array([
            10,
            20,
            30,
        ])

        with self.assertRaises(ValueError):
            calculate_tvar(
                values,
                0.0
            )


if __name__ == "__main__":
    unittest.main()