def calculate_xl_recovery(gross_loss, attachment, limit):

    if gross_loss <= attachment:
        recovery = 0
    else:
        recovery = min(
            gross_loss - attachment,
            limit
        )

    return recovery


# Treaty: ₹5M xs ₹1M
attachment = 1_000_000
limit = 5_000_000


# Test claims
test_claims = [
    500_000,
    1_000_000,
    1_500_000,
    3_000_000,
    6_000_000,
    8_000_000
]


print("--- XL Treaty Validation ---")

for claim in test_claims:

    recovery = calculate_xl_recovery(
        claim,
        attachment,
        limit
    )

    net_loss = claim - recovery

    print(
        f"Gross Claim: ₹{claim:,.0f} | "
        f"Recovery: ₹{recovery:,.0f} | "
        f"Net Loss: ₹{net_loss:,.0f}"
    )