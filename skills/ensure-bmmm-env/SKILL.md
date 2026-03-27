---
name: ensure-bmmm-env
description: "Ensure the Bayesian MMM conda/venv environment exists with all required dependencies"
user_invocable: true
aliases: [bmmm env, mmm env, ensure mmm env, ensure bmmm env]
extends: ml-automation
---

# Ensure BMMM Environment

Make sure the Bayesian MMM runtime environment exists at `knowledge_base/mmm/BMMM-env/`. Creates seed environment.yaml and requirements.txt if missing.

## Full Specification

See `commands/ensure-bmmm-env.md` for the complete workflow.
