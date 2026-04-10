---
id: REPORT_004
title: compare_predictions — counterfactual scenario analysis
source: b2b_src/contributions.py
category: reporting
tags: [counterfactual, compare_predictions, shutdown_channels, marginal_changes, scenario]
---

`compare_predictions()` plots observed vs. modified model predictions for counterfactual scenarios.

```python
from b2b_src.contributions import compare_predictions

# Scenario 1: Shut down a channel entirely
fig = compare_predictions(
    mmm=mmm, data=df,
    shutdown_channels=["tv"],
    original_scale=True,
    random_seed=327
)

# Scenario 2: Marginal budget change (+20% search, -10% social)
fig = compare_predictions(
    mmm=mmm, data=df,
    marginal_changes={"paid_search": 0.2, "paid_social": -0.1},
    original_scale=True,
    random_seed=327
)

# Scenario 3: Get predictions programmatically (no plot)
result = compare_predictions(
    mmm=mmm, data=df,
    shutdown_channels=["tv"],
    original_scale=True,
    return_predictions=True,
    random_seed=327
)
# result['relative_change_pct'] → % revenue lost by shutting down tv
```

**Returns when `return_predictions=True`:**
`dates`, `original_mean/lower/upper`, `modified_mean/lower/upper`, `observed`, `relative_change_pct`.

**Mechanism:** `marginal_changes={"ch": 0.2}` multiplies channel column by `1.2`. `shutdown_channels=["ch"]` sets channel column to 0. Requires `original_scale=False` inside, then `exp()` if `original_scale=True`.
