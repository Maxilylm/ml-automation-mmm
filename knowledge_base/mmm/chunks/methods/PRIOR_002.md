---
id: PRIOR_002
title: Per-channel heterogeneous priors — PerChannelDistributionFactory
source: b2b_src/Prior_upgrade.py
category: priors_constraints
tags: [priors, per_channel, heterogeneous, factory, HalfNormal, custom]
---

When channels have different expected contribution sizes, use per-channel priors via `PerChannelDistributionFactory`.

```python
from b2b_src.Prior_upgrade import PerChannelDistributionFactory
from pymc_extras.prior import Prior

# channels = ["paid_search", "paid_social", "tv"]
channel_priors = PerChannelDistributionFactory([
    Prior("HalfNormal", sigma=0.5),   # paid_search — expect moderate contribution
    Prior("HalfNormal", sigma=0.3),   # paid_social — smaller, more conservative
    Prior("HalfNormal", sigma=1.0),   # tv — wider; hard to identify without experiments
])
```

**When to use:**
- One channel has experiment evidence → tighten its prior proportional to measured iROAS.
- Channel with near-constant spend (low variation) → widen prior (let data be agnostic).
- Known brand vs. performance split → different sigma per channel type.

**Relationship to spend_share_priors:** `PerChannelDistributionFactory` overrides `use_spend_share_priors` for the channels specified. Can mix: use spend-share for most channels, override specific channels with stronger priors from experiments.

**Default fallback:** If `PerChannelDistributionFactory` is not used, all channels get identical priors from the YAML block.
