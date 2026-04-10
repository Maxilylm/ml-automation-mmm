---
id: VALID_002
title: Holdout validation — MAPE/WAPE benchmarks
source: pymc_marketing/mmm/evaluation.py, pymc_marketing/metrics.py
category: validation
tags: [holdout, mape, wape, backtest, validation, fit_quality, gate]
---

Always reserve a holdout window before fitting. Evaluate on holdout before delivery.

**Standard holdout setup:**
```python
n_holdout = 8    # weeks; B2B: 12 weeks
df_train    = df.iloc[:-n_holdout]
df_holdout  = df.iloc[-n_holdout:]

mmm.build_model(X=df_train[feature_cols], y=df_train["y"])
# ... fit on train ...

holdout_preds = mmm.sample_posterior_predictive(
    df_holdout, original_scale=True, extend_idata=False
)
```

**MAPE computation:**
```python
pred_mean = holdout_preds[mmm.output_var].mean(dim="sample").values
mape = np.mean(np.abs(pred_mean - df_holdout["y"].values) / df_holdout["y"].values)
```

**Delivery gates:**

| Model type | In-sample MAPE | Holdout MAPE |
|---|---|---|
| Direct response (B2C) | < 10% (good), < 15% (acceptable) | < 15% (good), < 20% (acceptable) |
| B2B / pipeline target | < 15% | < 25% |
| Brand / upper funnel | < 20% | < 30% |

**Leakage flag:** If in-sample MAPE << holdout MAPE (gap > 10 pp), check for data leakage (normalization on full dataset, lookahead features).

**Stability test:** Refit with holdout shifted ±4 weeks. If ROAS changes > 20%, flag as unstable.
