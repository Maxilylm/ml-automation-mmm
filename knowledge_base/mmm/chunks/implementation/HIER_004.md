---
id: HIER_004
title: Data contract — column_config and channel type declaration
source: b2b_src/column_config.py, b2b_src/config_loader.py
category: core_modeling
tags: [data_contract, column_config, paid_channels, spend_mapping, unpaid, schema]
---

`column_config.py` is the canonical schema definition. Populate it first on every new project before writing any code.

**Channel type declaration:**
```yaml
channel_columns:
  - name: paid_search
    type: paid                           # Has $ spend data
    spend_column: "Spend_PaidSearch"     # Maps visits/impressions → spend
  - name: organic_search_visits
    type: unpaid                         # No spend — cannot compute mROAS
    spend_column: null
  - name: tv_grps
    type: paid
    spend_column: "Spend_TV"
```

**Why this matters:**
- `calculate_roas()` and `calculate_marginal_roas()` auto-filter to `paid_channels` only — unpaid channels have no spend denominator.
- `spend_mapping` tells ROAS functions which spend column to use when model input is visits/impressions.
- Without correct `type` declaration, ROAS calculations silently use wrong columns.

**Validation at load time:**
```python
from b2b_src.config_loader import get_channel_config
channel_info = get_channel_config(config)
print("Paid channels:", channel_info['paid_channels'])
print("Spend mapping:", channel_info['spend_mapping'])
# Verify these match the actual data columns before fitting
```
