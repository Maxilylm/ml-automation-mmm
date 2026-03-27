---
name: mmm-methodologist
description: "Gate command for MMM methodologist review — scores complexity signals and decides whether full review is needed"
user_invocable: true
aliases: [mmm methodologist, methodologist review, mmm review]
extends: ml-automation
---

# MMM Methodologist Gate

Reads the existing design memo, scores complexity signals (geo dimensions, channel count, calibration evidence, collinearity), and decides whether a full methodologist review is warranted. Routes to `/bmmm-smoke` if not.

## Full Specification

See `commands/mmm-methodologist.md` for the complete workflow.
