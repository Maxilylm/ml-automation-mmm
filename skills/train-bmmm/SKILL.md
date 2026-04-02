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

## Workflow

1. **Stage 0 — Ensure Core Utilities**: Copies `ml_utils.py` and `mmm_utils.py` into `src/` if missing
2. **Stage 1 — Platform Detection**: Detects Python runner (`py` vs `python3`) and sets `PYTENSOR_FLAGS` for Windows compatibility
3. **Stage 2 — Ensure Domain Environment**: Runs `ensure_domain_env.py` to guarantee the BMMM conda/venv is ready
4. **Stage 3 — Run MCMC Training**: Executes `scripts/mmm/build.py` inside the managed environment with proper encoding flags
5. **Stage 4 — Self-Assessment**: Writes feedback to `feedback/mmm/<project_name>/` (runs even if training failed)
6. **Stage 5 — Generate Final Report**: Automatically invokes `/final-mmm-report` on success

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
