# MMM Design Memo

> **Instructions:** This memo is filled by the **mmm-methodologist** agent (or lead analyst) before model build starts. Every decision must have a rationale and a risk. Blank decisions are not allowed — use "TBD: [reason]" if genuinely unknown.

> **Agent scope (v1.0):** This agent is designed for **single-market, national-level MMM** with a single target variable. The following cases are not yet supported by the automated build pipeline and would require a custom build script:
> - Geo-level or regional panel models (hierarchical/partial-pooling across geos)
> - Per-channel saturation mapping
> - Time-varying parameters (Gaussian Process trend)
> - Calibration prior constraints (experiment-informed ROAS)
> - Multiple KPIs / multi-output models
>
> If your project falls into one of these categories, the agent will flag it during design review. You can still proceed — the design memo and methodological recommendations remain valid — but the generated build script will need manual extension. **Feedback on unsupported cases is welcome:** contact the team that built this agent to help prioritise the next version.

**Project:** <!-- project code -->
**Analyst:** <!-- name -->
**Date:** <!-- YYYY-MM-DD -->
**Version:** v1.0

---

## 0. Dataset Scoping

> Filled by `/start-mmm-project` during data profiling. Records pre-modelling judgments that affect model identification and complexity scoring.

| Field | Value |
|---|---|
| Raw dataset type | <!-- Single-brand time series / Panel (N brands) / Panel (N geos) / Panel (brands × geos) --> |
| Rows (raw) | <!-- N rows × M columns --> |
| Granularity (raw → model) | <!-- Daily → Weekly / Weekly (no change) / Monthly (no change) --> |
| Scope filter applied | <!-- None / Brand filter: org=X / Geo filter: territory=Y / Brand + Geo filter --> |
| Scoping confidence | <!-- High: unique match / Medium: judgment-based / Low: ambiguous --> |
| Scoping rationale | <!-- e.g. "selected highest-revenue Beauty brand with Google+Meta across 245 weeks" --> |

---

## 1. Model Variant

| Field | Decision | Rationale |
|---|---|---|
| Model type | <!-- Standard / Geo-hierarchical / B2B --> | |
| KPI (target) | <!-- column name --> | |
| Log-transform target? | <!-- Yes (default) / No --> | |
| Log-transform channels? | <!-- Yes (default) / No --> | |
| Likelihood | <!-- Normal / StudentT --> | StudentT if outliers detected in EDA |
| Dimensions (geo/brand) | <!-- None / column name --> | |

---

## 2. Time Configuration

| Field | Decision | Notes |
|---|---|---|
| Date column | | |
| Granularity | <!-- Weekly (default) --> | |
| Training window | <!-- YYYY-MM-DD to YYYY-MM-DD --> | |
| Holdout window | <!-- Last N weeks; default 8 --> | |
| Known break points | <!-- list dates, or None --> | |

---

## 3. Channel Configuration

**Global saturation:** <!-- LogisticSaturation / NoSaturation --> — <!-- rationale: e.g. "all channels continuous" or "pmax 51% zeros drives NoSaturation globally" -->

> Saturation is a single global choice — pymc-marketing applies one type to all channels.
> Rule: if ANY channel has >50% zero weeks OR CV < 0.05 OR < 3 distinct levels → NoSaturation globally. Otherwise → LogisticSaturation globally.

Fill one row per channel.

| Channel | Input column | Adstock type | l_max | Alpha prior | Notes |
|---|---|---|---|---|---|
| | | Geometric/Weibull/None | | Beta(1,3) | |
| | | | | | |
| | | | | | |
| | | | | | |

**Adstock decision guide** (from playbook §4.1):
- Digital (search, social): Geometric, l_max=8, Beta(1,3)
- TV/OOH: Geometric with wider prior Beta(3,3) or Weibull, l_max=8–13
- B2B events/email: Geometric, l_max=8–16, Beta(3,2)

---

## 4. Control Variables

| Variable | Column | Prior distribution | Rationale |
|---|---|---|---|
| Trend | <!-- t / index --> | Normal(0, 0.1) | Slow linear growth |
| Yearly seasonality | <!-- Fourier terms --> | Laplace(0, 0.2) | Sparse seasonal |
| Promo dummies | <!-- list columns --> | Normal(0, 0.3) | Unknown direction |
| Other | | | |

**Seasonality Fourier pairs:** <!-- 2 (default) / 4 (if strong seasonality in EDA) / 0 (if < 52 weeks) -->

### 4.1 Organic Proxy Variables

Columns remaining after removing paid channels, date, target, and structural variables (org/geo IDs). These enter the model as `gamma_control` regressors and capture organic demand signals not driven by paid media.

<!-- WHEN PROXIES DETECTED: fill table, remove the "none detected" block -->

| Proxy | Column | Rationale | Prior |
|---|---|---|---|
| | | | Normal(0, <!-- gamma_ctrl_sigma -->) |

<!-- WHEN NO PROXIES DETECTED: replace table above with the note below and add row to §10 Risks
> **No organic proxy variables detected.** Organic demand fluctuations (e.g., brand equity, direct intent, owned-channel engagement) will be absorbed into the model baseline, which may inflate or deflate paid channel contribution estimates. Consider sourcing branded search volume, direct traffic, email clicks, or referral sessions before model build. See §10 Risks.
-->

---

## 5. Prior Specifications

### 5.1 Standard priors (shared across channels)

