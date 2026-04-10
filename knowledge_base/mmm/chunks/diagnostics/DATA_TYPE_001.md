---
id: DATA_TYPE_001
title: Time-series vs. cross-sectional detection — early exit rules
source: benchmark validation 2026-03-07 (advertising_islr blocked analysis)
category: validation
tags: [data_type, time_series, cross_sectional, date_column, early_exit, pre_flight]
---

Standard Bayesian MMM (pymc-marketing) requires **time-series data**. Cross-sectional datasets (one row per market/region, no temporal ordering) cannot support adstock or seasonality and must be blocked early.

**Detection (run before any project document generation):**
```python
import pandas as pd

def detect_data_type(df):
    # Check for any date-like column
    date_candidates = [c for c in df.columns
                       if any(kw in c.lower() for kw in ['date', 'week', 'month', 'time', 'period', 'day'])]
    if not date_candidates:
        return "CROSS_SECTIONAL"

    # Try parsing
    for col in date_candidates:
        try:
            parsed = pd.to_datetime(df[col])
            n_unique = parsed.nunique()
            if n_unique >= 0.5 * len(df):  # most rows have distinct dates
                return "TIME_SERIES", col
        except Exception:
            continue

    return "CROSS_SECTIONAL"
```

**Decision rules for `/start-mmm-project`:**

| Result | Action |
|---|---|
| `TIME_SERIES` with ≥ 52 unique weeks | Proceed normally |
| `TIME_SERIES` with < 52 weeks | Proceed with warnings (disable seasonality) |
| `CROSS_SECTIONAL` | **Abort immediately** — do not generate project docs |

**Early exit message (cross-sectional):**
```
DATASET NOT SUITABLE FOR BAYESIAN MMM

Reason: No date/time column detected. pymc-marketing MMM requires time-series data
for adstock (carryover) and seasonality estimation.

This dataset appears to be cross-sectional (one row per market/unit).

Alternative approaches:
  - OLS regression: channel coefficients without uncertainty or carryover
  - Bayesian linear regression (PyMC): channel posteriors + HDI, no adstock
  - Saturation curves only: cross-sectional diminishing returns (no temporal component)

Pipeline aborted. No project documents generated.
```

**Why not write project docs first?** Writing problem_brief + data_readiness + design_memo for a dataset that cannot train wastes time and creates misleading artifacts. The date check takes < 1 second and should gate all downstream work.
