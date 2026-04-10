---
id: VALID_001
title: Convergence gates — R-hat, ESS, divergences
source: pymc_marketing/mmm/evaluation.py
category: validation
tags: [convergence, rhat, ess, divergences, arviz, gate, mcmc]
---

Run convergence checks immediately after sampling. **All gates must pass before producing any output.**

```python
import arviz as az

summary = az.summary(idata, var_names=[
    "adstock_alpha", "saturation_lam", "saturation_beta",
    "intercept", "gamma_control", "gamma_fourier", "y_sigma"
])

# Gates:
assert summary["r_hat"].max() < 1.01,      "R-hat failure — refit"
assert summary["ess_bulk"].min() > 400,    "ESS_bulk failure — more draws"
assert summary["ess_tail"].min() > 200,    "ESS_tail failure — more draws"

n_divergences = idata.sample_stats.diverging.sum().item()
assert n_divergences < 5,                  f"Divergences: {n_divergences} — reparameterise"
```

**Thresholds (from geo_config.yml):**
```yaml
diagnostics:
  convergence:
    max_rhat: 1.01
    min_ess: 400
    max_divergences: 0
```

**Fix guide:**
| Failure | Fix |
|---|---|
| R-hat > 1.05 | Increase `tune`; check prior/likelihood conflict |
| Low ESS_bulk | More `draws`; raise `target_accept` |
| Divergences > 0 | `centered: false` for hierarchical params; raise `target_accept` to 0.95 |
| Max tree depth > 5% | Simplify model; reduce number of parameters |

## Convergence passing is necessary but not sufficient

A model can pass all gates above and still produce wrong attribution. Confirmed pattern:
- R-hat=1.003, ESS=1649, 0 divergences → baseline=−30.5%, ROAS=50–300× (unrealistic)

**Why**: MCMC convergence means the sampler found a stable posterior mode. It does not
mean that mode correctly separates channel effects from organic/secular trends. When a
spend channel correlates with time (e.g. Shopping spend grows with the business), the
model can converge on a mode that attributes secular revenue growth to the channel —
inflating ROAS and deflating the baseline.

**Always run attribution checks after convergence passes (see VALID_003):**
- Baseline % within 30–70% of revenue
- No single channel > 50% of revenue unless documented
- ROAS plausibility vs. industry benchmarks or experiment evidence (see UTIL_004)
