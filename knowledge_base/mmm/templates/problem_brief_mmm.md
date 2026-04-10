# MMM Problem Brief

> **Instructions:** Fill in every section before kicking off the design memo. Leave a field blank only if genuinely unknown — do NOT guess. Blanks become open risks.

---

## 1. Engagement Overview

| Field | Value |
|---|---|
| Client / Brand | <!-- e.g., Acme Corp — Consumer Division --> |
| Project code | <!-- e.g., ACME-MMM-2025-Q1 --> |
| Lead analyst | |
| Date of brief | <!-- YYYY-MM-DD --> |
| Delivery deadline | |

---

## 2. Business Question

**Primary question:**
> <!-- e.g., "What is the incremental ROAS of each paid media channel, and how should we reallocate our $10M annual budget?" -->

**Secondary questions (optional):**
- <!-- e.g., "Is our TV spend driving any measurable short-term revenue lift?" -->
- <!-- e.g., "How do our digital channels perform across regions?" -->

---

## 3. Target KPI

| Field | Value |
|---|---|
| KPI name | <!-- e.g., Net Revenue, Orders, Leads, Pipeline Value --> |
| KPI column in data | <!-- exact column name --> |
| Unit | <!-- $, count, etc. --> |
| Granularity | <!-- weekly (preferred) / daily --> |
| Date range | <!-- YYYY-MM-DD to YYYY-MM-DD --> |
| Known structural breaks | <!-- COVID lockdowns, re-brand, product launches --> |

---

## 4. Media Channels

List all channels to model. Mark `Paid` (has spend data) or `Organic/Unpaid` (visits/impressions only).

| Channel | Column name(s) in data | Type | Spend available? | Notes |
|---|---|---|---|---|
| <!-- e.g., Paid Search --> | <!-- spend_search, impressions_search --> | Paid | Yes/No | |
| | | | | |
| | | | | |
| | | | | |

**Channels to EXCLUDE and reason:**
- <!-- e.g., Direct mail — spend data unavailable for > 30% of period -->

---

## 5. Control Variables

| Variable | Column name | Type | Notes |
|---|---|---|---|
| Trend | <!-- t or auto-generated --> | Continuous | Weekly index |
| Seasonality | <!-- Fourier terms, or explicit flags --> | | |
| Promo / event flags | | Binary | List specific dates if known |
| Pricing index | | | |
| Other | | | |

---

## 6. Geography / Dimensions

| Field | Value |
|---|---|
| Single market or multi-market? | <!-- Single / Multi --> |
| Market/geo column | <!-- column name, or N/A --> |
| Markets in scope | <!-- list of geos or brands --> |
| Minimum obs per market | <!-- check ≥ 52 weeks per market --> |

---

## 7. Experiment & Calibration Evidence

List any experiments (geo-lift, conversion-lift, A/B) already run that can calibrate the model.

| Channel | Experiment type | Period | Measured iROAS | CI / confidence | Notes |
|---|---|---|---|---|---|
| | | | | | |

**No experiments available?** Check this box and note whether any are planned: ☐

---

## 8. Holdout & Validation

| Field | Value |
|---|---|
| Holdout window (weeks) | <!-- default: 8 weeks; B2B: 12 weeks --> |
| Any known anomalies in holdout period? | <!-- e.g., COVID spike, competitor exit --> |
| MAPE target | <!-- < 15% direct response; < 25% B2B --> |

---

## 9. Deliverables Required

- [ ] Channel ROAS with 90% HDI
- [ ] Contribution decomposition (weekly + aggregate)
- [ ] Response curves per channel
- [ ] Budget optimization recommendations
- [ ] Calibration status table
- [ ] Validation report (internal)
- [ ] Client slide deck narrative
- [ ] Other: <!-- describe -->

---

## 10. Known Risks & Open Questions

| Risk | Severity (H/M/L) | Mitigation / Action needed |
|---|---|---|
| <!-- e.g., < 52 weeks of data per geo --> | | |
| <!-- e.g., Two channels highly correlated (r > 0.8) --> | | |
| <!-- e.g., No experiment data for TV --> | | |

---

## 11. Sign-off

| Role | Name | Date |
|---|---|---|
| Lead analyst | | |
| Project lead | | |