```yaml
# Paste final prior block here after methodologist review
priors:
  use_spend_share_priors: true
  spend_share_multiplier: 2     # = n_channels
  intercept:
    distribution: Normal
    mu: 0.5
    sigma: 0.2
  gamma_control:
    distribution: Normal
    mu: 0
    sigma: 0.05
  gamma_fourier:
    distribution: Laplace
    mu: 0
    b: 0.2
  likelihood:
    distribution: Normal
    sigma:
      distribution: HalfNormal
      sigma: 6
```

### 5.1b Per-control prior calibration

Each control variable must have its own sigma. Fill in this table and use it to populate `PRIOR_GAMMA_CTRL_SIGMA` in the build script.

| Control variable | Type | sigma | Rationale |
|---|---|---|---|
| <!-- e.g., t --> | <!-- trend / organic proxy / event flag / structural break --> | <!-- 0.08 --> | |
| | | | |

> Agent instruction: generate `PRIOR_GAMMA_CTRL_SIGMA` as a dict (not a scalar) with one entry per control column, using the sigmas from this table. See PRIOR_001 for type-to-sigma guidelines.

### 5.1c Intercept prior selection

> Agent instruction: before setting the intercept prior, apply the PRIOR_006 selection rule:
> 1. Compute `y_scaled_mean = y_train.mean() / y_train.max()`
> 2. If >= 0.50: omit intercept from model_config (use pymc-marketing default)
> 3. If 0.20–0.49: run prior predictive gate (see PRIOR_006 Step 2); auto-calibrate if ratio outside [0.1, 10]
> 4. If < 0.20: auto-calibrate immediately: `mu = y_scaled_mean * 0.5`, `sigma = y_scaled_mean * 1.0`

| Field | Value |
|---|---|
| y_scaled_mean (computed) | <!-- fill --> |
| Decision | <!-- Default / Prior predictive gate / Auto-calibrate --> |
| Intercept prior | <!-- pymc-marketing default  OR  Normal(mu=X, sigma=Y) --> |

### 5.2 Per-channel heterogeneous priors (if applicable)

| Channel | Parameter | Distribution | Rationale |
|---|---|---|---|
| <!-- e.g., TV --> | saturation_beta | HalfNormal(sigma=0.3) | Conservative — no experiment data |
| | | | |

### 5.3 Calibration priors (from experiments)

| Channel | Experiment iROAS | Calibration sigma | Implementation |
|---|---|---|---|
| | | 0.2 × iROAS | pm.Normal likelihood penalty |

---

## 6. Hierarchical / Pooling Structure (Geo model only)

| Parameter | Pooling strategy | Rationale |
|---|---|---|
| intercept | Hierarchical (non-centered) | Allow geo baseline differences |
| adstock_alpha | Unpooled per geo | Media mix can differ by market |
| saturation_beta | Hierarchical (non-centered) | Partial pool response curves |
| gamma_control | Pooled | Controls assumed shared |
| gamma_fourier | Hierarchical | Seasonality can differ by geo |

- [ ] `centered: false` confirmed for ALL hierarchical parameters
- [ ] Global max scaling confirmed (`dims: []` in scaling config)
- [ ] sigma_market posterior inspection plan documented

---

## 7. Sampler Configuration

```yaml
sampling:
  random_seed: 327
  mcmc:
    draws: 2000
    tune: 2000
    chains: 4                   # 2 for quick test; 4 for delivery
    target_accept: 0.90         # Raise to 0.95 for geo/hierarchical
    nuts_sampler: "numpyro"     # numpyro (fast) / pymc (default)
```

**Notes:** <!-- any deviations from defaults and why -->

---

## 8. Validation Plan

| Gate | Threshold | Action if failed |
|---|---|---|
| R-hat (all params) | < 1.01 | Increase tune; reparameterize |
| Bulk-ESS | > 400 per chain | More draws |
| Divergences | 0 (< 5 tolerated) | Raise target_accept; check priors |
| In-sample MAPE | < 15% | Inspect residuals by period |
| Holdout MAPE | < 20% (B2B: < 25%) | Check structural breaks |
| Baseline contribution | 30–70% of revenue | If < 30%: check attribution; if > 70%: check channel variation |
| Contribution sum-to-total | Within 1% | Bug in contribution calculation |

**Calibration check:** Posterior iROAS within 15% of experiment estimate for all calibrated channels.

---

## 9. Reporting Outputs Required

- [ ] Channel iROAS: mean + 90% HDI per channel, full period
- [ ] Channel iROAS by quarter / period (if requested)
- [ ] Contribution decomposition: weekly timeseries + aggregate %
- [ ] Response curves: each channel, 0 to 2× max observed spend, 90% HDI
- [ ] Budget optimization: current vs. recommended split, ±10%/±20% sensitivity
- [ ] Calibration status table
- [ ] Validation summary (internal)
- [ ] Client narrative (via mmm-communicator)

---

## 10. Risks & Open Items

| Risk | Severity | Owner | Resolution / Acceptance |
|---|---|---|---|
| | H/M/L | | |
| | | | |

---

## 11. Decisions Log

Track significant changes from initial design.

| Date | Decision changed | Old value | New value | Reason |
|---|---|---|---|---|
| | | | | |

---

## 12. Sign-off

Design memo reviewed and approved to proceed to model build.

| Role | Name | Date |
|---|---|---|
| Lead analyst | | |
| Methodologist review | | |
