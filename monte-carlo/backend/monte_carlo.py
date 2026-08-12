import numpy as np

from backend.analytics import analyze_simulation


# ============================================================
# EDINSURED TREATY LAB
# M3 + M4 — MONTE CARLO + ANALYTICS
# ============================================================


# ============================================================
# MONTE CARLO CONFIGURATION
# ============================================================

NUMBER_OF_SIMULATIONS = 10_000

# Portfolio assumptions
POLICIES = 10_000
CLAIM_FREQUENCY = 0.05
AVERAGE_CLAIM = 100_000

# Treaty: ₹5M xs ₹1M Per Risk XL
ATTACHMENT = 1_000_000
LIMIT = 5_000_000

# Lognormal severity parameter
SIGMA = 1.0


# ============================================================
# CORE SIMULATION FUNCTIONS
# ============================================================

def calculate_expected_claims(
    policies,
    claim_frequency
):
    """
    Calculate expected annual claim count.
    """

    return policies * claim_frequency


def simulate_claims(
    number_of_claims,
    average_claim
):
    """
    Generate individual claim severities using
    a Lognormal distribution.

    The mu adjustment keeps the expected
    severity approximately equal to average_claim.
    """

    if number_of_claims == 0:
        return np.array([])

    mu = (
        np.log(average_claim)
        - (SIGMA ** 2 / 2)
    )

    claims = np.random.lognormal(
        mean=mu,
        sigma=SIGMA,
        size=number_of_claims
    )

    return claims


def calculate_xl_recovery(
    gross_loss,
    attachment,
    limit
):
    """
    Calculate Per Risk XL recovery for
    one individual claim.
    """

    if gross_loss <= attachment:
        return 0

    return min(
        gross_loss - attachment,
        limit
    )


def simulate_one_year(
    expected_claims,
    average_claim,
    attachment,
    limit
):
    """
    Simulate one complete portfolio year.
    """

    # --------------------------------------------------------
    # CLAIM FREQUENCY
    # --------------------------------------------------------

    claim_count = np.random.poisson(
        expected_claims
    )

    # --------------------------------------------------------
    # CLAIM SEVERITY
    # --------------------------------------------------------

    claims = simulate_claims(
        claim_count,
        average_claim
    )

    # --------------------------------------------------------
    # GROSS LOSS
    # --------------------------------------------------------

    gross_loss = np.sum(claims)

    # --------------------------------------------------------
    # APPLY PER RISK XL
    # --------------------------------------------------------

    total_recovery = 0
    attaching_claims = 0
    exhausting_claims = 0

    exhaustion_threshold = (
        attachment + limit
    )

    for claim in claims:

        recovery = calculate_xl_recovery(
            claim,
            attachment,
            limit
        )

        total_recovery += recovery

        if recovery > 0:
            attaching_claims += 1

        if claim >= exhaustion_threshold:
            exhausting_claims += 1

    # --------------------------------------------------------
    # TREATY EXHAUSTION
    # --------------------------------------------------------

    treaty_exhausted = (
        exhausting_claims > 0
    )

    # --------------------------------------------------------
    # NET LOSS
    # --------------------------------------------------------

    net_loss = (
        gross_loss
        - total_recovery
    )

    return {
        "claim_count": int(claim_count),
        "gross_loss": float(gross_loss),
        "attaching_claims": int(attaching_claims),
        "exhausting_claims": int(exhausting_claims),
        "treaty_exhausted": bool(treaty_exhausted),
        "reinsurance_recovery": float(
            total_recovery
        ),
        "net_loss": float(net_loss)
    }


