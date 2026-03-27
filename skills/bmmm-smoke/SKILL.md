---
name: bmmm-smoke
description: "Fast smoke test for the Bayesian MMM toolchain — verifies environment, imports, and sampler without full MCMC"
user_invocable: true
aliases: [mmm smoke, smoke test mmm]
extends: ml-automation
---

# BMMM Smoke Test

Quick validation of the Bayesian MMM toolchain: ensures the environment exists, verifies core imports (pymc, pymc_marketing, arviz), runs a tiny sampler check, and optionally validates a CSV dataset.

## Full Specification

See `commands/bmmm-smoke.md` for the complete workflow.
