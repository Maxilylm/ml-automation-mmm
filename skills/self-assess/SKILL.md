---
name: self-assess
description: "Aggregate self-assessment feedback files across MMM runs and surface recurring patterns as improvement recommendations. Use this whenever you want to review how past MMM runs performed, even if the user just says 'how are we doing' or 'review past runs'."
user_invocable: true
aliases: [self assess, review feedback, mmm feedback]
extends: spark
---

# Self-Assessment Aggregator

Reads all self-assessment files from `feedback/<domain>/`, aggregates signals across runs, and produces a prioritized improvement report with recurring patterns and actionable recommendations.

## When to Use

- After several MMM runs have accumulated feedback and you want to identify improvement areas
- The user asks to "review feedback", "check quality trends", or "what should we improve"
- As a periodic health check on the MMM pipeline's self-reported performance

## Workflow

1. **Stage 1 — Read Feedback Files**: Globs `feedback/<domain>/**/*.md`, capped at the 20 most recent files for token safety
2. **Stage 2 — Aggregate by Dimension**: Groups findings across 5 dimensions: KB Coverage Gaps, Instruction Ambiguity, Execution Determinism, Data Edge Cases, Workflow Efficiency
3. **Stage 3 — Surface Recurring Patterns**: Flags any pattern appearing in 2+ runs as recurring
4. **Stage 4 — Produce Recommendations**: Prioritizes as High (3+ runs or any failure), Medium (2 runs with warnings), Low (1 run with warnings)

## Report Bus Integration

Writes aggregated assessment for continuous improvement:
```python
from ml_utils import save_agent_report
save_agent_report("mmm-methodologist", {
    "status": "completed",
    "dimensions_assessed": 5,
    "recurring_patterns": [...],
    "recommendations": [{"priority": "high", "action": "..."}]
})
```

## Full Specification

See `commands/self-assess.md` for the complete workflow.
