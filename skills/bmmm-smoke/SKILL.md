---
name: bmmm-smoke
description: "Fast smoke test for the Bayesian MMM toolchain — verifies environment, imports, and sampler without full MCMC. Use this whenever you need to validate the MMM environment works before committing to a long training run, or after environment setup."
user_invocable: true
aliases: [mmm smoke, smoke test mmm]
extends: spark
---

# BMMM Smoke Test

Quick validation of the Bayesian MMM toolchain: ensures the environment exists, verifies core imports (pymc, pymc_marketing, arviz), runs a tiny sampler check, and optionally validates a CSV dataset.

## When to Use

- After running `/ensure-bmmm-env` to confirm the environment is functional
- Before a full `/train-bmmm` run to catch setup issues early
- When the `/mmm-methodologist` gate passes with 0 complexity signals

## Workflow

1. **Stage 0 — Utilities Check**: Ensures `ml_utils.py` is present in `src/`
2. **Stage 1 — Platform Detection**: Detects Python runner and sets `PYTENSOR_FLAGS` for cross-platform compatibility
3. **Stage 2 — Ensure Domain Environment**: Runs `ensure_domain_env.py --domain mmm` to create or verify the BMMM-env
4. **Stage 3 — Imports Check**: Verifies `pymc`, `pymc_marketing`, `arviz`, and `numpy` can be imported inside the managed env
5. **Stage 4 — Tiny Sampler Test**: Runs a minimal PyMC model (30 draws, 1 chain) to confirm the sampler starts successfully
6. **Stage 5 — Optional CSV Sanity Check**: If a data path was provided, validates expected columns exist
7. **Report Back**: Summarizes env location, import status, sampler status, and dataset summary

## Report Bus Integration

Writes smoke test results for pipeline gating:
```python
from ml_utils import save_agent_report
save_agent_report("mmm-methodologist", {
    "status": "completed",
    "smoke_test": {"imports": "OK", "sampler": "OK", "dataset": "OK"},
    "ready_for_training": True
})
```

## Full Specification

See `commands/bmmm-smoke.md` for the complete workflow.
