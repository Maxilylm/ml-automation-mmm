---
id: UTIL_001
title: Divergence triage — diagnosis and fixes
source: playbook §6, pymc_marketing/mmm/base.py
category: core_modeling
tags: [divergences, convergence, funnel, reparameterize, debug, nuts]
---

Divergences indicate NUTS explored a region with very steep log-posterior gradient. They are NOT just "warnings" — divergences mean the posterior was not properly sampled.

**Step 1 — Quantify:**
```python
n_div = idata.sample_stats.diverging.sum().item()
pct_div = n_div / (idata.sample_stats.diverging.size) * 100
print(f"Divergences: {n_div} ({pct_div:.1f}%)")
```

**Step 2 — Locate (which parameters):**
```python
import arviz as az
az.plot_pair(idata, var_names=["adstock_alpha", "saturation_lam"],
             divergences=True)  # Divergences shown as red dots
```

**Step 3 — Fix by cause:**

| Symptom | Root cause | Fix |
|---|---|---|
| Divergences near adstock alpha = 0 or 1 | Prior too flat on boundary | Switch to Beta(2, 5); add `centered: false` |
| Divergences near saturation lam ≈ 0 | Saturation unidentified | Use `NoSaturation` for that channel |
| Divergences in hierarchical model | Funnel geometry | `centered: false` for ALL hierarchical priors |
| Scatter divergences (no clear cluster) | Global geometry issue | Raise `target_accept` to 0.95 |

**Last resort:** Simplify model (remove one channel or transform), re-run, confirm convergence, then progressively add complexity back.
