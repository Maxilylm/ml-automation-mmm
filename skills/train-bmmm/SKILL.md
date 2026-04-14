---
name: train-bmmm
description: "Run full Bayesian MMM training with MCMC sampling using the managed environment runner. Use this whenever the user wants to train, fit, or run a Bayesian Media Mix Model, even if they just say 'run the model' or 'fit the MMM'."
user_invocable: true
aliases: [train mmm, mmm train, bmmm train]
extends: spark
---

# Train BMMM

Run a full Bayesian Media Mix Model training using PyMC/pymc-marketing inside the managed BMMM environment. Handles environment setup, MCMC sampling, and generates a final report.

## When to Use

- The design memo and data readiness checklist are complete and the user is ready to train
- The user asks to "train the model", "run MCMC", or "fit the Bayesian MMM"
- After `/mmm-methodologist` has passed or completed its review

## MCMC with Informative Priors (v1.1.0)

**CRITICAL**: Always use full PyMC MCMC sampling with informative priors. Never fall back to MLE (Maximum Likelihood Estimation). MLE defeats the purpose of Bayesian MMM — it cannot encode domain knowledge and overfits on small marketing datasets.

Required prior structure for channel coefficients:
```python
import pymc as pm

with pm.Model() as mmm:
    # Intercept — weakly informative
    intercept = pm.Normal("intercept", mu=0, sigma=2)

    # Channel coefficients — MUST be positive (spend increases response)
    beta_channel = pm.HalfNormal("beta_channel", sigma=1, shape=n_channels)

    # Adstock decay — informative: marketing effects decay over 1-8 weeks
    alpha = pm.Beta("adstock_alpha", alpha=3, beta=3, shape=n_channels)

    # Saturation — hill function half-saturation
    lam = pm.Gamma("saturation_lam", alpha=3, beta=1, shape=n_channels)

    # Noise
    sigma = pm.HalfNormal("sigma", sigma=1)

    # MCMC — never use pm.find_MAP() as the final result
    idata = pm.sample(draws=1000, tune=1000, chains=4, cores=2,
                      target_accept=0.9, random_seed=42)
```

If MCMC fails to converge (divergences > 5% or R-hat > 1.05), **diagnose and fix** — do not fall back to MLE. Common fixes:
- Increase `target_accept` to 0.95-0.99
- Tighten priors based on domain knowledge
- Check data scaling (standardize spend columns)
- Reduce model complexity (fewer channels, simpler saturation)

## Workflow

1. **Stage 0 — Ensure Core Utilities**: Copies `ml_utils.py` and `mmm_utils.py` into `src/` if missing
2. **Stage 1 — Platform Detection**: Detects Python runner (`py` vs `python3`) and sets `PYTENSOR_FLAGS` for Windows compatibility
3. **Stage 2 — Ensure Domain Environment**: Runs `ensure_domain_env.py` to guarantee the BMMM conda/venv is ready (with `pytensor>=2.18`)
4. **Stage 3 — Run MCMC Training**: Executes `scripts/mmm/build.py` inside the managed environment with proper encoding flags. MUST use `pm.sample()` with informative priors — never `pm.find_MAP()` alone.
5. **Stage 3b — Convergence Check**: Verify R-hat < 1.05, ESS > 400, divergences < 5%. If checks fail, re-run with tighter priors or higher `target_accept`.
6. **Stage 4 — Self-Assessment**: Writes feedback to `feedback/mmm/<project_name>/` (runs even if training failed)
7. **Stage 5 — Generate Final Report**: Automatically invokes `/final-mmm-report` on success

## Report Bus Integration

Writes structured output for downstream reporting:
```python
from ml_utils import save_agent_report
save_agent_report("mmm-methodologist", {
    "status": "completed",
    "training": {"converged": True, "run_id": "..."},
    "next_step": "/final-mmm-report <project_name>"
})
```

## Full Specification

See `commands/train-bmmm.md` for the complete workflow.
