# MMM Playbook — MMM_Multiplicative_Hierarchical (pymc-marketing)

**Repo**: pymc-marketing fork — Bayesian MMM with geo/brand hierarchy and B2B extensions
**Distilled**: 2026-02-22 | **Framework**: PyMC + PyTensor + NumPyro
**Core entry points**: `mmm_config.yml`, `geo_config.yml`, `pymc_marketing/mmm/mmm.py`, `b2b_src/`

---

## 1. Purpose & Scope

A **Bayesian MMM** built on `pymc-marketing` with three operating modes:

| Mode | Config | When to use |
|------|--------|-------------|
| Standard (single market) | `mmm_config.yml` | One geo, B2C, short sales cycle |
| Multi-dimensional / Geo | `geo_config.yml` | Multiple geos/brands, partial pooling needed |
| B2B extensions | `geo_config.yml` + `b2b_src/` | Pipeline outcomes, visit-to-revenue mapping, long adstock |

The model uses a **log-linear (multiplicative) structure** — targets and channels are log-transformed before fitting. All predictions are in log-scaled space and must be inverse-transformed via `exp()` + `target_scale` for reporting.

---

## 2. Quick-Start (5 Steps)

### Step 1 — Configure (`mmm_config.yml`)

```yaml
data:
  source: "data/your_data.csv"
  columns:
    date_column: "date_week"       # ISO date, weekly cadence
    target_column: "y"             # Revenue / conversions
    channel_columns: ["x1", "x2"] # Spend or visits columns
    control_columns: ["event_1", "event_2", "t"]

model:
  adstock:
    type: "GeometricAdstock"  # or "NoAdstock"
    l_max: 8                  # Max lag weeks
  saturation:
    type: "LogisticSaturation"  # or "NoSaturation"
  seasonality:
    yearly_seasonality: 2     # Fourier terms (2–4)
  log_transformation:
    - "target"
    - "channels"

priors:
  use_spend_share_priors: true
  spend_share_multiplier: 2   # = n_channels

sampling:
  random_seed: 327            # sum(map(ord, "mmm"))
  mcmc:
    chains: 2
    target_accept: 0.85
    nuts_sampler: "numpyro"   # numpyro (fast), nutpie (GPU), pymc (default)
```

### Step 2 — Load config safely

```python
from b2b_src.config_loader import load_and_validate_config, get_channel_config, get_control_config

config = load_and_validate_config("mmm_config.yml")   # Raises ValueError if invalid
date_col   = config.data.columns.date_column
target_col = config.data.columns.target_column
channel_info = get_channel_config(config)   # → {'channel_columns', 'paid_channels', 'spend_mapping'}
control_cols = get_control_config(config)
```

`ConfigDict` supports safe dot-access — missing keys return `None`, not `KeyError`.

### Step 3 — Build and run prior predictive

```python
from pymc_marketing.mmm.mmm import MMM
from pymc_marketing.mmm.components.adstock import GeometricAdstock
from pymc_marketing.mmm.components.saturation import LogisticSaturation

mmm = MMM(
    date_column=date_col,
    channel_columns=channel_info['channel_columns'],
    adstock=GeometricAdstock(l_max=config.model.adstock.l_max),
    saturation=LogisticSaturation(),
    control_columns=control_cols,
)
mmm.build_model(X=df[channel_info['channel_columns'] + control_cols], y=df[target_col])

prior = mmm.sample_prior_predictive(samples=300)
# Inspect prior predictive — must cover observed target range
```

### Step 4 — Fit (MCMC)

```python
import pymc as pm

with mmm.model:
    idata = pm.sample(
        draws=2000,
        tune=1000,
        chains=config.sampling.mcmc.chains,
        target_accept=config.sampling.mcmc.target_accept,
        nuts_sampler=config.sampling.mcmc.nuts_sampler,
        random_seed=config.sampling.random_seed,
    )
mmm.idata = idata
```

For geo models: 4 chains, `target_accept=0.95`, `nuts_sampler="numpyro"`.

### Step 5 — Validate then report

Run convergence checks immediately after sampling (Section 7). Do not produce outputs before passing all convergence gates.

---

## 3. Data Requirements & Column Conventions

### Required columns

