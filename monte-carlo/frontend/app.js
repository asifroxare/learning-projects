const API_URL = "http://127.0.0.1:8000/simulate";

let chartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("simulation-form");
  form.addEventListener("submit", handleSimulationSubmit);
});

async function handleSimulationSubmit(event) {
  event.preventDefault();

  const runBtn = document.getElementById("run-btn");
  const btnText = document.getElementById("btn-text");
  const btnLoader = document.getElementById("btn-loader");
  const errorBanner = document.getElementById("error-banner");

  // Reset states
  errorBanner.classList.add("hidden");
  errorBanner.textContent = "";
  btnText.textContent = "Running...";
  btnLoader.classList.remove("hidden");
  runBtn.disabled = true;

  // Construct payload from input values
  const payload = {
    policies: Number(document.getElementById("policies").value),
    claim_frequency: Number(document.getElementById("claim_frequency").value),
    average_claim: Number(document.getElementById("average_claim").value),
    attachment: Number(document.getElementById("attachment").value),
    limit: Number(document.getElementById("limit").value),
    simulations: Number(document.getElementById("simulations").value)
  };

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    renderDashboard(data);
  } catch (error) {
    console.error("Simulation request failed:", error);
    errorBanner.textContent = `Error connecting to API (${error.message}). Ensure FastAPI server is running on http://127.0.0.1:8000.`;
    errorBanner.classList.remove("hidden");
  } finally {
    btnText.textContent = "Run Simulation";
    btnLoader.classList.add("hidden");
    runBtn.disabled = false;
  }
}

