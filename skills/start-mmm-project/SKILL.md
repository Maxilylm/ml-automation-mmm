---
name: start-mmm-project
description: "Bootstrap a new MMM project — generates problem brief, data readiness checklist, and design memo from the MMM knowledge pack. Use this whenever a user has media/marketing spend data and wants to begin a Marketing Mix Model, even if they just say 'analyze my marketing data' or 'set up an MMM'."
user_invocable: true
aliases: [mmm start, start mmm, bootstrap mmm]
extends: ml-automation
---

# Start MMM Project

Initialize the standard MMM project artifacts using the built-in MMM knowledge pack. Profiles your data, loads relevant knowledge chunks, and generates a problem brief, data readiness checklist, and design memo with concrete, data-driven decisions.

## When to Use

- A user provides a CSV with media spend, impressions, or marketing channel columns and wants to start modeling
- You need to bootstrap the design phase of a Marketing Mix Model project from scratch
- The user asks to "set up MMM", "plan a media mix model", or "analyze marketing ROI"

## Workflow

1. **Stage 0 — Ensure Core Utilities**: Copies `ml_utils.py` and `mmm_utils.py` into the project `src/` directory if missing
2. **Stage 0b — Ensure BMMM Environment**: Runs `/ensure-bmmm-env` to guarantee the conda/venv runtime is ready
3. **Stage 1 — Profile Data + Load KB Index** (parallel): Profiles the dataset (rows, columns, date range, channel stats, organic proxy detection) and reads the MMM knowledge base index
4. **Stage 2 — Select and Load Knowledge Chunks**: Picks up to 6 relevant chunks from `02_KB_INDEX.yml` by tag matching, plus the three document templates
5. **Stage 3 — Fill All Three Documents Inline**: Writes `problem_brief_mmm.md`, `data_readiness_mmm.md`, and `design_memo_mmm.md` directly (no subagent spawning)
6. **Completion — Self-Assessment + Next Step**: Writes self-assessment feedback, then suggests `/mmm-methodologist` as the next command

## Report Bus Integration

Writes structured artifacts to the report directory:
```python
from ml_utils import save_agent_report
save_agent_report("mmm-methodologist", {
    "status": "completed",
    "artifacts": ["problem_brief_mmm.md", "data_readiness_mmm.md", "design_memo_mmm.md"],
    "next_step": "/mmm-methodologist <project_name>"
})
```

## Full Specification

See `commands/start-mmm-project.md` for the complete workflow.