| Column | Convention | Notes |
|--------|-----------|-------|
| Date | `date_week` (or configured) | Weekly ISO dates, no gaps, timezone-naive |
| Target | `y` or `NetGMV` | Revenue/conversions; log-transformed internally |
| Channels | `x1`, `x2` … or `Spend_channel_N` | Raw spend **or** visits — not pre-log-transformed |
| Controls | `event_1`, `event_2`, `t` | Binary events + time trend |
| Dimension | `Groups` (geo model) | Geo / brand identifier; auto-detected from data |

### Critical data rules

- **NaN in any channel column = corrupted adstock for all subsequent weeks.** Pre-flight check: `df.isnull().sum()` must be zero for all spend and target columns. Fill missing spend with `0`, not `NaN`.
- **Paid vs unpaid channels**: declare `type: "paid"` for channels with spend data; `type: "unpaid"` for organic/visits-only. Marginal ROAS is calculated only for paid channels.
- **Spend mapping**: when channel column name differs from spend column (visits vs. spend), define `spend_mapping` in config:
  ```yaml
  spend_mapping:
    MV_Paid_1_visits: "MV_Paid_1_Spend"
  ```
- **Minimum data**: 104 weeks per market for stable seasonality. Below 52 weeks: disable seasonality, use strong priors, document limitation.
- **Dimension column**: auto-detected from `['Groups', 'geo', 'brand', 'region', 'market']`. If your column has another name, set `dimension_column` explicitly in config.

---

## 4. Modeling Decisions

### 4.1 Adstock (carryover)

**Default**: `GeometricAdstock(l_max=8)`

```yaml
model:
  adstock:
    type: "GeometricAdstock"
    l_max: 8   # weeks
```

- `l_max` = maximum lag window. Truncates adstock kernel at this lag.
- Prior on `adstock_alpha`: `Beta(alpha=2, beta=5)` → mean ~0.3 (fast decay, suitable for digital).
- For TV/OOH: widen prior to `Beta(3, 3)` → mean ~0.5 (slower decay).
- `NoAdstock`: use only for channels with proven immediate-response (e.g., promotions with known 1-week window).

**Decision by channel type**:

| Channel | `l_max` | Alpha prior | Notes |
|---------|---------|-------------|-------|
| Paid search | 4 | Beta(2, 5) | Fast decay |
| Paid social | 6 | Beta(2, 4) | Moderate |
| Display / video | 8 | Beta(3, 4) | Brand building |
| TV linear | 13 | Beta(3, 3) | Long memory |
| OOH | 8 | Beta(3, 3) | Similar to TV |
| B2B email/events | 8–16 | Beta(3, 2) | Long consideration |

### 4.2 Saturation

**Default**: `LogisticSaturation`

```yaml
model:
  saturation:
    type: "LogisticSaturation"
```

- Logistic: symmetric S-curve. Stable numerically. Default for most channels.
- `NoSaturation` (as in `geo_config.yml` default): use when spend variation is low and saturation cannot be identified. Document this decision.

**Identification rule**: If a channel has fewer than 3 distinct spend levels or CV < 0.05, set `type: "NoSaturation"` and flag channel as "not identified" in the design memo.

### 4.3 Log transformation

The repo applies log(x+1) transforms internally when configured:

```yaml
model:
  log_transformation:
    - "target"    # log(y+1)
    - "channels"  # log(x+1) for each channel
```

**Critical consequence**: predictions from `sample_posterior_predictive(..., original_scale=False)` are in log-scaled space. To convert back:

```python
# CORRECT order (from b2b_src/contributions.py):
mean_log = preds.mean(dim="sample").values
mean_original = np.exp(mean_log)           # Step 1: reverse log
mean_original *= mmm.target_scale          # Step 2: reverse scaling
```

