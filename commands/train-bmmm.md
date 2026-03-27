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

### 2) Run training (MCMC)

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
