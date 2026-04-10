---
id: HIER_001
title: Geo/multi-dimensional model — MMM instantiation
source: pymc_marketing/mmm/multidimensional.py, geo_config.yml
category: core_modeling
tags: [geo, multi_dimensional, hierarchical, dims, pooling, entry_point]
---

For multi-market (geo or brand) models, use the multi-dimensional `MMM` from `pymc_marketing.mmm.multidimensional`.

```python
from pymc_marketing.mmm.multidimensional import MMM as MultiMMM
from pymc_marketing.mmm import GeometricAdstock, LogisticSaturation

mmm = MultiMMM(
    date_column="date_week",
    dims=("Groups",),              # The dimension column name
    channel_columns=["x1", "x2"],
    target_column="y",
    adstock=GeometricAdstock(l_max=8),
    saturation=LogisticSaturation(),
    control_columns=["t"],
)

# df must have a "Groups" column with geo/brand labels
mmm.fit(df[feature_cols + ["Groups"]], df["y"])
```

**Dimension auto-detection:** The model auto-detects geo/brand columns from: `['Groups', 'geo', 'brand', 'region', 'market']`. If your column has a different name, pass it explicitly as `dims=("your_col",)`.

**Data format:** Long format — one row per week × geo. All geos must span the same date range (fill with 0 spend if a geo had no media in some weeks).

**Load geo config:**
```python
from b2b_src.config_loader import load_and_validate_config
config = load_and_validate_config("geo_config.yml")
dimension_col = config.data.columns.dimension_column  # "Groups"
```
