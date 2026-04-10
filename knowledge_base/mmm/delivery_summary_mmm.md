# MMM Delivery Summary

> **Instructions for mmm-communicator:** Fill this template by translating technical model outputs into a client-ready narrative. Each section has an instruction comment (HTML comment style). Remove instructions before delivering to the client. Use plain language — no PyMC jargon.

**Project:** <!-- project code -->
**Prepared by:** <!-- analyst name -->
**Date:** <!-- YYYY-MM-DD -->
**Model version:** <!-- v1.0 -->

---

## Executive Summary

<!-- 3–4 sentences max. Answer: (1) What did we measure? (2) What is the headline ROAS finding? (3) What is the #1 budget recommendation? Quantify everything — avoid vague statements like "significant impact". -->

> [FILL: e.g., "We modelled [Brand]'s weekly [KPI] across [N] paid media channels from [date] to [date]. Paid Search delivers the highest incremental return at [X.Xx per $1 spent], while [Channel] is currently operating in the saturation zone. Reallocating [X]% of [Channel]'s budget to [Channel] is projected to lift [KPI] by [X]% with high confidence."]

---

## 1. What We Measured

- **Target KPI:** <!-- e.g., Net Revenue / Orders / Pipeline Value -->
- **Period:** <!-- YYYY-MM-DD to YYYY-MM-DD -->
- **Channels modelled:** <!-- list -->
- **Channels excluded and why:** <!-- or "None" -->
- **Calibration used:** <!-- list channels with experiment data, or "No experiments — model-estimated only" -->

---

## 2. Key Findings

### 2.1 Channel ROAS

<!-- Report iROAS (incremental, not blended). Always include the HDI. Avoid presenting a single number without range. -->

| Channel | iROAS | 90% Credible Interval | Calibrated? | Interpretation |
|---|---|---|---|---|
| <!-- Paid Search --> | <!-- 3.2x --> | <!-- [2.5x – 4.1x] --> | <!-- Yes / No --> | <!-- e.g., "High confidence; well above break-even of 1.0x" --> |
| | | | | |
| | | | | |

**Break-even ROAS:** <!-- 1.0x for revenue targets; [X.Xx] if cost-margin adjusted -->

### 2.2 Contribution to Revenue

<!-- Pie or bar chart summary. State as % of total modelled revenue. -->

| Component | % of Revenue | Absolute ($) |
|---|---|---|
| Paid media (all channels) | <!-- e.g., 35% --> | |
| Baseline (organic, seasonality, trend) | <!-- e.g., 58% --> | |
| Promotions / events | <!-- e.g., 7% --> | |

**Baseline check:** <!-- Confirm baseline is 30–70% of revenue. If outside range, add a brief note. -->

### 2.3 Seasonal Patterns

<!-- One sentence on the main seasonal finding. -->
> [FILL: e.g., "Revenue peaks in Q4 (weeks 45–52), driven by [seasonality pattern], independent of media spend changes."]

---

## 3. Budget Recommendations

<!-- Lead with the recommendation, then support with evidence from the model. Avoid presenting optimization as "the answer" — frame as a scenario. -->

### 3.1 Current vs. Recommended Allocation

| Channel | Current Spend | Recommended Spend | Change | Expected KPI Lift |
|---|---|---|---|---|
| | $<!-- X --> | $<!-- X --> | <!-- +X% / -X% --> | <!-- + $X [90% HDI: $X – $X] --> |
| | | | | |
| **Total** | $<!-- X --> | $<!-- X --> | 0% | <!-- +X% [HDI] --> |

**Note:** Recommendations are capped at [1.5× / 2×] observed spend per channel to avoid unreliable extrapolation beyond the data.

### 3.2 Marginal Returns at Current Spend

<!-- Show where each channel sits on the response curve — which are over-invested and which are under-invested. -->

| Channel | Current Marginal ROAS | Optimal Marginal ROAS | Status |
|---|---|---|---|
| | | | <!-- Over-invested / Under-invested / Near-optimal --> |

---

## 4. Key Caveats & Limitations

<!-- Do NOT omit this section. Clients trust analyses that acknowledge limitations. -->

- **Model confidence:** <!-- Overall model quality — in-sample MAPE X%, holdout MAPE Y%. -->
- **Uncalibrated channels:** <!-- List channels with no experiment data. ROAS for these channels is model-estimated and carries wider uncertainty. -->
- **Saturation assumption:** <!-- If any channel used NoSaturation, note this and explain that marginal ROAS may be overstated if spend increases significantly. -->
- **Data period:** <!-- Note if the period includes COVID or other anomalies and how they were handled. -->
- **Extrapolation limit:** <!-- Budget optimization is valid within ±X% of observed spend range. -->
- **Other:** <!-- Any project-specific limitation. -->

---

## 5. Recommended Next Steps

<!-- 3–5 specific, actionable items. Not vague. -->

1. <!-- e.g., "Run a geo-lift experiment for [Channel] in Q3 to calibrate the model's TV ROAS estimate (currently model-estimated at 1.8x [0.9x–2.8x])" -->
2. <!-- e.g., "Test the +15% budget shift to Paid Search for 8 weeks and compare to model prediction" -->
3. <!-- e.g., "Refit the model with Q2 2025 data before next planning cycle (current data ends [date])" -->
4. <!-- e.g., "Investigate the high seasonal baseline in [market] — potential missed promo flag" -->

---

## 6. Methodology Note (optional — include if client requests)

<!-- One short paragraph for clients who want to understand the approach without needing to read the technical report. -->

> This analysis used a Bayesian Marketing Mix Model — a statistical method that estimates the causal contribution of each marketing channel to [KPI], while accounting for organic trends, seasonality, and promotional effects. We used Bayesian inference to quantify uncertainty: every ROAS estimate comes with a credible interval reflecting the range of plausible values given the data. Where geo-lift experiments were available, we incorporated those findings to anchor the model's estimates.

---

## Appendix: Validation Summary (internal)

<!-- Include for internal review; may be removed from client-facing version -->

| Gate | Result | Notes |
|---|---|---|
| R-hat (max) | <!-- X.XXX --> | |
| Divergences | <!-- N --> | |
| In-sample MAPE | <!-- X% --> | |
| Holdout MAPE | <!-- X% --> | |
| Calibration check | <!-- PASS / FAIL --> | |
| Contribution sum-to-total | <!-- PASS / FAIL --> | |
| Overall validation | <!-- PASS / CONDITIONAL / FAIL --> | |