def run_monte_carlo(
    number_of_simulations,
    policies,
    claim_frequency,
    average_claim,
    attachment,
    limit
):
    """
    Run the Monte Carlo simulation.

    Returns a list containing one result
    dictionary for each simulated year.
    """

    expected_claims = calculate_expected_claims(
        policies,
        claim_frequency
    )

    results = []

    for year in range(
        1,
        number_of_simulations + 1
    ):

        year_result = simulate_one_year(
            expected_claims,
            average_claim,
            attachment,
            limit
        )

        year_result["year"] = year

        results.append(
            year_result
        )

    return results


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print(
        "EDINSURED TREATY LAB — "
        "MONTE CARLO + ANALYTICS"
    )
    print("=" * 60)

    # --------------------------------------------------------
    # CONFIGURATION
    # --------------------------------------------------------

    print()
    print("--- Simulation Configuration ---")

    print(
        "Number of Simulations:",
        NUMBER_OF_SIMULATIONS
    )

    print(
        "Policies:",
        POLICIES
    )

    print(
        "Claim Frequency:",
        CLAIM_FREQUENCY
    )

    print(
        "Average Claim: ₹{:,.0f}".format(
            AVERAGE_CLAIM
        )
    )

    # --------------------------------------------------------
    # TREATY
    # --------------------------------------------------------

    print()
    print("--- Treaty ---")

    print(
        "Structure: ₹5M xs ₹1M Per Risk XL"
    )

    print(
        "Attachment: ₹{:,.0f}".format(
            ATTACHMENT
        )
    )

    print(
        "Limit: ₹{:,.0f}".format(
            LIMIT
        )
    )

    # --------------------------------------------------------
    # THEORETICAL EXPECTATIONS
    # --------------------------------------------------------

    expected_claims = calculate_expected_claims(
        POLICIES,
        CLAIM_FREQUENCY
    )

    expected_annual_loss = (
        expected_claims
        * AVERAGE_CLAIM
    )

    print()
    print("--- Theoretical Expectations ---")

    print(
        "Expected Claims: {:.2f}".format(
            expected_claims
        )
    )

    print(
        "Expected Annual Gross Loss: "
        "₹{:,.2f}".format(
            expected_annual_loss
        )
    )

    # --------------------------------------------------------
    # RUN MONTE CARLO
    # --------------------------------------------------------

    results = run_monte_carlo(
        NUMBER_OF_SIMULATIONS,
        POLICIES,
        CLAIM_FREQUENCY,
        AVERAGE_CLAIM,
        ATTACHMENT,
        LIMIT
    )

    # --------------------------------------------------------
    # CONVERT RESULTS TO ARRAYS
    # --------------------------------------------------------

    claim_counts = np.array([
        result["claim_count"]
        for result in results
    ])

    gross_losses = np.array([
        result["gross_loss"]
        for result in results
    ])

    attaching_claims = np.array([
        result["attaching_claims"]
        for result in results
    ])

    exhausting_claims = np.array([
        result["exhausting_claims"]
        for result in results
    ])

    recoveries = np.array([
        result["reinsurance_recovery"]
        for result in results
    ])

    net_losses = np.array([
        result["net_loss"]
        for result in results
    ])

    # --------------------------------------------------------
    # M4 ANALYTICS
    # --------------------------------------------------------

    analytics = analyze_simulation(
        gross_losses,
        recoveries,
        net_losses,
        exhausting_claims
    )

    # ========================================================
    # RESULTS
    # ========================================================

    print()
    print("=" * 60)
    print("MONTE CARLO + ANALYTICS RESULTS")
    print("=" * 60)

    # --------------------------------------------------------
    # SIMULATION VALIDATION
    # --------------------------------------------------------

    print()
    print("--- Simulation Validation ---")

    print(
        "Average Simulated Claims: {:.2f}".format(
            np.mean(claim_counts)
        )
    )

    print(
        "Average Gross Loss: ₹{:,.2f}".format(
            np.mean(gross_losses)
        )
    )

    print(
        "Expected Gross Loss: ₹{:,.2f}".format(
            expected_annual_loss
        )
    )

    # --------------------------------------------------------
    # GROSS
    # --------------------------------------------------------

    gross = analytics["gross"]

    print()
    print("--- Gross Portfolio Loss ---")

    print(
        "Mean Gross Loss: ₹{:,.2f}".format(
            gross["mean"]
        )
    )

    print(
        "Median Gross Loss: ₹{:,.2f}".format(
            gross["median"]
        )
    )

    print(
        "Minimum Gross Loss: ₹{:,.2f}".format(
            gross["minimum"]
        )
    )

    print(
        "Maximum Gross Loss: ₹{:,.2f}".format(
            gross["maximum"]
        )
    )

    print(
        "Standard Deviation: ₹{:,.2f}".format(
            gross["standard_deviation"]
        )
    )

    # --------------------------------------------------------
    # REINSURANCE
    # --------------------------------------------------------

    reinsurance = analytics[
        "reinsurance"
    ]

    print()
    print("--- Reinsurance Results ---")

    print(
        "Mean Recovery: ₹{:,.2f}".format(
            reinsurance["mean_recovery"]
        )
    )

    print(
        "Median Recovery: ₹{:,.2f}".format(
            reinsurance["median_recovery"]
        )
    )

    print(
        "Maximum Annual Recovery: ₹{:,.2f}".format(
            np.max(recoveries)
        )
    )

    attaching_years = np.sum(
        recoveries > 0
    )

    print(
        "Attaching Years: {:,}".format(
            attaching_years
        )
    )

    print(
        "Probability of Attachment: {:.2%}".format(
            reinsurance[
                "attachment_probability"
            ]
        )
    )

    print(
        "Average Attaching Claims per Year: {:.2f}".format(
            np.mean(attaching_claims)
        )
    )

    print(
        "Exhausting Claims: {:,}".format(
            np.sum(exhausting_claims)
        )
    )

    exhausted_years = np.sum(
        exhausting_claims > 0
    )

    print(
        "Years with Layer Exhaustion: {:,}".format(
            exhausted_years
        )
    )

    print(
        "Probability of Layer Exhaustion "
        "in a Year: {:.2%}".format(
            reinsurance[
                "exhaustion_probability"
            ]
        )
    )

    # --------------------------------------------------------
    # NET
    # --------------------------------------------------------

    net = analytics["net"]

    print()
    print("--- Net Portfolio Loss ---")

    print(
        "Mean Net Loss: ₹{:,.2f}".format(
            net["mean"]
        )
    )

    print(
        "Median Net Loss: ₹{:,.2f}".format(
            net["median"]
        )
    )

    print(
        "Minimum Net Loss: ₹{:,.2f}".format(
            net["minimum"]
        )
    )

    print(
        "Maximum Net Loss: ₹{:,.2f}".format(
            net["maximum"]
        )
    )

    print(
        "Standard Deviation: ₹{:,.2f}".format(
            net["standard_deviation"]
        )
    )

    # --------------------------------------------------------
    # RISK ANALYTICS
    # --------------------------------------------------------

    print()
    print("--- Risk Analytics ---")

    print()
    print("Gross Loss:")

    print(
        "95% VaR: ₹{:,.2f}".format(
            gross["var_95"]
        )
    )

    print(
        "99% VaR: ₹{:,.2f}".format(
            gross["var_99"]
        )
    )

    print(
        "99.5% VaR: ₹{:,.2f}".format(
            gross["var_995"]
        )
    )

    print(
        "99% TVaR: ₹{:,.2f}".format(
            gross["tvar_99"]
        )
    )

    print()
    print("Reinsurance Recovery:")

    print(
        "95% VaR: ₹{:,.2f}".format(
            analytics["recovery"]["var_95"]
        )
    )

    print(
        "99% VaR: ₹{:,.2f}".format(
            analytics["recovery"]["var_99"]
        )
    )

    print(
        "99% TVaR: ₹{:,.2f}".format(
            analytics["recovery"]["tvar_99"]
        )
    )

    print()
    print("Net Loss:")

    print(
        "95% VaR: ₹{:,.2f}".format(
            net["var_95"]
        )
    )

    print(
        "99% VaR: ₹{:,.2f}".format(
            net["var_99"]
        )
    )

    print(
        "99.5% VaR: ₹{:,.2f}".format(
            net["var_995"]
        )
    )

    print(
        "99% TVaR: ₹{:,.2f}".format(
            net["tvar_99"]
        )
    )

    # ========================================================
    # FIRST 10 YEARS
    # ========================================================

    print()
    print("=" * 60)
    print("FIRST 10 SIMULATED YEARS")
    print("=" * 60)

    for result in results[:10]:

        print(
            "Year {year}: "
            "Claims = {claims}, "
            "Gross = ₹{gross:,.2f}, "
            "Attaching = {attaching}, "
            "Exhausting = {exhausting}, "
            "Recovery = ₹{recovery:,.2f}, "
            "Net = ₹{net:,.2f}".format(
                year=result["year"],
                claims=result["claim_count"],
                gross=result["gross_loss"],
                attaching=result["attaching_claims"],
                exhausting=result["exhausting_claims"],
                recovery=result[
                    "reinsurance_recovery"
                ],
                net=result["net_loss"]
            )
        )

    # ========================================================
    # COMPLETE
    # ========================================================

    print()
    print("=" * 60)
    print(
        "M3 MONTE CARLO + M4 ANALYTICS COMPLETE"
    )
    print("=" * 60)