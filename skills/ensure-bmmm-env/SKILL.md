---
name: ensure-bmmm-env
description: "Ensure the Bayesian MMM conda/venv environment exists with all required dependencies. Use this whenever you need PyMC or pymc-marketing available, even if the user just says 'set up the environment' or 'install MMM dependencies'."
user_invocable: true
aliases: [bmmm env, mmm env, ensure mmm env, ensure bmmm env]
extends: spark
---

# Ensure BMMM Environment

Make sure the Bayesian MMM runtime environment exists at `knowledge_base/mmm/BMMM-env/`. Creates seed `environment.yaml` and `requirements.txt` if missing, then builds the env and verifies core imports.

## When to Use

- Before any command that runs Python inside the BMMM environment (`/train-bmmm`, `/bmmm-smoke`)
- When setting up a new machine or project for the first time
- After a failed training run where the environment may be corrupted or incomplete

## Workflow

1. **Stage 1 — Check Existing Environment**: If env directory already exists, reuse it
2. **Stage 2 — Create from Specs**: If `environment.yaml` or `requirements.txt` exist but env does not, create from those files
3. **Stage 3 — Seed and Create**: On first run, generates seed dependency files then creates the environment
4. **Stage 4 — Verify**: Runs an import check for `pymc` and `pymc_marketing` inside the env to confirm success

## Report Bus Integration

Writes environment status for downstream commands:
```python
from ml_utils import save_agent_report
save_agent_report("mmm-methodologist", {
    "status": "completed",
    "env_path": "knowledge_base/mmm/BMMM-env/",
    "verified": True
})
```

## Full Specification

See `commands/ensure-bmmm-env.md` for the complete workflow.
