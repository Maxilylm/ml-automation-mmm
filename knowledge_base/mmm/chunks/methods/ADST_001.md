---
id: ADST_001
title: GeometricAdstock — instantiation and default prior
source: pymc_marketing/mmm/components/adstock.py
category: transformations
tags: [adstock, geometric, carryover, prior, decay, digital]
---

`GeometricAdstock` is the default carryover transform for digital channels. It wraps `geometric_adstock()` from `transformers.py`.

**Instantiation:**
```python
from pymc_marketing.mmm.components.adstock import GeometricAdstock
adstock = GeometricAdstock(l_max=8)  # 8-week max lag
```

**Default prior:** `alpha ~ Beta(alpha=1, beta=3)` — mean ≈ 0.25, right-skewed toward fast decay. Suitable for paid search and social where effect mostly lands within 1–3 weeks.

**Key parameters:**
- `l_max` (required): maximum lag window in periods. Set 4–6 for digital, 8–13 for TV/OOH.
- `normalize` (default True): normalises kernel weights to sum to 1. Keep True to preserve spend scale.
- `mode` (default After): convolution mode; keep default.

**Prior customisation:**
```python
from pymc_extras.prior import Prior
adstock = GeometricAdstock(l_max=8, priors={"alpha": Prior("Beta", alpha=2, beta=3)})
# Wider prior (mean ≈ 0.4) for slower-decaying channels like TV
```
