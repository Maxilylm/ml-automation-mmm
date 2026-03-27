# ml-automation-mmm

Media Mix Modeling extension for [ml-automation](https://github.com/Maxilylm/ml-automation-core).

## Prerequisites

- [ml-automation](https://github.com/Maxilylm/ml-automation-core) core plugin (>= v1.8.0)
- Claude Code CLI

## Installation

```bash
claude plugin add /path/to/ml-automation-mmm
```

## What's Included

### Agents

| Agent | Purpose | Hooks Into |
|---|---|---|
| `mmm-methodologist` | Design and review MMM models | `after-eda` |
| `mmm-validator` | Validate MMM results | `after-evaluation` |
| `mmm-communicator` | Client-ready business narratives | *(MMM workflows only)* |

### Commands

| Command | Purpose |
|---|---|
| `/start-mmm-project` | Bootstrap MMM project (brief, data readiness, design memo) |
| `/mmm-methodologist` | Gate command — scores complexity, routes to review |
| `/bmmm-smoke` | Fast smoke test for Bayesian MMM toolchain |
| `/train-bmmm` | Full MCMC training run |
| `/final-mmm-report` | Consolidate artifacts into final report |
| `/mmm-communicate` | Convert results to client narrative |
| `/ensure-bmmm-env` | Ensure Python environment exists |
| `/self-assess` | Aggregate feedback across runs |

## How It Integrates

When installed alongside the core plugin:

1. **Automatic routing** — Tasks mentioning "MMM", "media mix", "channel attribution" etc. are routed to MMM agents via the core assigner (Priority 2.5)
2. **Core workflow hooks** — When running `/team-coldstart` on marketing data:
   - `mmm-methodologist` fires at `after-eda` to review data for MMM suitability
   - `mmm-validator` fires at `after-evaluation` to validate MMM-specific metrics
3. **Core agent reuse** — MMM commands use core agents (eda-analyst, developer, mlops-engineer) directly

## Setup Knowledge Base

After cloning, copy the knowledge base content from the source repository:

```bash
# Copy from BLEND360/spark-bayesian-mmm-agent (requires access)
cp -r /path/to/source/knowledge_base/mmm/* knowledge_base/mmm/
cp -r /path/to/source/scripts/* scripts/
```

## License

MIT
