# /mmm-communicate

Convert a completed MMM technical run into a **client-ready business narrative** using the `mmm-communicator` agent.

## Usage

```
/mmm-communicate <project_name> [--domain mmm] [--run_id <run_id>]
```

## Workflow

### Step 1 — Resolve paths

```
domain       = mmm  (default)
project_dir  = reports/<domain>/<project_name>/
run_id       = --run_id arg  OR  read LATEST.txt
run_dir      = reports/<domain>/<project_name>/<run_id>/
out_file     = reports/<domain>/<project_name>/<run_id>/client_report.md
```

### Step 2 — Read inputs (both required)

1. `reports/<domain>/<project_name>/<run_id>/final_report.md`
2. `reports/<domain>/<project_name>/problem_brief_mmm.md`

If `final_report.md` is missing, stop and tell the user to run `/final-mmm-report`.

### Step 3 — Invoke mmm-communicator agent

Spawn the `mmm-communicator` agent with the content of both files.

### Step 4 — Confirm and summarise

## Output

- `reports/<domain>/<project_name>/<run_id>/client_report.md`
