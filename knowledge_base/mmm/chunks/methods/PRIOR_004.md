---
id: PRIOR_004
title: Scaling — global max scaling for multi-dimensional models
source: pymc_marketing/mmm/scaling.py, geo_config.yml
category: priors_constraints
tags: [scaling, normalization, global_max, multi_dimensional, leakage, dims]
---

Scaling normalises spend and target before fitting. In multi-dimensional (geo) models, use **global max scaling** — scaling across all geos together. Per-geo scaling creates inconsistent scales and breaks hierarchical pooling.

**Config (`geo_config.yml`):**
```yaml
model:
  apply_scaling: true
  scaling:
    channel:
      method: max
      dims: []      # dims: [] = global max (across ALL geos)
    target:
      method: max
      dims: []
```

**`dims: []`** means: compute the max across all observations, all geos. This is the required setting for hierarchical models.

**`dims: ["Groups"]`** would mean: compute max per geo (WRONG for hierarchical — avoids this).

**After fitting, inverse-transform for reporting:**
```python
# mmm.target_scale is automatically stored
mean_log = predictions.mean(dim="sample")
mean_original = np.exp(mean_log) * mmm.target_scale
```

**Leakage check:** Scaling must be fitted on training data only, then applied to holdout using the same scaler. In `pymc_marketing`, this is handled automatically when `build_model()` is called on training data.
