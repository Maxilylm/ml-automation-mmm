---
id: UTIL_003
title: Promo confounding — detection and mitigation
source: playbook §8, MMM_PLAYBOOK.md
category: validation
tags: [promo, confounding, event, dummy, attribution, pitfall]
---

Promotion periods inflate revenue. Without promo dummy variables, media channels in those weeks absorb the promo effect, overstating their ROAS.

**Detection:**
```python
# Step 1: Check if promo periods have abnormal residuals
residuals = df["y"].values - model_mean_predictions
promo_periods = df["event_promo"] == 1
print("Mean residual during promos:", residuals[promo_periods].mean())
print("Mean residual outside promos:", residuals[~promo_periods].mean())
# Large difference → promo not fully captured by current controls
```

**Mitigation:**
1. Add explicit binary dummy for each promo/event week: `event_promo_q4_sale`, `event_product_launch`.
2. Use `control_columns` in the model config — the model absorbs the promo effect through `gamma_control`.
3. If promo magnitude is unknown, use `Normal(0, 0.3)` prior on promo coefficient (allows both positive and negative).

**Sensitivity test (after adding promo dummy):**
```python
# Re-run model with and without promo dummy
# Compare channel ROAS — if TV ROAS drops by > 20% when promo dummy is added,
# the previous model had promo confounding TV.
```

**Document clearly:** State which promo events were included as controls. List any major events NOT included and note the potential upward bias in co-active channel ROAS estimates.