Never apply `exp()` to individual samples then average — this biases estimates upward (Jensen's inequality).

### 4.4 Priors

**Standard model** — use spend-share priors:
```yaml
priors:
  use_spend_share_priors: true
  spend_share_multiplier: 2   # = n_channels
  intercept:
    distribution: "Normal"
    mu: 0.5
    sigma: 0.2
  gamma_control:
    distribution: "Normal"
    mu: 0
    sigma: 0.05
  gamma_fourier:
    distribution: "Laplace"
    mu: 0
    b: 0.2
  likelihood:
    distribution: "Normal"
    sigma:
      distribution: "HalfNormal"
      sigma: 6
```

**Per-channel heterogeneous priors** — use `PerChannelDistributionFactory` (`b2b_src/Prior_upgrade.py`):
```python
from b2b_src.Prior_upgrade import PerChannelDistributionFactory
from pymc_extras.prior import Prior

channel_priors = PerChannelDistributionFactory([
    Prior("HalfNormal", sigma=0.5),   # channel 0 — conservative
    Prior("HalfNormal", sigma=1.0),   # channel 1 — wider
])
```

Run prior predictive checks before sampling. If prior predictive range covers impossible values (e.g., negative revenue), tighten `intercept.sigma` or `likelihood.sigma`.

**Common prior pitfalls:**

| Pitfall | Symptom | Fix |
|---|---|---|
| Too-diffuse channel beta | Posterior beta >> 5; contribution > 100% of revenue | Tighten to `HalfNormal(sigma=0.3)` |
| Normal prior on adstock decay alpha | Negative decay sampled; divergences | Switch to Beta or HalfNormal |
| Flat prior on saturation lam | Saturation at 0 → infinite ROAS | Bound via HalfNormal centered at median normalized spend |
| Over-informative seasonal prior | Seasonality absorbs channel variation | Widen to `Laplace(b=0.3)` or check multicollinearity |
| Sigma_likelihood too tight | R-hat > 1.05 on all params (prior/data conflict) | Run prior predictive first; verify target scale |

### 4.5 Seasonality

```yaml
model:
  seasonality:
    yearly_seasonality: 2   # 2 Fourier pairs = 4 terms
```

- 2 Fourier pairs: adequate for most markets.
- Increase to 4 if residuals show strong seasonal pattern after initial fit.
- Disable (`yearly_seasonality: 0`) if fewer than 52 weeks of data.
- Prior: `Laplace(mu=0, b=0.2)` — sparse prior, prevents over-fitting to noise.

### 4.6 Time-varying effects

```yaml
model:
  time_varying:
    intercept: false  # GP on intercept (expensive)
    media: false      # GP on media betas (very expensive)
```

Keep both `false` by default. Enable only with explicit justification (non-stationary market) and document in design memo. GP sampling cost scales O(T³).

---

## 5. Geo / Multi-Dimensional Models

**Config**: `geo_config.yml` | **Entry**: `geo_model.ipynb`

### Pooling strategy per parameter

```yaml
dimensions:
  pooling:
    default_strategy: "hierarchical"
    pooled_params: ["gamma_control"]        # Controls shared across geos
    unpooled_params: ["adstock_alpha"]      # Adstock fitted per geo
    hierarchical_params: ["saturation_beta", "intercept", "gamma_fourier"]
```

**Saturation beta** — hierarchical (recommended):
```yaml
priors:
  saturation_beta:
    type: "LogNormalPrior"
    mean:
      distribution: "Gamma"
      mu: 0.25
      sigma: 0.10
      dims: ["channel"]           # Hyperprior per channel
    std:
      distribution: "Exponential"
      scale: 0.10
      dims: ["channel"]
    dims: ["channel", "Groups"]   # Posterior varies by channel AND geo
    centered: false               # Non-centered parameterization (required for stability)
```

Always use `centered: false` for hierarchical parameters — centered parameterization causes funnel geometry in NUTS.

**Adstock alpha** — unpooled per geo (conservative default):
```yaml
priors:
  adstock_alpha:
    distribution: "Beta"
    alpha: 2
    beta: 5
    dims: ["Groups", "channel"]   # One alpha per geo × channel
```

**Seasonality** — hierarchical (different pattern per geo):
```yaml
priors:
  gamma_fourier:
    distribution: "Normal"
    mu: 0
    sigma: 0.2
    dims: ["Groups", "fourier_mode"]
```

### Scaling for multi-dimensional models

```yaml
model:
  apply_scaling: true
  scaling:
    channel:
      method: "max"
      dims: []      # Scale across ALL dimensions together
    target:
      method: "max"
      dims: []
```

`dims: []` = global max scaling. This is critical for hierarchical models — per-geo scaling creates inconsistent scales.

### Minimum requirements for pooling

| Markets | Recommended pooling |
|---------|-------------------|
| ≥ 5 | Partial pool (hierarchical) |
| 3–4 | Careful partial pool — inspect sigma_market posterior |
| < 3 | Full pool or separate models |

If `sigma_market` (std of geo offsets) has posterior mass near 0, geos are similar — pooling is effective. If mass is very large (> 1.5 on log scale), geos are too heterogeneous.

### Config loading for geo model

```python
from b2b_src.config_loader import load_and_validate_config, get_channel_config

config = load_and_validate_config("geo_config.yml")
dimension_col = config.data.columns.dimension_column  # "Groups"
channel_info  = get_channel_config(config)
# channel_info['paid_channels'], channel_info['spend_mapping']
```

Dimension column auto-detected from: `['Groups', 'geo', 'brand', 'region', 'market']`. If your column name differs, set `dimension_column` in config explicitly.

---

## 6. Validation Checklist

Run **before sharing any result**. Gate is strict — do not proceed if any check fails.

### Convergence (required)

```python
import arviz as az
summary = az.summary(idata, var_names=["adstock_alpha", "saturation_beta", "saturation_lam",
                                        "intercept", "gamma_control", "gamma_fourier"])
```

| Metric | Threshold | Action if failed |
|--------|-----------|-----------------|
| R-hat | < 1.01 | Increase chains/draws; check identifiability |
| ESS_bulk | > 400 | Increase draws |
| ESS_tail | > 400 | Raise target_accept |
| Divergences | 0 (hard) | Check priors, use non-centered param |
| E-FMI | > 0.2 | Reparameterize |

**Config reference**: `diagnostics.convergence.max_rhat: 1.01`, `min_ess: 400`, `max_divergences: 0` (from `geo_config.yml`).

### Posterior Predictive Checks

```python
ppc = mmm.sample_posterior_predictive(df, extend_idata=False, original_scale=True)
```

- 94% HDI must cover observed target in ≥ 85% of weeks.
- Check per geo for hierarchical models (not just aggregate).
- Residuals: no autocorrelation (Durbin-Watson 1.5–2.5).

### Holdout validation

- Hold out last 8 weeks before final run (12 weeks for B2B / slow-moving targets).
- MAPE on holdout: < 15% direct response, < 25% B2B pipeline.
- ROAS estimate stability: refit with holdout shifted by 4 weeks; ROAS should be within ±20%.

---

## 7. Calibration Protocol (Geo-Lift / Experiment Evidence)

### 7.1 When to Calibrate

Use calibration whenever you have a geo-lift, conversion-lift, or incrementality experiment measuring iROAS for any channel. Calibration is **not optional** when experiment data exists — it is a hard requirement.

**When NOT to calibrate:**
- Experiment ran during an anomalous period (holiday, COVID lockdown, concurrent promo).
- Experiment geo coverage < 10% of total sales volume.
- Multiple channels were co-active in the same experiment arm (unattributable lift).
- Measured iROAS is > 5× the model prior range (investigate data quality first).

### 7.2 Geo-Lift to ROAS Target

```python
# roas_measured = 2.4  (every $1 spent drove $2.40 incremental revenue)
# Sigma recommendation: 20% of point estimate (wider if CI was wide)
roas_sigma = 0.2 * roas_measured   # = 0.48

iROAS_model = pm.Deterministic(
    "iROAS_ch1",
    compute_iROAS(alpha_ch1, adstock_params, saturation_params, spend_ch1)
)
pm.Normal("calibration_ch1", mu=iROAS_model, sigma=roas_sigma, observed=roas_measured)
```

**Sigma guide:**
| Experiment quality | Sigma recommendation |
|---|---|
| Well-powered geo-lift (< 15% CI) | `0.15 × roas_measured` |
| Standard geo-lift | `0.20 × roas_measured` (default) |
| Wide CI or low-coverage experiment | `(upper_CI - lower_CI) / 3.29` (map 99% CI → sigma) |
| Minimum (never be over-confident) | `0.10 × roas_measured` |

### 7.3 Calibration Sanity Check (run after sampling)

- Posterior iROAS mean within 15% of experiment estimate. ✓
- Posterior calibration sigma has NOT collapsed to near-zero (sign of likelihood conflict). ✓
- Channel contribution did not change sign or jump to implausible extreme. ✓
- R-hat on iROAS deterministic < 1.01. ✓

If the calibration likelihood conflicts with the data likelihood (e.g., posterior iROAS drifts far from experiment), do not force calibration — flag it and investigate channel spend data quality.

### 7.4 State Calibration Status in Every Deliverable

```
Channel   | Experiment | Calibrated | Model iROAS | 90% HDI
----------|------------|------------|-------------|----------
Paid Search | Q3 2024 geo-lift | Yes | 3.1x | [2.4x–3.9x]
Social Video | None | No | 1.8x | [0.9x–2.7x]
TV | None | No | 2.2x | [1.1x–3.4x]
```

Never present a single uncalibrated ROAS estimate as a fact. Always annotate calibration status.

---

## 7b. Budget Optimization

### Standard optimization call

```python
from b2b_src.contributions import analyze_revenue_vs_spend_levels

# Step 1: Generate response curves for each channel
curves = analyze_revenue_vs_spend_levels(
    mmm=mmm, data=df, config=config,
    multipliers=[0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0],
    random_seed=327,
)

# Step 2: Use scipy SLSQP to maximise expected revenue given budget constraint
from scipy.optimize import minimize

def neg_revenue(x, curves):
    return -sum(interp_curve(curves, ch, xi) for ch, xi in zip(channels, x))

result = minimize(
    neg_revenue, x0=current_spend, args=(curves,),
    method="SLSQP",
    bounds=[(min_spend[ch], max_spend[ch]) for ch in channels],
    constraints={"type": "eq", "fun": lambda x: x.sum() - total_budget},
)
```

### Required output elements

1. Current vs. recommended allocation (absolute $ and %).
2. Predicted incremental revenue change with 90% HDI.
3. Marginal ROAS at current and recommended spend per channel.
4. Constraints applied (min/max per channel, total budget).
5. Sensitivity table: output at ±10%, ±20% total budget.

### Cap extrapolation

Never optimize beyond **1.5–2× the maximum observed spend** per channel. Response curve extrapolation beyond this range is unreliable. Document the cap in the deliverable.

---

## 8. Contributions & ROAS

All contribution/ROAS functions live in `b2b_src/contributions.py`.

### Get individual contributions

```python
from b2b_src.contributions import get_individual_contributions

contribs = get_individual_contributions(
    mmm=mmm,
    data=df,
    channel_cols=channel_info['channel_columns'],
    control_cols=control_cols,
    random_seed=327,
)
# Returns: {'dates', 'channels', 'controls', 'intercept', 'seasonality'}
```

### Calculate ROAS

```python
from b2b_src.contributions import calculate_roas

roas_results = calculate_roas(
    contributions=contribs,
    data=df,
    channel_cols=channel_info['paid_channels'],
    date_start="2024-01-01",
    date_end="2024-12-31",
    target_column=target_col,
    spend_mapping=channel_info['spend_mapping'],   # visits → spend column
)
# roas_results['roas']         → {'channel': mean_roas}
# roas_results['roas_samples'] → {'channel': array(n_samples)} for uncertainty
```

**ROAS methodology** (from source): total contribution is computed including ALL components (channels + controls + intercept + seasonality) as denominator — ensures contributions sum to 100% of predicted revenue.

### Marginal ROAS (mROAS)

```python
from b2b_src.contributions import calculate_marginal_roas

mroas = calculate_marginal_roas(
    mmm=mmm,
    data=df,
    config=config,
    date_start="2024-01-01",
    date_end="2024-12-31",
    marginal_increase=0.01,   # 1% spend increase
    random_seed=327,
)
# mroas['mroas'] → {'channel': mroas_value}
```

**Key implementation note**: mROAS modifies the **channel visits column** (not the spend column) because the model is fitted on visits. The spend column is used only to compute the incremental spend denominator.

**Important**: mROAS uses mean predictions in log-space → `exp()` → `target_scale`, not individual posterior samples. This avoids Jensen's inequality bias but means mROAS uncertainty is not directly captured in the single-value output.

### Counterfactual / scenario comparison

```python
from b2b_src.contributions import compare_predictions

# Shut down a channel
fig = compare_predictions(mmm, df, shutdown_channels=["x1"], original_scale=True)

# Marginal change
fig = compare_predictions(mmm, df, marginal_changes={"x1": 0.2, "x2": -0.1}, original_scale=True)
```

### Response curves (spend levels)

```python
from b2b_src.contributions import analyze_revenue_vs_spend_levels

curves = analyze_revenue_vs_spend_levels(
    mmm=mmm,
    data=df,
    config=config,
    multipliers=[0.2, 0.4, 0.6, 0.8, 1.0, 2.0, 3.0],
    random_seed=327,
)
# curves['channels'][channel_name]['multipliers'][multiplier]
```

---

## 9. Reporting Standards

- **Always report 90% credible intervals** (HDI), not just point estimates.
- Format: `Channel X: Spend $1.2M → ROAS 2.4x [1.8x–3.1x, 90% HDI]`
- **Baseline sanity check**: intercept + seasonality contribution should be 40–70% of total predicted revenue. If < 30%, flag potential over-attribution.
- **Decomposition sum check**: sum of all component contributions must equal total predicted revenue (mathematical identity — if it doesn't, there is a bug in your contribution calculation).
- **State calibration status** per channel in the deliverable. Never present ROAS without noting whether it is model-estimated-only or calibrated to an experiment.
- **Trace variables to include** in diagnostic plots (from `geo_config.yml`):
  `adstock_alpha`, `gamma_control`, `gamma_fourier`, `intercept_contribution`, `saturation_beta`, `saturation_beta_mean`, `saturation_beta_std`, `saturation_lam`, `y_sigma`.

---

## 10. Anti-Patterns & Pitfalls

| Anti-pattern | Consequence | Fix |
|---|---|---|
| NaN in spend columns | Silent adstock corruption for all future weeks | Pre-flight `df.isnull().sum()` — must be zero; fill with 0 |
| Applying `exp()` per sample then averaging | Jensen's inequality bias — overstates revenue | Average in log-space first, then `exp()` (see Section 4.3) |
| Modifying spend column for mROAS | Wrong — model uses channel (visits) column | Modify channel visits column, use spend column only for incremental spend denominator |
| `centered: true` for hierarchical priors | Funnel geometry → divergences, poor mixing | Always `centered: false` for hierarchical parameters |
| Centered parameterization without checking sigma_market | May not detect over-pooling | Always inspect sigma_market posterior after fitting hierarchical model |
| Using `original_scale=True` for mROAS sampling | Applies exp() inside model, then you apply it again | Use `original_scale=False` + manual `exp()` + `target_scale` for mROAS |
| Fewer than 52 weeks with seasonality enabled | Overfit seasonal pattern, poor OOS | Disable seasonality below 52 weeks |
| Optimizing budget beyond 2× observed spend | Response curve extrapolation unreliable | Cap optimization at 1.5–2× max observed spend |
| Pooling markets with entirely different media mixes | Biases all market estimates | Use unpooled or separate models for structurally different markets |
| Ignoring `type: unpaid` channels in mROAS | Unpaid channels have no spend → mROAS undefined | `calculate_marginal_roas` auto-filters — ensure config marks unpaid channels correctly |

---

## 11. File Reference

| Task | File | Key function |
|------|------|-------------|
| Single-market config | `mmm_config.yml` | Edit directly |
| Geo / multi-market config | `geo_config.yml` | Edit directly |
| Load config safely | `b2b_src/config_loader.py` | `load_and_validate_config()` |
| Get channel / control info | `b2b_src/config_loader.py` | `get_channel_config()`, `get_control_config()` |
| Core MMM class | `pymc_marketing/mmm/mmm.py` | `MMM.__init__()`, `MMM.build_model()` |
| Adstock transforms | `pymc_marketing/mmm/components/adstock.py` | `GeometricAdstock`, `NoAdstock` |
| Saturation transforms | `pymc_marketing/mmm/components/saturation.py` | `LogisticSaturation`, `NoSaturation` |
| Per-channel priors | `b2b_src/Prior_upgrade.py` | `PerChannelDistributionFactory` |
| Contributions | `b2b_src/contributions.py` | `get_individual_contributions()` |
| ROAS | `b2b_src/contributions.py` | `calculate_roas()` |
| Marginal ROAS | `b2b_src/contributions.py` | `calculate_marginal_roas()` |
| Counterfactual | `b2b_src/contributions.py` | `compare_predictions()` |
| Response curves | `b2b_src/contributions.py` | `analyze_revenue_vs_spend_levels()` |
| Multi-dimensional contributions | `multi_src/contributions.py` | (same API as b2b_src) |
| Visualization utilities | `b2b_src/visual_tools.py` | `plot_multidimensional_prior_predictive_by_dim()` |
| Tutorial (single market) | `mmm_tutorial.ipynb` | Full end-to-end reference |
| Tutorial (geo / hierarchical) | `geo_model.ipynb` | Multi-dimensional reference |
| Generate geo data | `gen_geodata.ipynb` | Synthetic data generation |

---

## 12. When Not to Proceed

Stop and escalate if:

- R-hat > 1.05 for any channel parameter after two refit attempts.
- MAPE on holdout > 30% — model is misspecified.
- Baseline contribution < 25% of total — check for data leakage or model error.
- Any spend column has NaN values that cannot be explained and zero-filled.
- mROAS and average ROAS agree directionally but differ by > 3× — check saturation identification.
- Experiment ROAS and model ROAS disagree by > 2× — investigate before sharing results with client.
