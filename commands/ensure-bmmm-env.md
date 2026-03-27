# /ensure-bmmm-env

Ensure the **Bayesian MMM runtime environment** exists at `knowledge_base/mmm/BMMM-env/`.

## Policy

1) If env already exists, use it.
2) Else if `environment.yaml` and/or `requirements.txt` exist, create from them.
3) Else (first run): create seed files, then create the environment.

## Execution

```bash
RUNNER=$(command -v py 2>/dev/null && echo py || echo python3)
PYTENSOR_FLAGS_VAL=$([ "$RUNNER" = "py" ] && echo "cxx=" || echo "")
$RUNNER scripts/ensure_bmmm_env.py
```

## Verify

```bash
PYTENSOR_FLAGS="$PYTENSOR_FLAGS_VAL" PYTHONIOENCODING="utf-8" \
  $RUNNER scripts/run_in_env.py --domain mmm --no_ensure -- \
  python -c "import pymc; import pymc_marketing; print('ok')"
```

## Platform flags

| Flag | Windows | macOS/Linux |
|---|---|---|
| `PYTENSOR_FLAGS="cxx="` | Required | Not needed |
| `PYTHONIOENCODING="utf-8"` | Required | Harmless |
