---
id: REPORT_001
title: get_individual_contributions — decomposition API
source: b2b_src/contributions.py
category: reporting
tags: [contributions, decomposition, channels, intercept, seasonality, reporting]
---

`get_individual_contributions()` decomposes total predicted revenue into per-component contributions by shutting down one component at a time.

```python
from b2b_src.contributions import get_individual_contributions

contribs = get_individual_contributions(
    mmm=mmm,
    data=df,
    channel_cols=channel_info['channel_columns'],
    control_cols=control_cols,
    random_seed=327,
)
```

**Returns dict with keys:**
- `dates`: array of date values
- `channels`: `{channel_name: xarray(sample, date)}` — contribution per channel per week
- `controls`: `{control_name: xarray(sample, date)}` — contribution per control variable
- `intercept`: `xarray(sample, date)` — baseline intercept contribution
- `seasonality`: `xarray(sample, date)` — Fourier seasonality contribution

**Mechanism:** For each component, calls `sample_posterior_predictive(..., shutdown_components=[component])`, then subtracts from full-model predictions. Requires `include_last_observations=False`.

**Reproducibility:** Always set `random_seed`. Each `sample_posterior_predictive()` call gets a unique child seed derived from the main seed via `SeedSequence`.

**Typical aggregate summary:**
```python
for ch in channel_cols:
    mean_contrib = contribs['channels'][ch].mean("sample").sum("date").item()
    print(f"{ch}: {mean_contrib:.0f} total revenue contribution")
```
