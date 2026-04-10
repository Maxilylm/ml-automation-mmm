---
id: VALID_004
title: Data quality pre-flight — NaN and CV checks
source: b2b_src/column_config.py, b2b_src/config_loader.py
category: validation
tags: [data_quality, nan, missing_values, cv, pre_flight, column_config, leakage]
---

**Framework scope:** This chunk requires `b2b_src` (the custom hierarchical framework). For standard pymc-marketing projects without b2b_src, use **PREFLIGHT_001** instead.

Run this pre-flight script on raw data before any model build.

```python
import pandas as pd
import numpy as np

def preflight_check(df, config):
    from b2b_src.config_loader import get_channel_config
    channel_info = get_channel_config(config)
    channel_cols = channel_info['channel_columns']
    target_col   = config.data.columns.target_column

    errors = []

    # 1. NaN check — CRITICAL
    nan_counts = df[channel_cols + [target_col]].isnull().sum()
    if nan_counts.any():
        errors.append(f"NaN in columns: {nan_counts[nan_counts > 0].to_dict()}")

    # 2. Target positivity
    if (df[target_col] <= 0).any():
        errors.append(f"Non-positive target values: {(df[target_col] <= 0).sum()} rows")

    # 3. Low-variation channels (saturation unidentifiable)
    cv = df[channel_cols].std() / (df[channel_cols].mean() + 1e-8)
    low_cv = cv[cv < 0.05]
    if len(low_cv):
        print(f"WARNING — Low CV channels (set NoSaturation): {low_cv.index.tolist()}")

    # 4. Duplicate dates
    if df[config.data.columns.date_column].duplicated().any():
        errors.append("Duplicate dates found")

    if errors:
        raise ValueError("\n".join(errors))
    print("Pre-flight PASSED")
```

**Critical rule:** NaN in any channel column silently corrupts all adstock values for subsequent weeks. Fill with `0` (not interpolation) after confirming zero spend intent with the client.
