---
id: PRIOR_001
title: Spend-share priors — standard configuration
source: pymc_marketing/prior.py, mmm_config.yml
category: priors_constraints
tags: [priors, spend_share, intercept, gamma_control, config, yaml]
---

**Standard prior block (from `mmm_config.yml`):**
```yaml
priors:
  use_spend_share_priors: true
  spend_share_multiplier: 2    # set to n_channels
  intercept:
    distribution: Normal
    mu: 0.5
    sigma: 0.2
  gamma_control:
    distribution: Normal
    mu: per-control           # see per-control calibration table below
    sigma: per-control        # scalar sigma insufficient — use array aligned to control_cols
  gamma_fourier:
    distribution: Laplace
    mu: 0
    b: 0.2                    # sparse — prevents seasonal over-fit
  likelihood:
    distribution: Normal
    sigma:
      distribution: HalfNormal
      sigma: 6
```

**`use_spend_share_priors: true`** sets channel beta priors proportional to each channel's share of total spend. This is the recommended default — it prevents large-spend channels from dominating purely due to scale.

**`spend_share_multiplier`**: controls total prior strength. Set to `n_channels`; increase to `2*n_channels` for more conservative priors when channels are collinear.

**Intercept:** On log scale after normalisation. `Normal(0.5, 0.2)` centres expected log-revenue slightly above 0. Adjust `mu` if log(mean_target_normalised) deviates significantly from 0.5.

**`gamma_control` — per-control calibration (required):**

Controls are heterogeneous. A single shared sigma is insufficient — use a per-control dict and pass a numpy array aligned to `control_cols`:

```python
PRIOR_GAMMA_CTRL_MU = {
    "t":             0.00,   # no prior direction
    "covid_flag":   -0.15,   # known negative; informed by industry evidence
    "promo_flag":    0.00,   # direction uncertain
    "price_index":   0.00,   # direction uncertain
    "organic_proxy": 0.00,   # no prior direction
}
PRIOR_GAMMA_CTRL_SIGMA = {
    "t":             0.08,   # trend
    "covid_flag":    0.20,   # structural break — tighter when mu is informed
    "promo_flag":    0.20,   # event flag
    "price_index":   0.05,   # price elasticity
    "organic_proxy": 0.15,   # normalised organic proxy
}
mus    = np.array([PRIOR_GAMMA_CTRL_MU[c]    for c in control_cols])
sigmas = np.array([PRIOR_GAMMA_CTRL_SIGMA[c] for c in control_cols])
"gamma_control": Prior("Normal", mu=mus, sigma=sigmas)
```

The pymc-marketing `Prior` API accepts array-valued sigma — confirmed working.

| Control type | Typical sigma | Rationale |
|---|---|---|
| Trend `t` | 0.05–0.10 | Tight; prevent trend from absorbing media signal |
| Price index | 0.05 | Known elasticity range: −0.05 to −0.10 in log space |
| Promo / event flag | 0.15–0.25 | Effect direction uncertain; allow flexibility |
| Structural break (COVID, policy) | 0.30–0.50 | Can be large and poorly identified; let data speak |
| Organic proxies (normalised) | 0.10–0.20 | Correlated with baseline demand, not media |
| Organic proxies — weakly identified (\|corr\| < 0.05) | **0.08** | Prior-dominated; tighten to prevent spurious attribution. Always include — flag as `[WEAKLY IDENTIFIED]` in design memo. |

All controls must be on unit scale before fitting (mean-normalise continuous proxies; binary flags are already unit scale).
