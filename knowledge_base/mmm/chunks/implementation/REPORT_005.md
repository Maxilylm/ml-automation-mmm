---
id: REPORT_005
title: analyze_revenue_vs_spend_levels — response curves
source: b2b_src/contributions.py
category: reporting
tags: [response_curves, spend_levels, saturation, roas, optimization_input]
---

`analyze_revenue_vs_spend_levels()` generates response curves by sweeping spend multipliers per channel. Primary input for budget optimization.

```python
from b2b_src.contributions import analyze_revenue_vs_spend_levels

curves = analyze_revenue_vs_spend_levels(
    mmm=mmm,
    data=df,
    config=config,
    multipliers=[0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0],
    random_seed=327,
)
```

**Output structure:**
```
curves['channels'][channel_name]['multipliers'][multiplier] → {
    'mean_revenue': float,     # mean predicted revenue at this spend level
    'lower_bound': float,      # HDI lower
    'upper_bound': float,      # HDI upper
    'spend_level': float,      # absolute spend at this multiplier
}
```

**Usage in budget optimization:**
```python
# Extract the response curve as (spend, revenue) pairs per channel
for ch in channel_cols:
    spends   = [curves['channels'][ch]['multipliers'][m]['spend_level'] for m in multipliers]
    revenues = [curves['channels'][ch]['multipliers'][m]['mean_revenue'] for m in multipliers]
    # Use scipy.interpolate.interp1d to get a smooth curve for SLSQP
```

**Extrapolation cap:** Never optimise beyond `2.0` multiplier (2× observed max spend). Response curve is unreliable outside the data range. Cap all optimization upper bounds at `1.5–2.0` multiplier and document this in the deliverable.
