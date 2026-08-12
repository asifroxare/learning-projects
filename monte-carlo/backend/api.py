from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.monte_carlo import run_monte_carlo
from backend.analytics import analyze_simulation


# ============================================================
# EDINSURED TREATY LAB
# M5 — RESULTS API
# ============================================================

app = FastAPI(
    title="EdInsured Treaty Lab",
    description="Monte Carlo Reinsurance Simulator API",
    version="0.1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class SimulationRequest(BaseModel):

    policies: int = Field(
        default=10_000,
        gt=0
    )

    claim_frequency: float = Field(
        default=0.05,
        gt=0,
        le=1
    )

    average_claim: float = Field(
        default=100_000,
        gt=0
    )

    attachment: float = Field(
        default=1_000_000,
        gt=0
    )

    limit: float = Field(
        default=5_000_000,
        gt=0
    )

    simulations: int = Field(
        default=10_000,
        gt=0,
        le=1_000_000
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():

    return {
        "application": "EdInsured Treaty Lab",
        "status": "online",
        "version": "0.1.0"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# SIMULATION ENDPOINT
# ============================================================

@app.post("/simulate")
def simulate(
    request: SimulationRequest
):

    # --------------------------------------------------------
    # RUN MONTE CARLO
    # --------------------------------------------------------

    results = run_monte_carlo(
        number_of_simulations=request.simulations,
        policies=request.policies,
        claim_frequency=request.claim_frequency,
        average_claim=request.average_claim,
        attachment=request.attachment,
        limit=request.limit
    )

    # --------------------------------------------------------
    # EXTRACT ARRAYS
    # --------------------------------------------------------

    import numpy as np

    claim_counts = np.array([
        result["claim_count"]
        for result in results
    ])

    gross_losses = np.array([
        result["gross_loss"]
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

    exhausting_claims = np.array([
        result["exhausting_claims"]
        for result in results
    ])

    attaching_claims = np.array([
        result["attaching_claims"]
        for result in results
    ])

    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    analytics = analyze_simulation(
        gross_losses,
        recoveries,
        net_losses,
        exhausting_claims
    )

    # --------------------------------------------------------
    # ADDITIONAL SIMULATION INFORMATION
    # --------------------------------------------------------

    expected_claims = (
        request.policies
        * request.claim_frequency
    )

    expected_annual_loss = (
        expected_claims
        * request.average_claim
    )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "configuration": {
            "simulations": request.simulations,
            "policies": request.policies,
            "claim_frequency":
                request.claim_frequency,
            "average_claim":
                request.average_claim,
            "attachment":
                request.attachment,
            "limit":
                request.limit,
            "treaty_structure":
                f"{request.limit:,.0f} xs "
                f"{request.attachment:,.0f} "
                "Per Risk XL"
        },

        "theoretical": {
            "expected_claims":
                expected_claims,
            "expected_annual_loss":
                expected_annual_loss
        },

        "simulation": {
            "average_claims":
                float(np.mean(claim_counts)),
            "attaching_years":
                int(np.sum(recoveries > 0)),
            "average_attaching_claims":
                float(np.mean(attaching_claims)),
            "exhausting_claims":
                int(np.sum(exhausting_claims)),
            "layer_exhaustion_years":
                int(np.sum(
                    exhausting_claims > 0
                ))
        },

        "analytics": analytics,

        "years": results[:100]
    }