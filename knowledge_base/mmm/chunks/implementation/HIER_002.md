---
id: HIER_002
title: Pooling strategy — when to pool, partial pool, or unpool
source: geo_config.yml, pymc_marketing/mmm/multidimensional.py
category: core_modeling
tags: [hierarchical, pooling, partial_pooling, unpooled, geo, sigma_market]
---

**Pooling decision by number of markets and parameter type:**

| Markets | Recommended strategy |
|---|---|
| ≥ 5 | Partial pooling (hierarchical) for saturation and intercept |
| 3–4 | Careful partial pooling — inspect `sigma_market` posterior |
| < 3 | Full pooling or fit separate single-market models |

**Parameter-level pooling config (`geo_config.yml`):**
```yaml
dimensions:
  pooling:
    default_strategy: hierarchical
    pooled_params:       ["gamma_control"]       # Fully shared — controls same across geos
    unpooled_params:     ["adstock_alpha"]        # Separate per geo — media decay varies
    hierarchical_params: ["saturation_beta", "intercept", "gamma_fourier"]
```

**sigma_market check after fitting:**
```python
# If sigma posterior ≈ 0 → geos behave like same market → consider full pooling
# If sigma posterior > 1.5 (on log scale) → geos too different → consider separate models
az.plot_posterior(idata, var_names=["saturation_beta_std"])
```

**Warning:** Pooling structurally different markets (e.g., different media mix, different seasonality) introduces bias in all market estimates. Use unpooled params or separate models for markets with fundamentally different dynamics.
