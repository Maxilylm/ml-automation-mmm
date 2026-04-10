---
id: MODEL_002
title: Log-transform order and inverse-transform pitfall
source: pymc_marketing/mmm/mmm.py, b2b_src/contributions.py
category: core_modeling
tags: [log_transform, exp, inverse_transform, pitfall, jensens_inequality, scale]
---

The model fits in log-space. Predictions from `sample_posterior_predictive(original_scale=False)` are in log-space and must be inverse-transformed correctly.

**CORRECT pattern (average in log-space, then exponentiate):**
```python
preds = mmm.sample_posterior_predictive(df, original_scale=False)
mean_log = preds[mmm.output_var].mean(dim=["chain", "draw"]).values
mean_original = np.exp(mean_log) * mmm.target_scale
```

**WRONG pattern (Jensen's inequality bias — overstates revenue):**
```python
# DO NOT:
samples_original = np.exp(preds[mmm.output_var].values)
biased_mean = samples_original.mean(axis=(0,1))  # Wrong — higher than true mean
```

**Why:** `E[exp(X)] ≥ exp(E[X])` by Jensen's inequality. Exponentiating individual samples then averaging inflates the estimate.

**Config to enable:**
```yaml
model:
  log_transformation:
    - "target"    # log(y + 1) before fitting
    - "channels"  # log(x + 1) per channel
```

**target_scale:** `mmm.target_scale` stores the scale factor applied before fitting (often max of training target). Always multiply after `exp()`.
