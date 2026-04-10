---
id: MODEL_005
title: Seasonality — Fourier terms configuration
source: pymc_marketing/mmm/fourier.py, pymc_marketing/mmm/mmm.py
category: core_modeling
tags: [seasonality, fourier, priors, laplace, sparse, controls]
---

Seasonality is modelled with yearly Fourier pairs (sine/cosine terms). Each pair captures one harmonic of the annual cycle.

**Config:**
```yaml
model:
  seasonality:
    yearly_seasonality: 2   # 2 pairs = 4 parameters; adequate for most markets
```

**Prior:** `gamma_fourier ~ Laplace(mu=0, b=0.2)` — sparse prior; prevents seasonal term from absorbing channel variation.

**Decision by data length:**
| Weeks available | yearly_seasonality setting |
|---|---|
| < 52 | 0 (disable) |
| 52–104 | 1–2 |
| ≥ 104 | 2–4 |

**Increase to 4 when:** residual plot shows strong 3- or 6-month seasonal pattern after initial fit with 2 pairs.

**After fitting — inspect seasonality contribution:**
```python
contribs = get_individual_contributions(mmm, df, channel_cols, control_cols)
# contribs['seasonality'] contains the Fourier contribution timeseries
```

**Pitfall:** With < 52 weeks and `yearly_seasonality > 0`, the Fourier terms will overfit to in-sample noise. They will look smooth but will not generalise to holdout.
