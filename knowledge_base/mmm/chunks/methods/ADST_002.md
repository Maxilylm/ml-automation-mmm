---
id: ADST_002
title: WeibullCDFAdstock — long-lag channels
source: pymc_marketing/mmm/components/adstock.py
category: transformations
tags: [adstock, weibull, tv, ooh, long_lag, carryover]
---

`WeibullCDFAdstock` models channels with delayed peak effects (TV, OOH, brand campaigns). The CDF form produces a smooth hill-shaped kernel — effect builds, peaks, then decays.

**Instantiation:**
```python
from pymc_marketing.mmm.components.adstock import WeibullCDFAdstock
adstock = WeibullCDFAdstock(l_max=13)  # 13-week window for TV
```

**Default priors:** `lam ~ Gamma(mu=2, sigma=2.5)`, `k ~ Gamma(mu=2, sigma=2.5)`.

**Decision rule:**
- Use `WeibullCDFAdstock` when: TV, OOH, or brand-building channels; evidence of delayed peak (lag > 2 weeks before maximum effect).
- Use `WeibullPDFAdstock` when: similarly long lags but the kernel should peak then decay faster (PDF is more peaked than CDF).
- Use `GeometricAdstock` for all digital channels.

**Identification note:** Weibull requires more temporal variation in spend to identify `lam` and `k` separately. If spend is near-constant, fall back to `GeometricAdstock` and document.

**Visualise the prior kernel:**
```python
prior = adstock.sample_prior()
curve = adstock.sample_curve(prior)
adstock.plot_curve(curve)
```
