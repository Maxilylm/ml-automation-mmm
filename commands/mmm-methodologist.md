# /mmm-methodologist

Gate command for MMM methodologist review. Reads the latest design memo, evaluates complexity signals, and either invokes the mmm-methodologist agent or passes straight to `/bmmm-smoke`.

## Usage

```bash
/mmm-methodologist <project_name>
```

## Workflow

### 1) Locate the design memo

- Read `reports/mmm/<project_name>/LATEST.txt` → get `run_id`
- Read `reports/mmm/<project_name>/<run_id>/design_memo_mmm.md`

### 2) Evaluate complexity signals

| Signal | How to detect | Score |
|---|---|---|
| Multiple geos | §1 Dimensions ≠ "None" | 0/1 |
| Many channels | §3 Channel Config ≥5 rows | 0/1 |
| Calibration evidence | §5.3 has filled rows | 0/1 |
| B2B / long-cycle adstock | Any channel l_max > 8 | 0/1 |
| Binary or near-constant channel | CV < 0.05 or < 3 distinct levels | 0/1 |
| High channel collinearity | §7 lists pair r > 0.8 | 0/1 |
| Short series | §2 Training window < 52 weeks | 0/1 |

### 3) Gate decision

| Signals | Decision |
|---|---|
| 0 | **Pass** — skip agent, suggest `/bmmm-smoke` |
| 1–2 | **Review recommended** — invoke `mmm-methodologist` agent |
| ≥3 | **Review required** — invoke `mmm-methodologist` agent |

### 4a) If 0 signals — pass through

> **Methodologist gate: PASS** — Run `/bmmm-smoke` to validate the pipeline.

### 4b) If ≥1 signal — invoke the agent

Spawn `mmm-methodologist` subagent with the design memo path and flagged signals.
