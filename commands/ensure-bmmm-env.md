# /ensure-bmmm-env

Ensure the **Bayesian MMM runtime environment** exists at `knowledge_base/mmm/BMMM-env/`.

## Policy

1) If env already exists, verify `pytensor>=2.18` is installed. If not, upgrade: `pip install 'pytensor>=2.18'`
2) Else if `environment.yaml` and/or `requirements.txt` exist, ensure they include `pytensor>=2.18`, then create from them.
3) Else (first run): create seed files with `pytensor>=2.18` pinned, then create the environment.

## PyMC Compatibility (v1.1.0)

Always ensure `pytensor>=2.18` to avoid C compilation failures on macOS ARM and silent backend fallbacks. Seed dependency files must include:
```
pytensor>=2.18
pymc>=5.10
pymc-marketing>=0.7
arviz>=0.17
```

## Execution

```bash
RUNNER=$(command -v py 2>/dev/null && echo py || echo python3)
PYTENSOR_FLAGS_VAL=$([ "$RUNNER" = "py" ] && echo "cxx=" || echo "")
$RUNNER scripts/ensure_bmmm_env.py
```

If the env exists but pytensor is outdated, upgrade it:
```bash
$RUNNER scripts/run_in_env.py --domain mmm --no_ensure -- \
  pip install 'pytensor>=2.18'
```

## Verify

```bash
PYTENSOR_FLAGS="$PYTENSOR_FLAGS_VAL" PYTHONIOENCODING="utf-8" \
  $RUNNER scripts/run_in_env.py --domain mmm --no_ensure -- \
  python -c "import pymc; import pymc_marketing; import pytensor; assert tuple(int(x) for x in pytensor.__version__.split('.')[:2]) >= (2, 18), f'pytensor {pytensor.__version__} < 2.18'; print('ok')"
```

## Platform flags

| Flag | Windows | macOS/Linux |
|---|---|---|
| `PYTENSOR_FLAGS="cxx="` | Required | Not needed |
| `PYTHONIOENCODING="utf-8"` | Required | Harmless |
