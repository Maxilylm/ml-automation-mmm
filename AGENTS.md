# spark-mmm — Cortex Code Extension

Media Mix Modeling. Bayesian MMM with adstock, saturation, channel attribution, budget optimization, and client-ready reporting. Requires spark-core installed.

## Available Agents

| Agent | When to use |
|---|---|
| `mmm-methodologist` | User wants to design an MMM, choose priors, configure adstock/saturation, or address methodological questions |
| `mmm-communicator` | User wants to produce client-ready reports, ROI summaries, budget allocation recommendations, or executive presentations |
| `mmm-validator` | User wants to validate MMM outputs, run diagnostics, or check posterior predictive checks |

## Available Skills

| Skill | Trigger |
|---|---|
| `/start-mmm-project` | "start an MMM project", "set up media mix modeling", "initialize MMM" |
| `/mmm-methodologist` | "design the MMM", "choose priors", "configure adstock", "MMM methodology advice" |
| `/train-bmmm` | "train the Bayesian MMM", "fit the MMM model", "run PyMC sampling" |
| `/bmmm-smoke` | "smoke test the MMM", "quick sanity check on MMM", "verify MMM setup" |
| `/mmm-communicate` | "create MMM report", "ROI summary", "budget allocation chart", "client presentation" |
| `/final-mmm-report` | "final MMM report", "full client deliverable", "complete MMM summary" |
| `/self-assess` | "assess MMM quality", "self-critique the model", "check MMM assumptions" |
| `/ensure-bmmm-env` | "set up BMMM environment", "install MMM dependencies", "configure PyMC env" |

## Routing

- Methodology, priors, adstock/saturation design → `mmm-methodologist`
- Client reporting, ROI, budget allocation → `mmm-communicator`
- Diagnostics, validation, posterior checks → `mmm-validator`
- Fallback → spark-core orchestrator
