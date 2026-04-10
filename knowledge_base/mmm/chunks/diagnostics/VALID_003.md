---
id: VALID_003
title: Contribution sanity checks — sum-to-total and plausibility
source: b2b_src/contributions.py
category: validation
tags: [contributions, sanity_check, sum_to_total, baseline, attribution, validation]
---

After computing contributions, run these sanity checks before reporting.

**Sum-to-total check (mandatory):**
```python
contribs = get_individual_contributions(mmm, df, channel_cols, control_cols)

total_channels = sum(contribs['channels'][ch].mean("sample") for ch in channel_cols)
total_controls = sum(contribs['controls'][ctrl].mean("sample") for ctrl in control_cols)
total_intercept = contribs['intercept'].mean("sample")
total_seasonal = contribs['seasonality'].mean("sample")

reconstructed = total_channels + total_controls + total_intercept + total_seasonal
observed = df["y"].values
gap = np.abs(reconstructed - observed).max() / observed.mean()
assert gap < 0.01, f"Contribution sum mismatch: {gap:.1%} > 1%"
```

**Plausibility thresholds:**
| Component | Expected range | Flag if outside |
|---|---|---|
| Baseline (intercept + seasonality) | 30–70% of revenue | < 25%: check attribution; > 80%: check channel variation |
| Any single channel | 0–50% of revenue | > 50%: suspicious unless documented dominant channel |
| All contributions | ≥ 0 | Any negative = model error |

**Debug negative contributions:** In a multiplicative model, channel contributions should always be ≥ 0. A negative contribution indicates a sign error in the difference-based contribution calculation — check `shutdown_components` implementation in `get_individual_contributions()`.
