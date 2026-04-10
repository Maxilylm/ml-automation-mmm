---
id: TREND_001
title: Linear trend control — when to include and how to configure
source: e-commerce-demo runs 2026-03-25/26 — confirmed pattern
category: priors_constraints
tags: [trend, collinearity, controls, secular_growth, identification, attribution, baseline]
---

## When to include a linear trend

Include a normalised linear trend `t ∈ [0, 1]` as a control variable when **all three** hold:

1. Dataset spans > 2 years
2. Revenue has a visible growth or decline trajectory over the period (CV driven partly by trend, not only seasonality)
3. At least one channel spend correlates with time (Pearson r > 0.5)

If revenue is stationary, trend is optional — Fourier terms + intercept are sufficient.

**Note**: Fourier terms and trend are complementary, not redundant. Fourier captures repeating seasonal cycles (net-zero over a full year). Trend captures non-repeating directional drift. Both are needed when data is both seasonal and trending.

---

## Implementation

```python
# Normalise over the full dataset (train + holdout) before splitting,
# so the [0,1] range is consistent across both sets.
n_weeks = len(grp_w)
grp_w["trend"] = np.arange(n_weeks) / (n_weeks - 1)   # [0, 1]

# Add to controls
control_cols = [..., "trend"]

# Prior: tight Normal(0, 0.05) — allows slow secular drift,
# prevents absorbing channel variation
PRIOR_GAMMA_CTRL_SIGMAS["trend"] = 0.05
```

The prior `Normal(0, 0.05)` keeps the trend coefficient small relative to the [0,1] max-scaled
target. On a target with `y_scaled_mean ≈ 0.14`, σ=0.05 allows roughly ±35% of the mean as
trend contribution — enough to capture multi-year growth without dominating channel effects.

---

## Never remove trend to fix collinearity

Removing a trend control because it correlates with a channel spend variable is a misdiagnosis:

- **Symptom**: R-hat failures or high divergences when trend is included
- **Wrong fix**: remove trend → channel absorbs secular growth → inflated ROAS, deflated baseline
- **Right fix**: use tight prior `Normal(0, 0.05)` on the trend coefficient

Collinearity between trend and spend is expected and normal in growing businesses. The tight
prior regularises the trend contribution without eliminating it.

**Confirmed**: removing trend was the root cause of Shopping ROAS=33× and baseline=17% in
the e-commerce-demo. The R-hat failures that motivated its removal were caused by the
`target_scale=1` bug (see MODEL_003), not by the trend itself.

---

## Negative trend coefficient — identification warning

If the posterior trend coefficient is **negative** despite visible revenue growth, this indicates
a collinearity identification problem:

- The model assigns all upward revenue trajectory to the correlated channel (e.g. Shopping)
- After conditioning on that channel, the "residual" trend is slightly negative
- Tightening the prior further will not resolve this

**This is not a modelling error — it is a signal that attribution is unreliable for the
correlated channel.** The only reliable fix is lift test calibration (see CAL_001) to anchor
that channel's ROAS to an experimentally-measured value.

Observed pattern (e-commerce-demo, run_20260326):
- trend γ = −0.075 (HDI: −0.139 to −0.011)
- Shopping ROAS = 38× (implausible)
- Holdout MAPE = 6.3% (prediction is good despite wrong attribution)

---

## Diagnostic checklist after adding trend

| Check | Expected | Action if wrong |
|---|---|---|
| Trend γ > 0 | Revenue growth → positive trend | If negative: collinearity; add lift test |
| Baseline % in 30–70% | Organic baseline plausible | If still low: channel absorbing trend → calibrate |
| Holdout MAPE | Should improve or hold | If worsens: trend overfitting; reduce σ to 0.03 |
| R-hat for trend | < 1.01 | If high: prior too loose or true collinearity → tighten to σ=0.03 |