function renderDashboard(data) {
  const { configuration, theoretical, simulation, analytics, years } = data;

  // Format helpers
  const formatCurrency = (val) => val !== undefined && val !== null ? `$${Number(val).toLocaleString(undefined, { maximumFractionDigits: 0 })}` : '-';
  const formatNum = (val) => val !== undefined && val !== null ? Number(val).toLocaleString(undefined, { maximumFractionDigits: 2 }) : '-';
  const formatPct = (val) => val !== undefined && val !== null ? `${(Number(val) * 100).toFixed(2)}%` : '-';

  // 1. CARDS
  if (theoretical) {
    document.getElementById("card-expected-claims").textContent = formatNum(theoretical.expected_claims);
    document.getElementById("sub-claims-theoretical").textContent = `Theoretical: ${formatNum(theoretical.expected_claims)}`;
    document.getElementById("card-expected-loss").textContent = formatCurrency(theoretical.expected_annual_loss);
    document.getElementById("sub-loss-theoretical").textContent = `Theoretical: ${formatCurrency(theoretical.expected_annual_loss)}`;
  }

  if (simulation) {
    document.getElementById("card-average-claims").textContent = formatNum(simulation.average_claims);
    document.getElementById("card-attaching-years").textContent = formatNum(simulation.attaching_years);
    document.getElementById("card-attaching-pct").textContent = `Pct of Years: ${formatPct(simulation.pct_attaching_years || (simulation.attaching_years / configuration.simulations))}`;
    document.getElementById("card-avg-attaching-claims").textContent = formatNum(simulation.average_attaching_claims);
    document.getElementById("card-exhaustion-years").textContent = formatNum(simulation.layer_exhaustion_years);
    document.getElementById("card-exhaustion-pct").textContent = `Pct of Years: ${formatPct(simulation.pct_exhaustion_years || (simulation.layer_exhaustion_years / configuration.simulations))}`;
  }

  // 2. CONFIGURATION & TREATY STRUCTURE
  const configContainer = document.getElementById("config-summary");
  if (configuration) {
    configContainer.innerHTML = `
      <div class="config-grid">
        <div class="metric-box">
          <span class="metric-label">Policies</span>
          <div class="metric-val">${formatNum(configuration.policies)}</div>
        </div>
        <div class="metric-box">
          <span class="metric-label">Claim Frequency</span>
          <div class="metric-val">${configuration.claim_frequency}</div>
        </div>
        <div class="metric-box">
          <span class="metric-label">Average Claim</span>
          <div class="metric-val">${formatCurrency(configuration.average_claim)}</div>
        </div>
        <div class="metric-box">
          <span class="metric-label">Attachment Point</span>
          <div class="metric-val">${formatCurrency(configuration.attachment)}</div>
        </div>
        <div class="metric-box">
          <span class="metric-label">Layer Limit</span>
          <div class="metric-val">${formatCurrency(configuration.limit)}</div>
        </div>
        <div class="metric-box">
          <span class="metric-label">Simulated Years</span>
          <div class="metric-val">${formatNum(configuration.simulations)}</div>
        </div>
      </div>
    `;
  }

  // 3. ANALYTICS METRICS (Dynamically rendering whatever actual keys exist)
  const analyticsContainer = document.getElementById("analytics-container");
  if (analytics && Object.keys(analytics).length > 0) {
    analyticsContainer.innerHTML = Object.entries(analytics).map(([key, value]) => {
      const label = key.replace(/_/g, " ").toUpperCase();
      let formattedValue = value;
      if (typeof value === "number") {
        formattedValue = key.toLowerCase().includes("loss") || key.toLowerCase().includes("recovery") || key.toLowerCase().includes("claim")
          ? formatCurrency(value)
          : formatNum(value);
      }
      return `
        <div class="metric-box">
          <span class="metric-label">${label}</span>
          <div class="metric-val">${formattedValue}</div>
        </div>
      `;
    }).join("");
  } else {
    analyticsContainer.innerHTML = `<p class="placeholder-text">No additional analytics returned by API.</p>`;
  }

  // 4. YEARS TABLE
  const tableBody = document.getElementById("years-table-body");
  if (years && Array.isArray(years) && years.length > 0) {
    tableBody.innerHTML = years.map((yr, idx) => {
      // Flexibly map properties returned by API
      const yearNum = yr.year !== undefined ? yr.year : idx + 1;
      const claimCount = yr.claim_count ?? yr.claims ?? yr.num_claims ?? '-';
      const grossLoss = yr.gross_loss ?? yr.total_loss ?? yr.loss ?? null;
      const recovery = yr.reinsurance_recovery ?? yr.recovery ?? yr.xs_loss ?? null;
      const netLoss = yr.net_loss ?? (grossLoss !== null && recovery !== null ? grossLoss - recovery : null);
      const attaching = yr.attaching_claims ?? yr.attaching ?? '-';
      const exhausting = yr.exhausting_claims ?? yr.exhausting ?? '-';

      return `
        <tr>
          <td>${yearNum}</td>
          <td>${formatNum(claimCount)}</td>
          <td>${formatCurrency(grossLoss)}</td>
          <td>${formatCurrency(recovery)}</td>
          <td>${formatCurrency(netLoss)}</td>
          <td>${formatNum(attaching)}</td>
          <td>${formatNum(exhausting)}</td>
        </tr>
      `;
    }).join("");

    // Render chart using real years data
    renderChart(years);
  } else {
    tableBody.innerHTML = `<tr><td colspan="7" class="placeholder-text text-center">No years data available.</td></tr>`;
  }
}

function renderChart(yearsData) {
  const ctx = document.getElementById("lossChart").getContext("2d");

  const labels = yearsData.map((y, idx) => `Year ${y.year !== undefined ? y.year : idx + 1}`);
  const grossLosses = yearsData.map(y => y.gross_loss ?? y.total_loss ?? 0);
  const recoveries = yearsData.map(y => y.reinsurance_recovery ?? y.recovery ?? 0);

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Gross Loss ($)",
          data: grossLosses,
          backgroundColor: "#38bdf8",
          borderRadius: 2
        },
        {
          label: "Reinsurance Recovery ($)",
          data: recoveries,
          backgroundColor: "#10b981",
          borderRadius: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: { color: "#94a3b8", maxTicksLimit: 20 },
          grid: { display: false }
        },
        y: {
          ticks: { color: "#94a3b8" },
          grid: { color: "#334155" }
        }
      },
      plugins: {
        legend: {
          labels: { color: "#f8fafc" }
        }
      }
    }
  });
}