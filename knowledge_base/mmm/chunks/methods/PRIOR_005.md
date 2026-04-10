---
id: PRIOR_005
title: Config file structure — mmm_config.yml reference
source: mmm_config.yml, b2b_src/config_loader.py
category: priors_constraints
tags: [config, yaml, mmm_config, channels, sampler, data_contract]
---

**Minimal `mmm_config.yml` structure:**
```yaml
data:
  source: "data/your_data.csv"
  columns:
    date_column: "date_week"       # ISO date, weekly cadence
    target_column: "y"             # Revenue / conversions (positive)
    channel_columns: ["x1", "x2"] # Spend or visits columns
    control_columns: ["t", "event_1"]

model:
  adstock:
    type: "GeometricAdstock"
    l_max: 8
  saturation:
    type: "LogisticSaturation"
  seasonality:
    yearly_seasonality: 2
  log_transformation:
    - "target"
    - "channels"

priors:
  use_spend_share_priors: true
  spend_share_multiplier: 2

sampling:
  random_seed: 327
  mcmc:
    chains: 4
    target_accept: 0.90
    nuts_sampler: "numpyro"
```

**Load with validation:**
```python
from b2b_src.config_loader import load_and_validate_config, get_channel_config
config = load_and_validate_config("mmm_config.yml")  # Raises ValueError on invalid
channel_info = get_channel_config(config)
# → {'channel_columns', 'paid_channels', 'spend_mapping'}
```

`ConfigDict` supports safe dot-access: `config.data.columns.date_column`. Missing keys return `None`, not `KeyError`.
