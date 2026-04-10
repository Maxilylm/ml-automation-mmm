# MMM Data Readiness Checklist

> **How to use:** Complete this checklist on the raw client data BEFORE starting model design. Each ☐ item must be resolved or formally accepted as a risk before proceeding to the design memo.

**Project:** <!-- project code -->
**Analyst:** <!-- name -->
**Date:** <!-- YYYY-MM-DD -->
**Data snapshot date:** <!-- the date up to which data was received -->

---

## 1. File & Format

- [ ] Data received in agreed format (CSV / Parquet / Excel)
- [ ] Date column exists and is parseable as ISO date (`YYYY-MM-DD`)
- [ ] Granularity confirmed: **weekly** (preferred) or daily
- [ ] No duplicate date rows per market/dimension
- [ ] All columns have clear, documented names (request a data dictionary if not)

---

## 2. Target KPI

- [ ] Target column exists: `______________` (fill column name)
- [ ] Target is strictly positive (> 0) for all rows
- [ ] No NaN or zero values in target — if zeros exist, confirm they represent true zero sales and document
- [ ] Target values are on a sensible scale (not already log-transformed; not already normalized)
- [ ] Structural breaks identified and documented: `______________`

**Target stats (fill after loading):**

| Metric | Value |
|---|---|
| Rows (weeks) | |
| Date range | |
| Mean | |
| Min | |
| Max | |
| % weeks with value < 10% of mean | |

---

## 3. Channel Spend / Media Columns

For each channel column:

| Channel | Column | Min | Max | % Zeros | % NaN | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |

**Rules:**
- [ ] All channel columns exist in the data
- [ ] No NaN values in any channel column (fill with 0 after confirming intent)
- [ ] Channels with CV < 0.05 (near-constant spend) flagged — saturation cannot be identified → set `NoSaturation` for those channels
- [ ] Channels with > 30% zero weeks flagged — adstock may have limited variation → widen alpha prior
- [ ] Spend columns confirmed to be raw $spend (not pre-normalized, not log-transformed)
- [ ] If model uses visits/impressions as input, the corresponding spend column is mapped in config (`spend_mapping`)

---

## 4. Control Variables

- [ ] Trend variable available (can be auto-generated as weekly index)
- [ ] Seasonality coverage: data spans ≥ 52 weeks to support 2-pair Fourier seasonality
- [ ] Promo / event dummy columns identified and dates documented
- [ ] Any major competitor events, price changes, or external shocks documented as dummies
- [ ] Control variable list agreed with client before model build

---

## 5. Geo / Multi-Dimensional Data (skip if single market)

- [ ] Dimension column exists: `______________`
- [ ] Markets / geos in scope: `______________`
- [ ] Each market has ≥ 52 weeks (preferred ≥ 104 weeks)
- [ ] No market with < 26 weeks — exclude or use full-pooled model for that market
- [ ] Pairwise correlation of spend across markets computed — note markets with r > 0.8
- [ ] Global max scaling confirmed (not per-geo scaling, which breaks hierarchical model)

**Market-level data summary:**

| Market | Rows (weeks) | Date range | Notes |
|---|---|---|---|
| | | | |

---

## 6. Minimum Data Requirements

| Check | Required | Actual | Pass? |
|---|---|---|---|
| Total weeks in training set | ≥ 52 | | ☐ |
| Preferred weeks (for stable seasonality) | ≥ 104 | | ☐ |
| Holdout weeks reserved | ≥ 8 (B2B: ≥ 12) | | ☐ |
| Weeks per market (geo model) | ≥ 52 | | ☐ |

---

## 7. Collinearity Check

- [ ] Pairwise correlation matrix computed for all channel spend columns
- [ ] No channel pair with r > 0.85 — if found, document and discuss with team:

| Channel pair | Correlation | Decision |
|---|---|---|
| | | Merge / Strong prior / Separate estimation |

---

## 8. Experiment & Calibration Data

- [ ] Experiment results file received (if applicable)
- [ ] Experiment period does NOT overlap with known anomalies
- [ ] Experiment geo coverage ≥ 10% of total sales
- [ ] Multiple channels were NOT simultaneously active in the same test arm
- [ ] Measured iROAS and confidence interval documented per channel

---

## 9. Data Leakage Pre-check

- [ ] Train/holdout split will be performed BEFORE any normalization or transformation
- [ ] No future-looking variables included (e.g., forward-filled prices, lookahead sales)
- [ ] Normalization scalers will be computed on training set only
- [ ] Promo dummies are known at model-build time (not leak from future)

---

## 10. Sign-off

**Overall data readiness:** PASS ☐ / CONDITIONAL PASS ☐ / FAIL ☐

**Conditions (if conditional pass):**
- <!-- list outstanding items that must be resolved before model fit -->

| Role | Name | Date |
|---|---|---|
| Analyst | | |
| Data provider confirmed | | |
