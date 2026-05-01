# /train-bmmm

Run a **full BMMM training** for a project using the managed environment runner.

## Usage
- `/train-bmmm <project_name> [run_id]`

## What this does
1. Ensures the `mmm` domain env exists (BMMM-env).
2. Runs the managed **wrapper entrypoint** (`scripts/mmm/build.py`) inside the env.
3. After training completes, run `/final-mmm-report <project_name>` to produce `final_report.md`.

## Token-Safe File Handling Rules

- **Do not read existing output files** just to verify whether they can be overwritten.
- Only open/read files that are **explicit inputs** required to complete the task.

---

### Stage 0: Ensure Core Utilities

Before training, ensure core utilities are available:
1. Check if `ml_utils.py` exists in the project's `src/` directory
2. If missing, scan for the core plugin's copy and copy it to `src/ml_utils.py`
3. Check if `mmm_utils.py` exists in the project's `src/` directory
4. If missing, copy from this plugin's `templates/mmm_utils.py` to `src/mmm_utils.py`

## Platform detection (run once, reuse throughout)

```bash
RUNNER=$(command -v py 2>/dev/null && echo py || echo python3)
PYTENSOR_FLAGS_VAL=$([ "$RUNNER" = "py" ] && echo "cxx=" || echo "")
```

### 1) Ensure the domain env exists

```bash
$RUNNER scripts/ensure_domain_env.py --domain mmm --env_dir ./knowledge_base/mmm/BMMM-env
```

### 2) Run training (MCMC with informative priors — v1.1.0)

**CRITICAL**: The build script MUST use `pm.sample()` with informative priors. Never use `pm.find_MAP()` as the final result — MLE cannot encode domain knowledge and overfits on small marketing datasets.

Required: positive channel coefficients (`HalfNormal`), bounded adstock decay (`Beta`), informative saturation (`Gamma`). See the train-bmmm skill for the full prior specification.

```bash
project="<project_name>"
run_id=""

if [ -z "$run_id" ]; then
  PYTENSOR_FLAGS="$PYTENSOR_FLAGS_VAL" PYTHONIOENCODING="utf-8" \
    $RUNNER scripts/run_in_env.py --domain mmm -- \
    python scripts/mmm/build.py --project_name "$project" 2>&1
else
  PYTENSOR_FLAGS="$PYTENSOR_FLAGS_VAL" PYTHONIOENCODING="utf-8" \
    $RUNNER scripts/run_in_env.py --domain mmm -- \
    python scripts/mmm/build.py --project_name "$project" --run_id "$run_id" 2>&1
fi
```

### 2b) Convergence Check (v1.1.0)

After MCMC completes, verify convergence before proceeding:
```bash
PYTENSOR_FLAGS="$PYTENSOR_FLAGS_VAL" PYTHONIOENCODING="utf-8" \
  $RUNNER scripts/run_in_env.py --domain mmm --no_ensure -- \
  python -c "
import arviz as az, json, sys
idata = az.from_netcdf('$project/outputs/trace.nc')
summary = az.summary(idata)
rhat_ok = (summary['r_hat'] < 1.05).all()
ess_ok = (summary['ess_bulk'] > 400).all()
divs = idata.sample_stats['diverging'].values.sum()
div_ok = divs / idata.sample_stats['diverging'].values.size < 0.05
print(json.dumps({'rhat_ok': bool(rhat_ok), 'ess_ok': bool(ess_ok), 'divergences': int(divs), 'div_ok': bool(div_ok)}))
if not (rhat_ok and ess_ok and div_ok): sys.exit(1)
"
```

If convergence fails: increase `target_accept` (0.95-0.99), tighten priors, check data scaling. Do NOT fall back to MLE.
```

### 3) Write self-assessment (MUST run — even if training failed)

After training completes (pass or fail), write self-assessment to `feedback/mmm/<project_name>/<session_run_id>/self_assessment_train_bmmm.md`.

### 4) Generate the final report

After the build finishes successfully:
- `/final-mmm-report <project_name>`

### 5) Invite the user to share feedback

### 6) If training fails

Common fixes:

| Error | Fix |
|---|---|
| `ModuleNotFoundError: pandas` | Install pandas in env |
| `UnicodeEncodeError` (CP1252) | Ensure `PYTHONIOENCODING=utf-8` |
| `python: command not found` | Use RUNNER from platform detection |
