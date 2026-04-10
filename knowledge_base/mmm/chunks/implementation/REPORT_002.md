---
id: REPORT_002
title: calculate_roas — ROAS with uncertainty
source: b2b_src/contributions.py
category: reporting
tags: [roas, iroas, hdi, uncertainty, calculate_roas, reporting, spend_mapping]
---

`calculate_roas()` computes incremental ROAS with posterior uncertainty per channel.

```python
from b2b_src.contributions import calculate_roas

roas_results = calculate_roas(
    contributions=contribs,
    data=df,
    channel_cols=channel_info['paid_channels'],     # Only paid channels
    date_start="2024-01-01",
    date_end="2024-12-31",
    target_column=config.data.columns.target_column,
    spend_mapping=channel_info['spend_mapping'],    # visits col → spend col
)
```

**Returns:**
- `roas_results['roas']`: `{channel: mean_roas}` — posterior mean per channel
- `roas_results['roas_samples']`: `{channel: array(n_samples)}` — full distribution for HDI

**Compute 90% HDI:**
```python
import arviz as az
import numpy as np

for ch, samples in roas_results['roas_samples'].items():
    hdi = az.hdi(np.array(samples), hdi_prob=0.90)
    print(f"{ch}: {roas_results['roas'][ch]:.2f}x [90% HDI: {hdi[0]:.2f}x – {hdi[1]:.2f}x]")
```

**spend_mapping:** When model channels are visits/impressions columns but ROAS denominator must be in $spend, provide `spend_mapping = {"visits_col": "spend_col"}`. `calculate_roas()` divides contribution by spend (not visits) automatically.

**Mandatory in all deliverables:** Never report ROAS without HDI. Label as "Incremental ROAS" not just "ROAS".
