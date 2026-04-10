---
id: PRIOR_006
title: Target scaling in pymc-marketing — prior calibration for max-scaled [0,1] target
source: pymc_marketing/mmm/mmm.py (_compute_scales, _create_scaled_data_variables) — confirmed v0.18.2
category: priors_constraints
tags: [scaling, target_scale, intercept, saturation_beta, prior_calibration, collapse, degenerate_posterior]
---

## Intercept prior selection rule

Use this two-step decision before every model build.

### Step 1 — Pre-flight check (always run, no extra sampling)

```python
y_scaled_mean = float(y_train.mean() / y_train.max())  # in (0, 1]
```

| y_scaled_mean | Decision | Rationale |
|---|---|---|
| >= 0.50 | **Use pymc-marketing default** (omit intercept from model_config) | True intercept is near the centre of the default prior; degenerate mode risk is low |
| 0.20 - 0.49 | **Run prior predictive gate** (Step 2) | Borderline — default may be too wide; verify before committing |
| < 0.20 | **Auto-calibrate immediately** (skip Step 2) | True intercept is far from 0 on the scaled target; default prior will produce degenerate modes |

### Step 2 — Prior predictive gate (borderline zone only)

Build the model with the default, draw prior predictive samples, and check:

```python
mmm.build_model(X_train, y=y_train)
ppc = mmm.sample_prior_predictive(X_train, y=y_train, samples=200, random_seed=42)
target_scale_val = float(mmm.target_scale)
prior_median_raw  = float(np.median(ppc["y"].values) * target_scale_val)
actual_mean_raw   = float(y_train.mean())
ratio = prior_median_raw / actual_mean_raw   # should be in [0.1, 10]
```

- **ratio in [0.1, 10]** -> default is acceptable; proceed to MCMC
- **ratio outside [0.1, 10]** -> switch to auto-calibrated formula below

### Auto-calibrated formula (used when Step 1 or Step 2 flags)

```python
y_scaled_mean         = float(y_train.mean() / y_train.max())
PRIOR_INTERCEPT_MU    = round(y_scaled_mean * 0.5, 3)
PRIOR_INTERCEPT_SIGMA = round(y_scaled_mean * 1.0, 3)
model_config["intercept"] = Prior("Normal", mu=PRIOR_INTERCEPT_MU, sigma=PRIOR_INTERCEPT_SIGMA)
```

**Never use** log(y_mean / y_max) as mu — that is the log-scale formula and will push the intercept
below 0 on a linear max-scaled target (see Anti-patterns below).

---

## pymc-marketing internally max-scales the target (confirmed v0.18.2)

MMM always divides y by max(|y|) before fitting. All priors operate on the resulting
[0, 1] scaled target — not on raw revenue values.

```python
# Inside pymc-marketing (MMM._compute_scales + _create_scaled_data_variables):
target_scale  = max(abs(y_train))          # stored as mmm.target_scale
target_scaled = y_train / target_scale     # used as the likelihood observed variable
# -> target_scaled in [0, 1]; y_scaled_mean = y_train.mean() / y_train.max()
```

Channels are similarly max-scaled per-channel: channel_scaled = channel / max(channel).

---

## Intercept prior — calibration formula

The intercept must be calibrated to y_scaled, not to raw revenue or log(revenue):

```python
y_scaled_mean         = float(y_train.mean() / y_train.max())
PRIOR_INTERCEPT_MU    = round(y_scaled_mean * 0.5, 3)   # assume ~50% of mean revenue is organic baseline
PRIOR_INTERCEPT_SIGMA = round(y_scaled_mean * 1.0, 3)   # allow wide variation; centred correctly

model_config = {
    "intercept": Prior("Normal", mu=PRIOR_INTERCEPT_MU, sigma=PRIOR_INTERCEPT_SIGMA),
    ...
}
```

**Example** (e-commerce dataset, y_scaled_mean = 0.14):
- mu = 0.07, sigma = 0.14
- Prior predictive median approx 3.5M/week (matches observed mean after multiplying by target_scale)

---

## saturation_beta prior — scale constraint

LogisticSaturation channel output: beta * tanh(lam * x_scaled / 2).

With channels at mean x_scaled ~0.10-0.25 and lam ~ Gamma(2,3) (mean=0.67):
tanh(0.67 * 0.15 / 2) ~0.05 — so each channel contributes roughly beta * 0.05.

With 4 channels: total channel contribution ~4 * beta * 0.05 = 0.20 * beta.

For this to match y_scaled_mean ~0.14:

| beta sigma | E[beta] | Expected total contribution | vs y_scaled_mean |
|---|---|---|---|
| 2.0 | 1.60 | 0.32 | 2.3x — over-predicts |
| 0.5 | 0.40 | 0.08 | 0.6x — reasonable |
| 0.3 | 0.24 | 0.05 | 0.4x — conservative |

**Recommendation**: saturation_beta ~ HalfNormal(sigma=0.5). Adjust down to 0.3 for datasets
with very low y_scaled_mean (< 0.10).

---

## Organic proxy absorption effect on the intercept

When ≥ 3 organic proxies are included as controls, they can collectively absorb a meaningful share of the baseline signal. The fitted intercept then models only the *residual* baseline — which may be slightly negative even when the prior was correctly calibrated.

**This is expected behaviour, not a model failure.** The effective baseline is:

```
effective_baseline = intercept_posterior_mean + Σ(gamma_control_posterior_mean × proxy_normalised_mean)
```

A negative fitted intercept is acceptable provided the **effective baseline is positive**. Check this after training:

```python
proxy_contributions = sum(
    gamma_mean * 1.0  # normalised proxy mean ≈ 1.0 by construction (mean-normalised at build time)
    for gamma_mean in gamma_control_posterior_means
)
effective_baseline = intercept_posterior_mean + proxy_contributions
assert effective_baseline > 0, "Baseline is negative — investigate proxy priors"
```

If the effective baseline is negative, tighten organic proxy priors (reduce sigma toward 0.08) or reduce the number of proxies included.

---

## Anti-patterns — degenerate posterior modes

### Default Normal(0, 2) intercept
Places prior mass at intercept in [-4, +4] on a [0,1] target. The sampler finds the
degenerate mode {intercept=0, beta=0, y_sigma->0} — the path of least resistance.
Result: R-hat=4+, ESS=4, MAPE=100%, all parameters at 0.0000.

### Log-scale formula Normal(log(y_mean/y_max), 0.5)
log(mean/max) is negative (e.g., -2.0 for a skewed distribution). On a linear max-scaled
target this pushes intercept far outside [0,1], forcing betas to extreme compensating values.
Converges accidentally by constraining betas to be non-zero, but produces wrong attribution.

### HalfNormal(sigma=2) for saturation_beta
With multiple channels, the sum of prior channel contributions greatly exceeds y_scaled_max=1.
This widens the prior predictive to +-10x the observed range, making NUTS exploration expensive
and increasing risk of degenerate modes.

---

## Prior predictive display after correct scaling

When sample_prior_predictive(X_train, y=y_train, ...) is called,
ppc["y"] is on the [0, 1] scale. Convert to original units for display:

```python
target_scale_val = float(mmm.target_scale)         # set after build_model() via y=y_train
y_prior_scaled   = ppc["y"].values                 # shape (n_dates, n_samples), [0,1]
prior_mean_gbp   = y_prior_scaled.mean() * target_scale_val
prior_p5_gbp     = np.percentile(y_prior_scaled, 5)  * target_scale_val
prior_p95_gbp    = np.percentile(y_prior_scaled, 95) * target_scale_val
```
