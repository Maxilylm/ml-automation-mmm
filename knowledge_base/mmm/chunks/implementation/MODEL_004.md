---
id: MODEL_004
title: Sampler configuration — recommended settings
source: pymc_marketing/model_builder.py
category: core_modeling
tags: [sampler, nuts, numpyro, chains, target_accept, draws, convergence]
---

**Standard model (single market):**
```python
with mmm.model:
    idata = pm.sample(
        draws=2000, tune=2000, chains=4,
        target_accept=0.90,
        nuts_sampler="numpyro",   # 10–50x faster than default PyMC
        random_seed=327,
    )
```

**Geo / hierarchical model (more complex geometry):**
```python
    idata = pm.sample(
        draws=2000, tune=2000, chains=4,
        target_accept=0.95,       # Raise to handle hierarchical funnels
        nuts_sampler="numpyro",
        random_seed=327,
    )
```

**Quick diagnostic pass (before full run):**
```python
    idata = pm.sample(draws=500, tune=500, chains=2, target_accept=0.85)
    # Check R-hat and divergences first — fix issues before scaling to 2000 draws
```

**Sampler backends:** `nuts_sampler="numpyro"` requires JAX. `nuts_sampler="blackjax"` also fast. Default is PyMC's built-in (slowest). `nuts_sampler="nutpie"` for GPU.

**random_seed:** Always set for reproducibility. Convention: `327` = `sum(map(ord, "mmm"))`.

**target_accept:** Start at 0.90; raise to 0.95 only if divergences persist after reparameterisation.
