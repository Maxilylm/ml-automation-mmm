---
name: mmm-communicate
description: "Convert MMM technical results into a client-ready business narrative using the mmm-communicator agent. Use this whenever the user wants to share MMM findings with stakeholders, even if they just say 'make it client-ready' or 'write the executive summary'."
user_invocable: true
aliases: [mmm communicate, mmm client report, mmm narrative]
extends: ml-automation
---

# MMM Communicate

Transform a completed MMM technical run into a client-ready business narrative. Reads the final report and problem brief, then delegates to the mmm-communicator agent to produce a polished deliverable.

## When to Use

- After `/final-mmm-report` has produced the consolidated technical report
- The user wants a client-facing version of MMM results free of technical jargon
- Stakeholders need a business narrative with ROI insights and budget recommendations

## Workflow

1. **Stage 1 — Resolve Paths**: Determines `project_dir`, reads `LATEST.txt` for `run_id`, sets output to `client_report.md`
2. **Stage 2 — Read Inputs**: Loads `final_report.md` and `problem_brief_mmm.md` (stops with guidance if final report is missing)
3. **Stage 3 — Invoke mmm-communicator Agent**: Spawns the `mmm-communicator` subagent with both documents as context
4. **Stage 4 — Confirm and Summarize**: Verifies `client_report.md` was written and prints a summary

## Report Bus Integration

Writes the client narrative for delivery:
```python
from ml_utils import save_agent_report
save_agent_report("mmm-communicator", {
    "status": "completed",
    "artifact": "client_report.md",
    "audience": "business_stakeholders"
})
```

## Full Specification

See `commands/mmm-communicate.md` for the complete workflow.
