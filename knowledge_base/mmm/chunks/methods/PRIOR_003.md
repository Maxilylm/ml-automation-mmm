---
id: PRIOR_003
title: Hierarchical priors — non-centered parameterisation (geo model)
source: pymc_marketing/mmm/multidimensional.py, geo_config.yml
category: priors_constraints
tags: [hierarchical, non_centered, geo, partial_pooling, saturation_beta, adstock]
---

For geo/multi-dimensional models, ALL hierarchical parameters must use `centered: false`. Centered parameterisation causes funnel geometry in NUTS, leading to high divergences.

**Hierarchical saturation beta (recommended):**
```yaml
priors:
  saturation_beta:
    type: LogNormalPrior
    mean:
      distribution: Gamma
      mu: 0.25
      sigma: 0.10
      dims: ["channel"]          # Hyperprior per channel
    std:
      distribution: Exponential
      scale: 0.10
      dims: ["channel"]
    dims: ["channel", "Groups"]  # Posterior varies by channel AND geo
    centered: false              # REQUIRED for NUTS stability
```

**Adstock alpha — unpooled per geo (conservative default):**
```yaml
priors:
  adstock_alpha:
    distribution: Beta
    alpha: 2
    beta: 5
    dims: ["Groups", "channel"]  # One alpha per geo × channel
```

**sigma_market inspection (after fitting):**
```python
az.plot_posterior(idata, var_names=["saturation_beta_std"])
# If posterior mass near 0 → strong pooling (geos are similar)
# If mass > 1.5 on log scale → geos too heterogeneous; consider unpooled
```
