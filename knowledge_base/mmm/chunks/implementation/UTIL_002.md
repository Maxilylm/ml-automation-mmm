---
id: UTIL_002
title: idata I/O — save and reload InferenceData
source: pymc_marketing/model_builder.py, pymc_marketing/utils.py
category: core_modeling
tags: [idata, save, load, netcdf, reproducibility, checkpoint]
---

Always save `idata` after sampling. Resampling is expensive and results may differ between runs without a fixed seed.

**Save:**
```python
idata.to_netcdf("outputs/idata_v1.nc")
# Or via the MMM wrapper:
mmm.idata.to_netcdf("outputs/idata_v1.nc")
```

**Load:**
```python
import arviz as az
idata = az.from_netcdf("outputs/idata_v1.nc")
mmm.idata = idata   # Reattach to model object for prediction/reporting
```

**What idata contains:**
- `.posterior`: all MCMC draws (adstock_alpha, saturation params, etc.)
- `.sample_stats`: divergences, tree_depth, energy, leapfrog steps
- `.posterior_predictive`: if `sample_posterior_predictive` was run with `extend_idata=True`
- `.prior`: if `sample_prior_predictive` was run

**Version control note:** Commit `idata.nc` only if size < 50MB. For large models, store in cloud and reference the path in the project README. Always record the random_seed and PyMC version alongside the file for reproducibility.

**Reattach after load:**
```python
# mmm.model must be rebuilt before predictions after reload
mmm.build_model(X=df_train[feature_cols], y=df_train["y"])
mmm.idata = idata
preds = mmm.sample_posterior_predictive(df, original_scale=True)
```
