# MMM CORE (always load)

This file is the **minimal always-on knowledge** for the Bayesian MMM agent.

## Default modeling posture

- **Model family**: Bayesian MMM using `pymc-marketing` (`MMM`), log-linear / multiplicative structure (log(y+1), log(x+1) when enabled).
- **Adstock default**: Geometric adstock with weekly lags.
  - Default `l_max = 8` (digital). Use longer lags only when justified (e.g., TV/OOH, B2B long cycle).
- **Saturation default**: Single global choice — pymc-marketing applies one saturation type to ALL channels.
  - If **ANY** channel has >50% zero weeks OR CV < 0.05 OR <3 distinct levels → **NoSaturation globally**. This is a quick summary rule — **SAT_004 is the authoritative rule** for channels with >50% zeros: always apply SAT_004 identifiability criteria (`cv_nonzero` + `n_distinct_nonzero`) to finalise the decision. SAT_004 overrides this threshold.
  - Otherwise → **LogisticSaturation globally**.
  - Channels with >50% zero weeks still get Geometric adstock; flag them in the design memo risks table and mark ROAS as unreliable in outputs.
  - Never assign NoSaturation to some channels and LogisticSaturation to others in the same model.
- **Seasonality**:
  - If ≥ 52 weeks, allow 2 Fourier pairs as a starting point.
  - If < 52 weeks, disable seasonality by default.
- **Scaling**: keep scaling consistent across dimensions for hierarchical models (avoid per-geo scaling unless you explicitly intend it).

## Data contract (hard rules)

- **No NaNs** in target or channel inputs. NaNs in channels can corrupt carryover logic.
- Spend vs visits: if the model is fit on visits but ROAS denominator uses spend, ensure a correct **spend mapping**.
- Weekly cadence, no gaps. Document any imputation.

## Priors (safe defaults)

- Prefer conservative channel priors (avoid overly diffuse media betas).
- Run **prior predictive** before MCMC; tighten priors if priors imply impossible outcomes.

## Inference defaults

- Use NUTS via `numpyro` when available for speed.
- Start with 2 chains for smoke tests; use more chains / higher `target_accept` for geo/hierarchical.

## Reporting rules (must follow)

- Predictions are often in **log space**. Convert back by averaging in log space first, then applying `exp()` and scaling.
- Never present a single uncalibrated ROAS as a fact; always annotate calibration status if experiments exist.

## What to load next

1) Read `02_KB_INDEX.yml`.
2) Select **≤ 8 chunks** by tag/title/summary that match the current task.
3) Open only those chunk files.
4) Only open the full playbook under `playbook/deep_refs/` if explicitly necessary.
