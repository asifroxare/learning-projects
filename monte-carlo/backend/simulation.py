import random
import numpy as np


# ============================================================
# PORTFOLIO INFORMATION
# ============================================================

policies = int(input("Number of Policies: "))
claim_frequency = float(input("Claim Frequency: "))
average_claim = float(input("Average Claim: "))


# ============================================================
# FUNCTIONS
# ============================================================

def calculate_expected_claims(policies, claim_frequency):
    expected_claims = policies * claim_frequency
    return expected_claims


def calculate_expected_loss(expected_claims, average_claim):
    expected_annual_loss = expected_claims * average_claim
    return expected_annual_loss


def simulate_claims(number_of_claims, average_claim):

    sigma = 1.0

    # Adjust mu so the expected severity remains
    # approximately equal to average_claim
    mu = np.log(average_claim) - (sigma ** 2 / 2)

    claims = np.random.lognormal(
        mean=mu,
        sigma=sigma,
        size=number_of_claims
    )

    return claims


def calculate_xl_recovery(gross_loss, attachment, limit):

    if gross_loss <= attachment:
        recovery = 0

    else:
        recovery = min(
            gross_loss - attachment,
            limit
        )

    return recovery


# ============================================================
# EXPECTED LOSS CALCULATIONS
# ============================================================

expected_claims = calculate_expected_claims(
    policies,
    claim_frequency
)

expected_annual_loss = calculate_expected_loss(
    expected_claims,
    average_claim
)


# ============================================================
# SIMULATE CLAIM FREQUENCY
# ============================================================

simulated_claim_count = np.random.poisson(
    expected_claims
)


# ============================================================
# SIMULATE CLAIM SEVERITY
# ============================================================

simulated_claims = simulate_claims(
    simulated_claim_count,
    average_claim
)


# ============================================================
# GROSS PORTFOLIO LOSS
# ============================================================

simulated_gross_loss = sum(simulated_claims)

largest_claim = max(simulated_claims)


# ============================================================
# XL TREATY PARAMETERS
# $5M xs $1M PER RISK XL
# ============================================================

attachment = 1_000_000
limit = 5_000_000


# ============================================================
# APPLY XL TO EACH INDIVIDUAL CLAIM
# ============================================================

total_reinsurance_recovery = 0
attaching_claims = 0

claim_recoveries = []

for claim in simulated_claims:

    recovery = calculate_xl_recovery(
        claim,
        attachment,
        limit
    )

    claim_recoveries.append(recovery)

    total_reinsurance_recovery += recovery

    if recovery > 0:
        attaching_claims += 1


# ============================================================
# NET PORTFOLIO LOSS
# ============================================================

net_loss = (
    simulated_gross_loss
    - total_reinsurance_recovery
)


# ============================================================
# TREATY UTILIZATION
# ============================================================

treaty_capacity = limit * attaching_claims

if treaty_capacity > 0:
    treaty_utilization = (
        total_reinsurance_recovery
        / treaty_capacity
    )
else:
    treaty_utilization = 0


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n--- Portfolio Information ---")

print("Policies:", policies)
print("Claim Frequency:", claim_frequency)
print("Average Claim:", average_claim)


print("\n--- Expected Results ---")

print("Expected Claims:", expected_claims)
print("Expected Annual Loss:", expected_annual_loss)


print("\n--- Simulated Year ---")

print("Simulated Claims:", simulated_claim_count)
print(
    "Simulated Gross Loss:",
    round(simulated_gross_loss, 2)
)

print(
    "Largest Claim:",
    round(largest_claim, 2)
)


print("\n--- XL Treaty ---")

print("Attachment:", attachment)
print("Limit:", limit)
print("Treaty Structure: 5M xs 1M Per Risk")


print("\n--- Reinsurance Results ---")

print(
    "Attaching Claims:",
    attaching_claims
)

print(
    "Total Reinsurance Recovery:",
    round(total_reinsurance_recovery, 2)
)

print(
    "Net Portfolio Loss:",
    round(net_loss, 2)
)

print(
    "Treaty Utilization:",
    round(treaty_utilization * 100, 2),
    "%"
)


# ============================================================
# FIRST 10 CLAIMS
# ============================================================

print("\n--- First 10 Simulated Claims ---")

for i, claim in enumerate(
    simulated_claims[:10],
    start=1
):

    recovery = claim_recoveries[i - 1]

    print(
        f"Claim {i}: "
        f"Gross = {round(claim, 2)}, "
        f"Recovery = {round(recovery, 2)}, "
        f"Net = {round(claim - recovery, 2)}"
    )