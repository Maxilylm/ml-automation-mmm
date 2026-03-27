# /final-mmm-report

Create (or update) a human-readable **final report** for an MMM project.

## Usage

/final-mmm-report <project_name> [--domain mmm] [--run_id <run_id>]

## Utilities Check

If `ml_utils.py` is not present in `src/`, copy it from the core plugin's templates directory.

## What to do

1. Resolve paths:
   - `project_dir = reports/<domain>/<project_name>/`
   - Determine `run_id` from arg or `LATEST.txt`
   - `out_file = reports/<domain>/<project_name>/<run_id>/final_report.md`

2. Collect inputs (if they exist):
   - `problem_brief_mmm.md` from `project_dir`
   - `design_memo_mmm.md` from `project_dir`
   - Validation report from `reports_dir`

3. Write `final_report.md` with structure:
   - Title + project metadata
   - Executive summary (5–10 bullets)
   - Data readiness + key decisions
   - Model spec (variant, priors, sampler settings)
   - Results summary (convergence, fit quality)
   - Artifacts & file pointers
   - Open items / next steps

4. Never run MCMC here. This command is **report-only**.

## Output

- `reports/<domain>/<project_name>/<run_id>/final_report.md`
