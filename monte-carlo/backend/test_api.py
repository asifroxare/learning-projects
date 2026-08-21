import unittest

from fastapi.testclient import TestClient

from backend.api import app


client = TestClient(app)


class TestAPI(unittest.TestCase):

    # ========================================================
    # ROOT ENDPOINT
    # ========================================================

    def test_root(self):
        response = client.get("/")

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.json()

        self.assertEqual(
            data["application"],
            "EdInsured Treaty Lab"
        )

        self.assertEqual(
            data["status"],
            "online"
        )

        self.assertEqual(
            data["version"],
            "0.1.0"
        )

    # ========================================================
    # HEALTH ENDPOINT
    # ========================================================

    def test_health(self):
        response = client.get("/health")

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.json()["status"],
            "healthy"
        )

    # ========================================================
    # SIMULATION ENDPOINT
    # ========================================================

    def test_simulate(self):
        response = client.post(
            "/simulate",
            json={
                "policies": 1000,
                "claim_frequency": 0.05,
                "average_claim": 100000,
                "attachment": 1000000,
                "limit": 5000000,
                "simulations": 100
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.json()

        # ----------------------------------------------------
        # Top-level response structure
        # ----------------------------------------------------

        self.assertIn(
            "configuration",
            data
        )

        self.assertIn(
            "theoretical",
            data
        )

        self.assertIn(
            "simulation",
            data
        )

        self.assertIn(
            "analytics",
            data
        )

        self.assertIn(
            "years",
            data
        )

        # ----------------------------------------------------
        # Configuration
        # ----------------------------------------------------

        configuration = data[
            "configuration"
        ]

        self.assertEqual(
            configuration["policies"],
            1000
        )

        self.assertEqual(
            configuration["claim_frequency"],
            0.05
        )

        self.assertEqual(
            configuration["average_claim"],
            100000
        )

        self.assertEqual(
            configuration["attachment"],
            1000000
        )

        self.assertEqual(
            configuration["limit"],
            5000000
        )

        self.assertEqual(
            configuration["simulations"],
            100
        )

        # ----------------------------------------------------
        # Theoretical values
        # ----------------------------------------------------

        theoretical = data[
            "theoretical"
        ]

        self.assertEqual(
            theoretical["expected_claims"],
            50.0
        )

        self.assertEqual(
            theoretical["expected_annual_loss"],
            5_000_000.0
        )

        # ----------------------------------------------------
        # Simulation section
        # ----------------------------------------------------

        simulation = data[
            "simulation"
        ]

        self.assertIn(
            "average_claims",
            simulation
        )

        self.assertIn(
            "attaching_years",
            simulation
        )

        self.assertIn(
            "average_attaching_claims",
            simulation
        )

        self.assertIn(
            "exhausting_claims",
            simulation
        )

        self.assertIn(
            "layer_exhaustion_years",
            simulation
        )

        self.assertGreaterEqual(
            simulation["average_claims"],
            0
        )

        self.assertGreaterEqual(
            simulation["attaching_years"],
            0
        )

        self.assertGreaterEqual(
            simulation["average_attaching_claims"],
            0
        )

        # ----------------------------------------------------
        # M4 Analytics
        # ----------------------------------------------------

        analytics = data[
            "analytics"
        ]

        self.assertIn(
            "gross",
            analytics
        )

        self.assertIn(
            "recovery",
            analytics
        )

        self.assertIn(
            "net",
            analytics
        )

        self.assertIn(
            "reinsurance",
            analytics
        )

        reinsurance = analytics[
            "reinsurance"
        ]

        self.assertIn(
            "mean_recovery",
            reinsurance
        )

        self.assertIn(
            "attachment_probability",
            reinsurance
        )

        self.assertIn(
            "average_attaching_claims",
            reinsurance
        )

        self.assertIn(
            "treaty_utilization",
            reinsurance
        )

        self.assertIn(
            "exhaustion_probability",
            reinsurance
        )

        # ----------------------------------------------------
        # Verify API and M4 use the same value
        # ----------------------------------------------------

        self.assertEqual(
            simulation[
                "average_attaching_claims"
            ],
            reinsurance[
                "average_attaching_claims"
            ]
        )

        # ----------------------------------------------------
        # Simulation years
        # ----------------------------------------------------

        years = data[
            "years"
        ]

        self.assertLessEqual(
            len(years),
            100
        )

        self.assertGreater(
            len(years),
            0
        )

        first_year = years[0]

        self.assertIn(
            "claim_count",
            first_year
        )

        self.assertIn(
            "gross_loss",
            first_year
        )

        self.assertIn(
            "reinsurance_recovery",
            first_year
        )

        self.assertIn(
            "net_loss",
            first_year
        )

    # ========================================================
    # VALIDATION — POLICIES
    # ========================================================

    def test_invalid_policies(self):
        response = client.post(
            "/simulate",
            json={
                "policies": 0
            }
        )

        self.assertEqual(
            response.status_code,
            422
        )

    # ========================================================
    # VALIDATION — CLAIM FREQUENCY
    # ========================================================

    def test_invalid_claim_frequency(self):
        response = client.post(
            "/simulate",
            json={
                "claim_frequency": 1.5
            }
        )

        self.assertEqual(
            response.status_code,
            422
        )

    # ========================================================
    # VALIDATION — AVERAGE CLAIM
    # ========================================================

    def test_invalid_average_claim(self):
        response = client.post(
            "/simulate",
            json={
                "average_claim": 0
            }
        )

        self.assertEqual(
            response.status_code,
            422
        )

    # ========================================================
    # VALIDATION — ATTACHMENT
    # ========================================================

    def test_invalid_attachment(self):
        response = client.post(
            "/simulate",
            json={
                "attachment": 0
            }
        )

        self.assertEqual(
            response.status_code,
            422
        )

    # ========================================================
    # VALIDATION — LIMIT
    # ========================================================

    def test_invalid_limit(self):
        response = client.post(
            "/simulate",
            json={
                "limit": 0
            }
        )

        self.assertEqual(
            response.status_code,
            422
        )

    # ========================================================
    # VALIDATION — SIMULATIONS
    # ========================================================

    def test_invalid_simulations(self):
        response = client.post(
            "/simulate",
            json={
                "simulations": 0
            }
        )

        self.assertEqual(
            response.status_code,
            422
        )

    # ========================================================
    # VALIDATION — MAXIMUM SIMULATIONS
    # ========================================================

    def test_too_many_simulations(self):
        response = client.post(
            "/simulate",
            json={
                "simulations": 1_000_001
            }
        )

        self.assertEqual(
            response.status_code,
            422
        )


if __name__ == "__main__":
    unittest.main()