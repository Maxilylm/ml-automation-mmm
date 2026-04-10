# MMM Router Rules (always load)

These rules control **what the agent loads** to prevent token blowups.

## Hard constraints

- **Index-first**: decide what to open using `02_KB_INDEX.yml`. Do not open chunk files to “see what’s inside”.
- **Hard cap**: open at most **10** chunk files. Default target is **6–8**.
- **No directory scans**: do not scan `chunks/`, `docs/`, `reports/`, or `projects/`.
- **Playbook is deep reference**: do not open `playbook/deep_refs/MMM_PLAYBOOK.md` unless explicitly needed.

## Task → tag routing

### Start / bootstrap project artifacts (/start-mmm-project)
Load up to 8 chunks matching tags:
- data_contract, config, priors, adstock, saturation, log_transform, scaling, validation

### Fit / sampling (/train-bmmm)
Load up to 6 chunks matching tags:
- sampling, nuts, target_accept, divergences, hierarchical (if geo), prior_predictive

### Diagnostics / validation
Load up to 6 chunks matching tags:
- rhat, ess, divergences, ppc, holdout, backtest, residuals

### ROAS / contributions
Load up to 6 chunks matching tags:
- contributions, roas, mroas, spend_mapping, jensen_bias, counterfactual

### Calibration (geo-lift / experiments)
Load up to 6 chunks matching tags:
- calibration, iroas, likelihood, sigma, experiment

## Selection procedure

1) From `02_KB_INDEX.yml`, choose chunk IDs with best tag overlap.
2) Prefer chunks with the most direct `use_when`.
3) Open only the selected chunk paths.
