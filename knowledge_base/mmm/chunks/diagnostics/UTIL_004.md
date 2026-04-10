---
id: UTIL_004
title: Escalation rules — when to stop and escalate
source: MMM_PLAYBOOK.md §12
category: validation
tags: [escalation, gate, convergence, mape, experiment_conflict, stop]
---

**Stop and escalate (do NOT proceed alone) when:**

| Condition | Action |
|---|---|
| R-hat > 1.05 after two full refit attempts | Escalate — fundamental model or data issue |
| Holdout MAPE > 25% (B2C) or > 35% (B2B) after two iterations | Escalate — model misspecified |
| Divergence count > 50 with no improvement from reparameterisation | Escalate |
| Any channel contribution is negative in final model | Escalate — contribution calculation bug |
| Experiment ROAS conflicts with model ROAS by > 2× | Escalate — investigate data before sharing results |
| Client data has < 52 weeks of observations | Flag upfront — MMM is underpowered; document limitations prominently |
| Spend data has structural break with no counterfactual control | Escalate — model cannot isolate media from break effect |

**Do NOT proceed when:**
- Channel spend columns cannot be confirmed to map to the correct campaigns.
- Target variable definition changes mid-project.
- Holdout period overlaps with a known major anomaly and no counterfactual exists.
- Client requests point-estimate ROAS without uncertainty — push back and report HDI.

**When escalating:** Document the specific failure, what was tried, and what data/decision is needed to unblock. Never silently deliver results that fail a gate.
