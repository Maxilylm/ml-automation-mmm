# /start-mmm-project

This command initializes the **standard MMM project artifacts** using the built-in MMM knowledge pack, generating the core project documents required to begin a Marketing Mix Modeling analysis.

---

## Usage

/start-mmm-project <data_file> <domain> <project_name>

---

## Outputs (created/updated)

- reports/mmm/{{project_name}}/{{session_run_id}}/problem_brief_mmm.md
- reports/mmm/{{project_name}}/{{session_run_id}}/data_readiness_mmm.md
- reports/mmm/{{project_name}}/{{session_run_id}}/design_memo_mmm.md
- reports/mmm/{{project_name}}/LATEST.txt  (points to session_run_id)

---

## Token / cost guardrails (MUST FOLLOW)

- Do **not** scan directories.
- Do **not** read `reports/**` or `projects/**` unless the user explicitly asks.
- **Never open existing destination files** under `reports/mmm/{{project_name}}/{{session_run_id}}/` "to check before overwriting".
  - If the three output files already exist, **overwrite them blindly** but **do not read them**.
- **Do NOT spawn the mmm-methodologist agent** — fill all three documents inline using context already loaded in steps 1–2. Spawning a subagent re-reads the same files from scratch and doubles token cost.

---

## Workflow

### Stage 0: Ensure Core Utilities

Before generating artifacts, ensure core utilities are available:
1. Check if `ml_utils.py` exists in the project's `src/` directory
2. If missing, scan for the core plugin's copy:
   - `.claude/plugins/*/templates/ml_utils.py`
   - `~/.claude/plugins/*/templates/ml_utils.py`
   - Copy it to `src/ml_utils.py`
3. Check if `mmm_utils.py` exists in the project's `src/` directory
4. If missing, copy from this plugin's `templates/mmm_utils.py` to `src/mmm_utils.py`

### 0) Ensure BMMM environment

```bash
/ensure-bmmm-env
```

Environment location: `knowledge_base/mmm/BMMM-env/`

### 1) Profile the data + load KB index (parallel)

Run these in a single parallel batch:

- **Profile the dataset** with a short script (rows, columns, date range, weekly aggregation stats, channel names, % zeros, % NaN, zero-revenue rows).

  After the standard profile, run **organic proxy detection**:
  - Residual columns = all columns minus date, target, org/geo structural cols, and paid channel cols
  - From residuals, drop columns whose names contain any of: `promo`, `dummy`, `flag`, `holiday`, `event`, `coupon`, `discount`, `trend`; also drop any column whose name is exactly `t` (case-insensitive)
  - The remainder are organic proxy candidates
  - Compute correlation of each candidate with the target — record for use as rationale context in §4.1
  - For each candidate, record its weekly mean — this is the normalization divisor used at build time
  - Note whether zero candidates were found (`NO_ORGANIC_PROXIES`)

- **Read KB index files**:
  - `knowledge_base/mmm/00_CORE.md`
  - `knowledge_base/mmm/02_KB_INDEX.yml`

### 2) Select and load only top-K chunks (INDEX-FIRST)

**Selection rule (MUST FOLLOW):**
- Choose **≤ 6 chunks** by matching the dataset profile to **tags** in `02_KB_INDEX.yml`.
- Open **only** the selected chunk paths.
- **Do not scan** `knowledge_base/mmm/chunks/`.

Read the templates in the same batch:
- `knowledge_base/mmm/templates/problem_brief_mmm.md`
- `knowledge_base/mmm/templates/data_readiness_mmm.md`
- `knowledge_base/mmm/templates/design_memo_mmm.md`

### 3) Fill all three documents inline (NO SUBAGENT)

Using the data profile from step 1 and the chunk knowledge from step 2, write all three output files directly. **Do not spawn mmm-methodologist or any other agent.**

Generate the `session_run_id` (format: `run_YYYYMMDD_HHMMSS_<rand4>`).

Create the output directory: `reports/mmm/{{project_name}}/{{session_run_id}}/`

After writing the three docs, write `reports/mmm/{{project_name}}/LATEST.txt` containing the `session_run_id`.

Fill each document with concrete, data-driven decisions.

**Output length rule (MUST FOLLOW):**
- Target **1–2 pages per document** (≤ ~60 lines of content). Hard cap: 3 pages.
- Skip any section that has no applicable content.
- No sign-off tables.
- Prefer a single consolidated risks table over per-section risk notes.

---

## Completion Behavior

When all three files are written:

1. Confirm all three paths exist.
2. Print a summary table: file | status | 2–3 key findings per document.
3. Print: `Design phase complete for {{project_name}}.`

### Write self-assessment (MUST run after completion)

Write to: `feedback/mmm/<project_name>/<session_run_id>/self_assessment_start_mmm.md`

Also write `feedback/mmm/<project_name>/CURRENT_SESSION.txt` containing the `session_run_id`.

### Complexity check — suggest methodologist if warranted

After completing the inline fill, evaluate complexity signals and always append:

> `/mmm-methodologist` is the next step — it gates the design and routes to `/bmmm-smoke`.

Then print: `Run /mmm-methodologist <project_name>`
