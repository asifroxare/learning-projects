import random
random_number = random.random()
print(random_number)
random_claims = random.randint(450, 550)
print("Simulated Claims:", random_claims)
# Portfolio Information
policies = int(input("Number of Policies: "))
claim_frequency = float(input("Claim Frequency: "))
average_claim = float(input("Average Claim: "))


# Functions

def calculate_expected_claims(policies, claim_frequency):
    expected_claims = policies * claim_frequency
    return expected_claims


def calculate_expected_loss(expected_claims, average_claim):
    expected_annual_loss = expected_claims * average_claim
    return expected_annual_loss


# Calculations

expected_claims = calculate_expected_claims(
    policies,
    claim_frequency
)

expected_annual_loss = calculate_expected_loss(
    expected_claims,
    average_claim
)


# Display Results

print("Policies:", policies)
print("Claim Frequency:", claim_frequency)
print("Average Claim:", average_claim)
print("Expected Claims:", expected_claims)
print("Expected Annual Loss:", expected_annual_loss)