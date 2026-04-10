---
id: PREFLIGHT_001
title: Standard data pre-flight — pure pandas checks
source: standard MMM practice
category: validation
tags: [data_quality, nan, missing_values, cv, zero_rate, pre_flight, date_column, collinearity]
---

Run before any model build. No custom framework required — pure pandas only.

```python
import pandas as pd
import numpy as np

def mmm_preflight(df, date_col, channel_cols, target_col):
    issues = []

    # 1. Date column check
    if date_col not in df.columns:
        raise ValueError(f"FATAL: No date column '{date_col}'. Dataset is cross-sectional — standard MMM cannot run.")
    try:
        df[date_col] = pd.to_datetime(df[date_col])
    except Exception:
        issues.append(f"Date column '{date_col}' cannot be parsed as datetime.")

    # 2. Duplicate dates
    if df[date_col].duplicated().any():
        issues.append(f"Duplicate dates: {df[date_col].duplicated().sum()} rows")

    # 3. NaN check — CRITICAL (corrupts adstock carryover)
    nan_counts = df[channel_cols + [target_col]].isnull().sum()
    if nan_counts.any():
        issues.append(f"NaN in columns: {nan_counts[nan_counts > 0].to_dict()}")

    # 4. Target positivity
    if (df[target_col] <= 0).any():
        issues.append(f"Non-positive target: {(df[target_col] <= 0).sum()} rows")

    # 5. CV check — saturation identification
    cv = df[channel_cols].std() / (df[channel_cols].mean().replace(0, np.nan))
    low_cv = cv[cv < 0.05].index.tolist()
    if low_cv:
        print(f"WARNING — Low CV (< 0.05), use NoSaturation: {low_cv}")

    # 6. Zero-rate check — burst channel detection
    zero_rate = (df[channel_cols] == 0).mean()
    burst = zero_rate[zero_rate > 0.30].index.tolist()
    high_zero = zero_rate[zero_rate > 0.50].index.tolist()
    if high_zero:
        print(f"WARNING — >50% zero weeks, force NoSaturation: {high_zero}")
    elif burst:
        print(f"WARNING — >30% zero weeks, prefer NoSaturation: {burst}")

    # 7. Collinearity (optional but recommended for 5+ channels)
    corr = df[channel_cols].corr()
    high_corr = [(c1, c2, round(corr.loc[c1, c2], 2))
                 for i, c1 in enumerate(channel_cols)
                 for c2 in channel_cols[i+1:]
                 if abs(corr.loc[c1, c2]) > 0.8]
    if high_corr:
        print(f"WARNING — High channel correlation (> 0.8): {high_corr}")

    if issues:
        raise ValueError("Pre-flight FAILED:\n" + "\n".join(issues))
    print(f"Pre-flight PASSED — {len(df)} rows, {len(channel_cols)} channels")
```

**Critical rules:**
- NaN in any channel column silently corrupts all adstock values for subsequent weeks. Fill with `0` (not interpolation) after confirming zero-spend intent.
- Zero-rate > 50% → NoSaturation (see SAT_004).
- Low CV (< 0.05) → NoSaturation (see SAT_001).
