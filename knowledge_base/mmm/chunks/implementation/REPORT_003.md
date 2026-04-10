---
id: REPORT_003
title: calculate_marginal_roas — mROAS implementation note
source: b2b_src/contributions.py
category: reporting
tags: [marginal_roas, mroas, visits_column, spend_mapping, implementation_note]
---

`calculate_marginal_roas()` estimates the incremental return on the next marginal dollar spent per channel.

```python
from b2b_src.contributions import calculate_marginal_roas

mroas = calculate_marginal_roas(
    mmm=mmm,
    data=df,
    config=config,
    date_start="2024-01-01",
    date_end="2024-12-31",
    marginal_increase=0.01,    # 1% increase in spend
    random_seed=327,
)
# mroas['mroas'] → {'channel': mroas_value}
```

**CRITICAL implementation note:** mROAS modifies the **channel visits column** (model input), not the spend column. The spend column is used only to compute the incremental spend denominator for the ROAS ratio. Do not modify the spend column.

**Why:** The model was fitted on visits; modifying visits is a genuine counterfactual. Modifying spend without modifying visits would give zero lift.

**mROAS uses mean predictions** (not individual posterior samples), then applies `exp()` → `target_scale`. This avoids Jensen's inequality bias but means mROAS uncertainty is not directly captured. For uncertainty: run at multiple marginal_increase values and compare.

**Interpretation:** mROAS > 1.0 = channel not yet saturated; mROAS < 1.0 = channel is over-invested at current level. Compare mROAS across channels to identify reallocation opportunities.
