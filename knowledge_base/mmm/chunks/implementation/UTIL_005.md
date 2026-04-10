---
id: UTIL_005
title: YAML config loading — build_from_yml pattern
source: pymc_marketing/mmm/builders/yaml.py, data/config_files/basic_model.yml
category: core_modeling
tags: [yaml, config, build_from_yml, adstock, saturation, serialization]
---

The model can be fully specified from YAML — no Python class references required.

```python
from pymc_marketing.mmm import MMM

mmm = MMM.build_from_file("data/config_files/basic_model.yml")
```

**YAML structure (basic_model.yml):**
```yaml
model_config:
  adstock:
    lookup_name: geometric
    l_max: 8
    priors:
      alpha:
        dist: Beta
        kwargs: {alpha: 1, beta: 3}
  saturation:
    lookup_name: logistic
    priors:
      lam:
        dist: Gamma
        kwargs: {alpha: 3, beta: 1}
      beta:
        dist: HalfNormal
        kwargs: {sigma: 2}
  yearly_seasonality: 2

sampler_config:
  draws: 2000
  tune: 2000
  chains: 4
  target_accept: 0.9
  nuts_sampler: numpyro
```

**Serialisation roundtrip (save and reload model config):**
```python
config_dict = mmm.model_config
import json; json.dumps(config_dict)  # Must be serialisable
# Reload:
mmm2 = MMM(**config_dict)
```

**adstock/saturation lookup names** (use these in YAML): `geometric`, `delayed`, `weibull_pdf`, `weibull_cdf`, `no_adstock`, `logistic`, `hill`, `michaelis_menten`, `tanh`, `root`, `no_saturation`.
