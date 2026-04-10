---
id: MODEL_003
title: Prior predictive check — required before sampling
source: pymc_marketing/mmm/base.py, pymc_marketing/model_builder.py
category: core_modeling
tags: [prior_predictive, sanity_check, priors, model_build, bayesian]
---

Always run a prior predictive check before MCMC sampling. It validates that your priors produce plausible revenue ranges.

## Correct pattern — call order matters

**Option A (explicit build first — preferred in scripts):**
```python
mmm.build_model(X=X_train, y=y_train)   # sets target_scale = max(y_train)
prior_pred = mmm.sample_prior_predictive(samples=500, random_seed=42)
mmm.fit(X_train, y_train, ...)           # skips rebuild — uses correctly-scaled model
```

**Option B (pass y to sample_prior_predictive directly):**
```python
prior_pred = mmm.sample_prior_predictive(X_train, y=y_train,
                                          extend_idata=False, random_seed=42)
mmm.fit(X_train, y_train, ...)           # skips rebuild — uses correctly-scaled model
```

Both options are valid. In both cases `y=y_train` must reach `build_model()` so that
`target_scale = max(y_train)` is set correctly before MCMC.

## CRITICAL: never call `sample_prior_predictive(X_train)` without `y`

```python
# WRONG — causes silent complete MCMC collapse
prior_pred = mmm.sample_prior_predictive(X_train, extend_idata=False)
mmm.fit(X_train, y_train, ...)
```

**Why it fails**: `sample_prior_predictive(X)` without `y` internally calls
`build_model(X, zeros)`, which computes `target_scale = max(zeros) → 1`.
`MMM.fit()` has `if not hasattr(self, "model"): build_model(X, y)` — model already
exists, so rebuild is **skipped**. MCMC then fits raw target values (e.g. £3.5M/week)
against priors calibrated for `[0, 1]` → complete collapse: R-hat=4+, ESS=4, MAPE=100%.

## Displaying prior predictive in original units

`ppc["y"]` is on the `[0, 1]` max-scaled target. Multiply by `mmm.target_scale` for display:

```python
target_scale = float(mmm.target_scale)
y_prior      = ppc["y"].values                          # [0,1] scale
prior_p5     = np.percentile(y_prior, 5)  * target_scale
prior_p95    = np.percentile(y_prior, 95) * target_scale
obs_mean     = float(y_train.mean())
# Compare prior_p5 / prior_p95 against obs_mean for coverage check
```

## What to look for

- Prior predictive median ≈ observed mean (within 2×). If median ≈ 0 → intercept prior wrong scale.
- Range covers observed min–max without extending to impossibly large values.
- No systematic all-negative draws (intercept prior too negative).

**If prior predictive fails:**
- Median ≈ 0 or all values near 0 → `y` not passed to `build_model`; or intercept prior miscalibrated (see PRIOR_006).
- HDI too wide (> 100× observed range) → reduce `saturation_beta` sigma (see PRIOR_006).
- All prior samples identical → model not built correctly; check call order above.
