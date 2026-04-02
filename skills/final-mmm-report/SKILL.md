---
name: final-mmm-report
description: "Generate a consolidated final report for an MMM project from all pipeline artifacts. Use this whenever a training run is complete and you need a single document summarizing the entire MMM analysis, even if the user just says 'write the report' or 'summarize results'."
user_invocable: true
aliases: [mmm report, mmm final report]
extends: ml-automation
---

# Final MMM Report

Consolidate all pipeline artifacts (problem brief, design memo, validation report, model outputs) into a single human-readable final report. This command is report-only and never runs MCMC.

## When to Use

- After `/train-bmmm` completes successfully and you need a consolidated deliverable
- The user asks for a "final report", "summary of the MMM run", or "project report"
- You need to collect all existing artifacts into one document before communicating results

## Workflow

1. **Stage 0 — Utilities Check**: Ensures `ml_utils.py` is present in `src/`
2. **Stage 1 — Resolve Paths**: Determines `project_dir`, reads `LATEST.txt` for `run_id` if not provided, sets output path
3. **Stage 2 — Collect Inputs**: Reads `problem_brief_mmm.md`, `design_memo_mmm.md`, and validation report if they exist
4. **Stage 3 — Write Final Report**: Produces `final_report.md` with executive summary, data readiness, model spec, results, artifacts, and next steps

## Report Bus Integration

Writes the consolidated report for downstream communication:
```python
from ml_utils import save_agent_report
save_agent_report("mmm-methodologist", {
    "status": "completed",
    "artifact": "final_report.md",
    "next_step": "/mmm-communicate <project_name>"
})
```

## Full Specification

See `commands/final-mmm-report.md` for the complete workflow.
