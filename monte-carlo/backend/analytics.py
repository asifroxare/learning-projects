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

    if not 0 < confidence_level < 1:
        raise ValueError(
            "confidence_level must be between 0 and 1."
        )

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

    if not 0 < confidence_level < 1:
        raise ValueError(
            "confidence_level must be between 0 and 1."
        )

    values = np.asarray(values)

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

    A year attaches when recovery > 0.
    """

    recoveries = np.asarray(
        recoveries
    )

    if len(recoveries) == 0:
        return 0.0

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

    exhausting_claims contains the number
    of exhausting claims for each year.
    """

    exhausting_claims = np.asarray(
        exhausting_claims
    )

    if len(exhausting_claims) == 0:
        return 0.0

    exhausted_years = np.sum(
        exhausting_claims > 0
    )

    return float(
        exhausted_years
        / len(exhausting_claims)
    )


def calculate_average_attaching_claims(
    attaching_claims,
    recoveries
):
    """
    Calculate the average number of attaching
    claims in years where the treaty actually
    attaches.

    A year is considered attaching when:

        recovery > 0

    Example:

        attaching_claims = [0, 2, 0, 4, 1, 0]
        recoveries       = [0, 100, 0, 200, 50, 0]

        Attaching years:
            2 claims
            4 claims
            1 claim

        Average:
            (2 + 4 + 1) / 3
            = 2.3333
    """

    attaching_claims = np.asarray(
        attaching_claims
    )

    recoveries = np.asarray(
        recoveries
    )

    if len(attaching_claims) != len(recoveries):
        raise ValueError(
            "attaching_claims and recoveries "
            "must have the same length."
        )

    if len(attaching_claims) == 0:
        return 0.0

    attaching_years = recoveries > 0

    if not np.any(attaching_years):
        return 0.0

    return float(
        np.mean(
            attaching_claims[
                attaching_years
            ]
        )
    )


def calculate_treaty_utilization(
    recoveries,
    limit
):
    """
    Calculate average annual treaty utilization.

    Treaty utilization is:

        average recovery / treaty limit

    Example:

        Average recovery = 150,000
        Treaty limit     = 1,000,000

        Utilization = 15%
    """

    if limit <= 0:
        raise ValueError(
            "Treaty limit must be greater than zero."
        )

    recoveries = np.asarray(
        recoveries
    )

    return float(
        np.mean(recoveries)
        / limit
    )


def calculate_summary_statistics(values):
    """
    Return the core descriptive statistics
    for a simulated loss distribution.
    """

    return {
        "mean":
            calculate_mean(values),

        "median":
            calculate_median(values),

        "minimum":
            calculate_minimum(values),

        "maximum":
            calculate_maximum(values),

        "standard_deviation":
            calculate_standard_deviation(values),

        "var_95":
            calculate_var(
                values,
                0.95
            ),

        "tvar_95":
            calculate_tvar(
                values,
                0.95
            ),

        "var_99":
            calculate_var(
                values,
                0.99
            ),

        "tvar_99":
            calculate_tvar(
                values,
                0.99
            ),

        "var_995":
            calculate_var(
                values,
                0.995
            ),
    }


def analyze_simulation(
    gross_losses,
    recoveries,
    net_losses,
    exhausting_claims,
    attaching_claims,
    treaty_limit
):
    """
    Produce the complete M4 analytics package
    from Monte Carlo simulation results.
    """

    return {
        "gross":
            calculate_summary_statistics(
                gross_losses
            ),

        "recovery":
            calculate_summary_statistics(
                recoveries
            ),

        "net":
            calculate_summary_statistics(
                net_losses
            ),

        "reinsurance": {

            "mean_recovery":
                calculate_mean(
                    recoveries
                ),

            "median_recovery":
                calculate_median(
                    recoveries
                ),

            "maximum_recovery":
                calculate_maximum(
                    recoveries
                ),

            "attachment_probability":
                calculate_attachment_probability(
                    recoveries
                ),

            "attaching_years":
                int(
                    np.sum(
                        np.asarray(
                            recoveries
                        ) > 0
                    )
                ),

            "average_attaching_claims":
                calculate_average_attaching_claims(
                    attaching_claims,
                    recoveries
                ),

            "treaty_utilization":
                calculate_treaty_utilization(
                    recoveries,
                    treaty_limit
                ),

            "exhaustion_probability":
                calculate_exhaustion_probability(
                    exhausting_claims
                ),
        }
    }