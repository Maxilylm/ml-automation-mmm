# /bmmm-smoke

Run a **fast smoke test** for the BMMM toolchain **without long MCMC sampling**.

## What this does
- Ensures the `mmm` domain environment exists (BMMM-env).
- Verifies core imports (`pymc`, `pymc_marketing`, `arviz`, etc.).
- Runs a tiny PyMC model with very small draws/chains to confirm the sampler can start.
- Optionally checks a CSV dataset has expected columns.

## Usage
- `/bmmm-smoke`
- `/bmmm-smoke path/to/mmm_dataset.csv`

## Utilities Check

If `ml_utils.py` is not present in `src/`, copy it from the core plugin's templates directory.

## Platform detection

```bash
RUNNER=$(command -v py 2>/dev/null && echo py || echo python3)
PYTENSOR_FLAGS_VAL=$([ "$RUNNER" = "py" ] && echo "cxx=" || echo "")
```

### 1) Ensure the domain env exists

```bash
$RUNNER scripts/ensure_domain_env.py --domain mmm --env_dir ./knowledge_base/mmm/BMMM-env
```

### 2) Imports check inside the env

```bash
PYTENSOR_FLAGS="$PYTENSOR_FLAGS_VAL" PYTHONIOENCODING="utf-8" \
  $RUNNER scripts/run_in_env.py --domain mmm --no_ensure -- \
  python -c "import pymc, pymc_marketing, arviz, numpy; print('imports: OK')"
```

### 3) Tiny sampler check

Write a temp script, run it, delete it:

```bash
cat > /tmp/_bmmm_smoke.py << 'EOF'
import pymc as pm
import numpy as np
rng = np.random.default_rng(0)
y = rng.normal(size=50)
with pm.Model():
    mu = pm.Normal("mu", 0, 1)
    sigma = pm.HalfNormal("sigma", 1)
    pm.Normal("obs", mu, sigma, observed=y)
    idata = pm.sample(draws=30, tune=30, chains=1, cores=1,
                      progressbar=False, compute_convergence_checks=False,
                      random_seed=0)
print("tiny-sample: OK")
EOF
PYTENSOR_FLAGS="$PYTENSOR_FLAGS_VAL" PYTHONIOENCODING="utf-8" \
  $RUNNER scripts/run_in_env.py --domain mmm --no_ensure -- python /tmp/_bmmm_smoke.py
rm /tmp/_bmmm_smoke.py
```

### 4) Optional: quick CSV sanity check

### 5) Report back

Summarize: env location, import status, tiny-sampler status, dataset summary.
