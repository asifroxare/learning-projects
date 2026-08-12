import numpy as np


# ============================================================
# EDINSURED TREATY LAB
# M4 — ANALYTICS ENGINE
# ============================================================


def calculate_mean(values):
    """
    Calculate the arithmetic mean.
    """
    return float(np.mean(values))


def calculate_median(values):
    """
    Calculate the median.
    """
    return float(np.median(values))


def calculate_minimum(values):
    """
    Calculate the minimum value.
    """
    return float(np.min(values))


def calculate_maximum(values):
    """
    Calculate the maximum value.
    """
    return float(np.max(values))


def calculate_standard_deviation(values):
    """
    Calculate standard deviation.
    """
    return float(np.std(values))


def calculate_percentile(values, percentile):
    """
    Calculate a percentile.

    Example:
        percentile = 95
        returns the 95th percentile.
    """
    return float(
        np.percentile(
            values,
            percentile
        )
    )


def calculate_var(values, confidence_level):
    """
    Calculate Value at Risk.

    Example:
        confidence_level = 0.99

        returns the 99% VaR.
    """

    return calculate_percentile(
        values,
        confidence_level * 100
    )


def calculate_tvar(values, confidence_level):
    """
    Calculate Tail Value at Risk.

    TVaR is the average loss at or above
    the selected VaR threshold.
    """

    var = calculate_var(
        values,
        confidence_level
    )

    tail_values = values[
        values >= var
    ]

    if len(tail_values) == 0:
        return var

    return float(
        np.mean(tail_values)
    )


def calculate_attachment_probability(
    recoveries
):
    """
    Probability that the reinsurance layer
    attaches in a simulated year.
    """

    attaching_years = np.sum(
        recoveries > 0
    )

    return float(
        attaching_years
        / len(recoveries)
    )


def calculate_exhaustion_probability(
    exhausting_claims
):
    """
    Probability that at least one claim
    exhausts the layer during a simulated year.

    exhausting_claims should contain the
    number of exhausting claims for each year.
    """

    exhausted_years = np.sum(
        exhausting_claims > 0
    )

    return float(
        exhausted_years
        / len(exhausting_claims)
    )


def calculate_summary_statistics(values):
    """
    Return the core descriptive statistics
    for a simulated loss distribution.
    """

    return {
        "mean": calculate_mean(values),
        "median": calculate_median(values),
        "minimum": calculate_minimum(values),
        "maximum": calculate_maximum(values),
        "standard_deviation":
            calculate_standard_deviation(values),
        "var_95":
            calculate_var(values, 0.95),
        "var_99":
            calculate_var(values, 0.99),
        "var_995":
            calculate_var(values, 0.995),
        "tvar_99":
            calculate_tvar(values, 0.99)
    }


def analyze_simulation(
    gross_losses,
    recoveries,
    net_losses,
    exhausting_claims
):
    """
    Produce the main M4 analytics package
    from Monte Carlo simulation results.
    """

    return {
        "gross": calculate_summary_statistics(
            gross_losses
        ),

        "recovery": calculate_summary_statistics(
            recoveries
        ),

        "net": calculate_summary_statistics(
            net_losses
        ),

        "reinsurance": {
            "mean_recovery":
                calculate_mean(recoveries),

            "median_recovery":
                calculate_median(recoveries),

            "attachment_probability":
                calculate_attachment_probability(
                    recoveries
                ),

            "exhaustion_probability":
                calculate_exhaustion_probability(
                    exhausting_claims
                )
        }
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("EDINSURED TREATY LAB — ANALYTICS TEST")
    print("=" * 60)

    # Small artificial dataset for testing
    test_losses = np.array([
        10_000_000,
        20_000_000,
        30_000_000,
        40_000_000,
        50_000_000
    ])

    test_recoveries = np.array([
        0,
        500_000,
        1_000_000,
        2_000_000,
        5_000_000
    ])

    test_net_losses = (
        test_losses
        - test_recoveries
    )

    test_exhausting_claims = np.array([
        0,
        0,
        1,
        0,
        2
    ])

    results = analyze_simulation(
        test_losses,
        test_recoveries,
        test_net_losses,
        test_exhausting_claims
    )

    print()
    print("--- Gross Loss ---")

    print(
        "Mean: ₹{:,.2f}".format(
            results["gross"]["mean"]
        )
    )

    print(
        "Median: ₹{:,.2f}".format(
            results["gross"]["median"]
        )
    )

    print(
        "95% VaR: ₹{:,.2f}".format(
            results["gross"]["var_95"]
        )
    )

    print(
        "99% VaR: ₹{:,.2f}".format(
            results["gross"]["var_99"]
        )
    )

    print(
        "99% TVaR: ₹{:,.2f}".format(
            results["gross"]["tvar_99"]
        )
    )

    print()
    print("--- Reinsurance ---")

    print(
        "Mean Recovery: ₹{:,.2f}".format(
            results["reinsurance"]["mean_recovery"]
        )
    )

    print(
        "Attachment Probability: {:.2%}".format(
            results["reinsurance"]
            ["attachment_probability"]
        )
    )

    print(
        "Exhaustion Probability: {:.2%}".format(
            results["reinsurance"]
            ["exhaustion_probability"]
        )
    )

    print()
    print("--- Net Loss ---")

    print(
        "Mean: ₹{:,.2f}".format(
            results["net"]["mean"]
        )
    )

    print(
        "95% VaR: ₹{:,.2f}".format(
            results["net"]["var_95"]
        )
    )

    print(
        "99% VaR: ₹{:,.2f}".format(
            results["net"]["var_99"]
        )
    )

    print(
        "99.5% VaR: ₹{:,.2f}".format(
            results["net"]["var_995"]
        )
    )

    print(
        "99% TVaR: ₹{:,.2f}".format(
            results["net"]["tvar_99"]
        )
    )

    print()
    print("=" * 60)
    print("ANALYTICS TEST COMPLETE")
    print("=" * 60)