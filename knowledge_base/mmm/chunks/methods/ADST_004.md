---
id: ADST_004
title: NoAdstock — when to skip carryover
source: pymc_marketing/mmm/components/adstock.py
category: transformations
tags: [adstock, no_adstock, pitfall, identification]
---

`NoAdstock` passes spend through unchanged. Use only when:
1. Channel has a proven immediate-response window (e.g., same-week promotional coupons).
2. Spend variation is so low (CV < 0.05) that adstock cannot be identified — forcing a kernel will absorb noise.
3. You need a fast baseline model before adding transforms progressively.

```python
from pymc_marketing.mmm.components.adstock import NoAdstock
adstock = NoAdstock(l_max=1)  # l_max still required even when unused
```

**Pitfall:** Using `NoAdstock` for brand channels (TV, OOH) severely underestimates long-run channel value. Always document the decision and flag ROAS estimates as "lower-bound" when adstock is skipped for brand channels.

**Identification check before choosing:**
```python
# Coefficient of variation per channel
cv = df[channel_cols].std() / df[channel_cols].mean()
print(cv[cv < 0.05])  # Channels that cannot identify adstock
```
