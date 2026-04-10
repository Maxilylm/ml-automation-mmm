---
id: MODEL_001
title: MMM class — fit and predict API
source: pymc_marketing/mmm/mmm.py
category: core_modeling
tags: [mmm, fit, predict, api, entry_point, pymc_marketing]
---

The `MMM` class is the primary interface. Instantiate with transform objects, call `fit()`.

```python
from pymc_marketing.mmm import MMM, GeometricAdstock, LogisticSaturation

mmm = MMM(
    date_column="date_week",
    channel_columns=["ch_search", "ch_social", "ch_tv"],
    adstock=GeometricAdstock(l_max=8),
    saturation=LogisticSaturation(),
    control_columns=["t", "event_promo", "event_holiday"],
)

# Fit — mmm.fit() handles build + sampling and sets mmm.idata internally
mmm.fit(
    X=df[channel_cols + control_cols],
    y=df["y"],
    draws=1000,
    tune=1000,
    chains=2,
    target_accept=0.90,
    nuts_sampler="numpyro",
    random_seed=42,
)
```

**Key outputs after fitting:**
- `mmm.idata`: ArviZ InferenceData — all posteriors
- `mmm.sample_posterior_predictive(X, y, combined=True)`: posterior predictions (returns `xarray.Dataset`; `original_scale=True` arg removed in 0.10+)
- `mmm.plot_channel_contribution_share_of_total()`: contribution chart

**API note (pymc-marketing >= 0.10 / 0.18.2):** Do NOT use the old pattern `with mmm.model: pm.sample(...)` + `mmm.idata = idata` — it no longer works reliably. Use `mmm.fit()` directly. `mmm.get_errors()` does not exist in the official API; compute MAPE manually from `sample_posterior_predictive` output.
