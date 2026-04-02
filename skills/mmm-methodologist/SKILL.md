---
name: mmm-methodologist
description: "Gate command for MMM methodologist review — scores complexity signals and decides whether a full expert review is needed before training. Use this after /start-mmm-project to validate the design, even if the user just says 'review the design' or 'check if we're ready to train'."
user_invocable: true
aliases: [mmm methodologist, methodologist review, mmm review]
extends: spark
---

# MMM Methodologist Gate

Reads the existing design memo, scores complexity signals (geo dimensions, channel count, calibration evidence, collinearity), and decides whether a full methodologist review is warranted or the project can proceed directly to smoke testing.

## When to Use

- Immediately after `/start-mmm-project` completes the design phase
- The user wants to validate whether the MMM design needs expert review before training
- Before `/bmmm-smoke` to ensure the model configuration is sound

## Workflow

1. **Stage 1 — Locate Design Memo**: Reads `LATEST.txt` to resolve `run_id`, then loads `design_memo_mmm.md`
2. **Stage 2 — Evaluate Complexity Signals**: Scores 7 binary signals (multiple geos, many channels, calibration evidence, long-cycle adstock, binary channels, high collinearity, short series)
3. **Stage 3 — Gate Decision**: Routes based on signal count:
   - **0 signals**: PASS -- skip agent, suggest `/bmmm-smoke`
   - **1-2 signals**: Review recommended -- invoke `mmm-methodologist` agent
   - **3+ signals**: Review required -- invoke `mmm-methodologist` agent
4. **Stage 4 — Execute Decision**: Either prints pass-through message or spawns the `mmm-methodologist` subagent with flagged signals

## Report Bus Integration

Writes the gate decision for pipeline routing:
```python
from ml_utils import save_agent_report
save_agent_report("mmm-methodologist", {
    "status": "completed",
    "gate": "pass|review_recommended|review_required",
    "signals_flagged": 0,
    "next_step": "/bmmm-smoke or agent review"
})
```

## Full Specification

See `commands/mmm-methodologist.md` for the complete workflow.
