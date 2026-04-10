---
id: ADST_003
title: DelayedAdstock — peak-delayed carryover
source: pymc_marketing/mmm/components/adstock.py
category: transformations
tags: [adstock, delayed, theta, peak_delay, carryover]
---

`DelayedAdstock` adds a `theta` parameter that shifts the peak of the adstock kernel forward in time. Useful when the channel's main effect lands 1–3 weeks after exposure (e.g., video awareness → purchase intent).

**Parameters:** `alpha` (decay rate), `theta` (delay offset in periods).

**Default priors:** `alpha ~ Beta(1, 3)` (fast decay), `theta ~ HalfNormal(sigma=1)` (small delay).

**Instantiation:**
```python
from pymc_marketing.mmm.components.adstock import DelayedAdstock
adstock = DelayedAdstock(l_max=10, priors={
    "alpha": Prior("Beta", alpha=2, beta=3),
    "theta": Prior("HalfNormal", sigma=2),  # allow up to ~4-week delay
})
```

**When to use:** Video/display campaigns with known consideration phase; B2B email with 2–4 week pipeline delay. Prefer `WeibullCDFAdstock` over `DelayedAdstock` for very long channels (TV/OOH ≥ 8 weeks) — Weibull is more numerically stable at large l_max.

**Anti-pattern:** Do not set `theta` prior too wide on short l_max — delayed adstock can push peak beyond l_max, effectively wasting the carryover window.
