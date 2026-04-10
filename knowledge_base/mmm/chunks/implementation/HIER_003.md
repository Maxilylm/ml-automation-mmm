---
id: HIER_003
title: Collinearity — diagnosis and mitigation
source: b2b_src/column_config.py, playbook §8
category: core_modeling
tags: [collinearity, correlation, identification, pitfall, channels, priors]
---

High correlation between channel spend columns (r > 0.8) means the model cannot separate their individual effects. This is a fundamental identification problem.

**Diagnosis:**
```python
import pandas as pd
corr = df[channel_cols].corr()
high_corr = (corr.abs() > 0.85) & (corr != 1.0)
if high_corr.any().any():
    print("Highly correlated channels:")
    print(corr[high_corr].dropna(how="all").dropna(axis=1, how="all"))
```

**Mitigation options (in order of preference):**

1. **Merge channels into a single aggregate** (e.g., "brand media" = TV + OOH if always co-active). Simplest fix; loses channel-level insight.

2. **Use strong informative priors** to resolve ambiguity. If experiments exist for one channel, tighten its prior; let the other be residual. Document clearly.

3. **Separate estimation periods:** If channels have different active periods, model them in different time windows.

4. **Accept and document:** Report aggregate "combined channel" ROAS with a note that individual ROAS estimates are unreliable due to collinearity. Recommend future experiments.

**Anti-pattern:** Running the model with r > 0.8 channels and presenting separate ROAS without caveat. The wide HDI will signal the problem, but clients may not notice without explicit communication.
