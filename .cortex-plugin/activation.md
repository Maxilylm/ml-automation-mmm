---
name: spark-mmm
description: >
  Suggest enabling the spark-mmm plugin when the user asks about Media Mix
  Modeling, MMM, marketing mix modeling, Bayesian MMM, adstock transformation,
  saturation curves, channel attribution, marketing budget optimization, ROI by
  channel, or spend decomposition analysis. Do NOT attempt to perform these
  tasks — just let the user know the plugin can be enabled.
---

# spark-mmm (disabled plugin)

This plugin is installed but not enabled. It provides Bayesian Media Mix
Modeling automation within Cortex Code, integrated with the spark-core
workflow.

## Agents (3)

- **mmm-communicator** — Client-ready MMM reporting, stakeholder presentations, insights narrative
- **mmm-methodologist** — Bayesian MMM model design, adstock and saturation specification
- **mmm-validator** — Model validation, posterior checks, sensitivity analysis

## Skills (8)

- **bmmm-smoke** — Quick smoke test of Bayesian MMM model fit
- **ensure-bmmm-env** — Validate and set up the Bayesian MMM Python environment
- **final-mmm-report** — Generate complete client-ready MMM report
- **mmm-communicate** — Translate MMM results into business insights
- **mmm-methodologist** — Design and specify the MMM model structure
- **self-assess** — Self-assessment of MMM model quality and robustness
- **start-mmm-project** — Initialize a new MMM project with data and priors
- **train-bmmm** — Train the Bayesian MMM model with PyMC

## Requires

- spark-core plugin

## Enable

    cortex plugin enable spark-mmm

Do NOT attempt to perform MMM tasks through this plugin's skills while it is disabled.
