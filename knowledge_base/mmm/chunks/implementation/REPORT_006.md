---
id: REPORT_006
title: Reporting standards — ROAS table format and HDI requirement
source: pymc_marketing/mmm/base.py, delivery_summary_mmm.md
category: reporting
tags: [reporting, hdi, roas_table, deliverable_standards, calibration_status]
---

**Mandatory ROAS table format for all deliverables:**

```
Channel      | iROAS | 90% HDI          | Calibrated? | Interpretation
-------------|-------|------------------|-------------|----------------------------------
Paid Search  | 3.2x  | [2.5x – 4.1x]   | Yes (Q3 exp)| High confidence; above 1.0x break-even
Social Video | 1.8x  | [0.9x – 2.7x]   | No          | Moderate; wide CI — experiment recommended
TV           | 2.1x  | [1.1x – 3.4x]   | No          | Positive but uncertain
```

**Non-negotiable standards:**
1. **Always 90% HDI** — never just point estimates.
2. **Label "Incremental ROAS"** — not "ROAS" alone (prevents confusion with blended ROAS).
3. **Calibration status column** — every row must state whether an experiment was used.
4. **Break-even reference** — note `1.0x` break-even or the client-specific cost-margin adjusted threshold.

**Baseline sanity narrative:**
```
Baseline (organic + seasonality + trend): 52% of total modelled revenue.
✓ Within expected 30–70% range — channel attribution is plausible.
```

**Decomposition sum-to-total sentence (include in every report):**
```
Sum of all component contributions = [X]% of total modelled revenue.
✓ Within 1% tolerance — attribution is internally consistent.
```
