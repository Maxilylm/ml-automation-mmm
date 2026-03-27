# /self-assess

Aggregate self-assessment files from `feedback/<domain>/` across runs and surface recurring patterns as actionable improvement recommendations.

## Usage

```bash
/self-assess <domain>
```

## Token guardrails

- Read **only** files under `feedback/<domain>/`.
- If more than 20 files, read the 20 most recent.

## Workflow

### 1) Read all feedback files

Use Glob: `feedback/<domain>/**/*.md`

### 2) Aggregate by dimension

For each of the 5 dimensions (KB Coverage Gaps, Instruction Ambiguity, Execution Determinism, Data Edge Cases, Workflow Efficiency), collect all ratings and findings.

### 3) Surface recurring patterns

A pattern is **recurring** if it appears in ≥ 2 runs.

### 4) Produce recommendations

| Priority | Rule |
|---|---|
| High | ≥ 3 runs flagged, or any failure |
| Medium | 2 runs flagged with warnings |
| Low | 1 run flagged with warnings |

## Output

- Summary table: dimension x rating distribution
- Recurring patterns (≥ 2 runs only)
- Recommendations sorted by priority
- Max 3 pages total
