# Task 2 — Financial Health Analysis: Findings

*Group YAPPERS · BI10 Round 01 · 999 consumers × ~11 months = 10,992 consumer-months, 2025, VND. All figures reproducible via `draft/task2.py`.*

**This is a wellbeing study, not credit scoring.** `financial_health_score` (FHS) measures spending health, not creditworthiness. Every driver below is a ratio, not a VND magnitude, per the case caveats.

---

## Q1 — Health is a tight, slightly left-skewed band; distress is *episodic*, never chronic

| View | n | Mean | Median | Std | Min | Max | Skew |
|---|---|---|---|---|---|---|---|
| **Consumer level** (12-mo mean per person) | 999 | 66.30 | 66.24 | 4.67 | 42.32 | 80.83 | −0.32 |
| **Month level** (consumer-months) | 10,992 | 66.37 | 67.70 | 9.48 | 0.80 | 90.20 | — |

Consumer percentiles: p5 **58.6** · p25 63.4 · p50 66.2 · p75 69.3 · p95 **73.9**. The population is a **narrow band around ~66** with a mild low-side tail.

**Segment shares (consumer-months):**

| Segment | Consumer-months | Share |
|---|---|---|
| Ổn định (Stable) | 7,965 | **72.5%** |
| Cần theo dõi (Watch) | 2,457 | 22.4% |
| Khỏe mạnh (Healthy) | 475 | 4.3% |
| Có dấu hiệu căng thẳng tài chính (Stressed) | 95 | **0.9%** |

The decisive fact: **only 95 of 10,992 consumer-months (0.9%) score FHS < 40, and 0 of 999 consumers** have a 12-month *mean* below 40 (the lowest consumer averages 42.3). Month-to-month, mean FHS swings from **73.6 (Feb) down to 54.2 (Dec)** — December's spending surge (Task 1 Q1) drags health down system-wide.

**BI insight:** Financial stress in this data is a **transient monthly state, not a fixed customer type.** Nobody is chronically unhealthy; healthy customers dip into stress in specific months (led by December). This means interventions should be **event-triggered** (fire when a customer's *current-month* FHS drops), not a static "high-risk list." Consumer-level averaging hides the entire distressed population — always analyse distress at the month grain.
*Caveat: the month-level min of 0.80 and inflated tails reflect synthetic magnitudes; trust the shape and shares, not the extremes.*

---

## Q2 — Low health is an *overspend* story: spend-to-income and credit utilization dominate

Ranked Pearson correlation of ratio fields against FHS (n = 10,992 months):

| Rank | Factor | Corr with FHS | Direction |
|---|---|---|---|
| 1 | **spend_to_income_ratio** | **−0.898** | more spend vs income → lower health |
| 2 | **credit_utilization_ratio** | **−0.862** | more limit used → lower health |
| 3 | spending_volatility | −0.496 | erratic spend → lower health |
| 4 | essential_spend_ratio | +0.481 | more on essentials → **higher** health |
| 5 | discretionary_spend_ratio | −0.481 | more on wants → lower health |
| 6 | engagement_score | **−0.299** | *more engaged → lower health* |
| 7 | online_spend_ratio | −0.273 | more online → lower health |
| 8 | average_transaction_value_vnd | −0.206 | — |
| 9 | active_transaction_days | −0.145 | — |
| 10 | category_diversity | −0.069 | negligible |
| 11 | transaction_recency_days | +0.017 | none |

**Low health defined as FHS < 40.** Contrast of the 95 stressed vs 475 healthy (FHS ≥ 80) consumer-months:

| Factor | Stressed (FHS<40) | Healthy (FHS≥80) |
|---|---|---|
| spend_to_income_ratio | **2.098** | 0.289 |
| credit_utilization_ratio | **0.582** | 0.078 |
| spending_volatility | 3.017 | 0.984 |
| essential_spend_ratio | 0.288 | 0.611 |
| discretionary_spend_ratio | 0.712 | 0.389 |
| engagement_score | **81.1** | 72.7 |

Stressed months show customers spending **~2.1× their income** and burning **58% of their credit line**, with a discretionary-heavy mix (71% wants vs 29% essentials) — the exact inversion Task 1 Q2 flagged. The two spend-vs-capacity ratios alone (−0.90, −0.86) explain almost all of health.

**BI insight:** Low health is **overspending relative to capacity**, not low income. The most striking row is engagement: **stressed months are *more* engaged than healthy ones (81.1 vs 72.7, corr −0.30).** Distress and engagement move *together* — the people sliding into stress are active, not disengaged. That is the direct setup for Q4 and reframes intervention toward **spend-pacing and utilization alerts**, never credit denial.
*Caveat: essential/discretionary ratios and FHS are partly constructed from the same spend fields, so correlations are directional, not causal proof.*

---

## Q3 — Age and province are weak; occupation is unusable (confirming Task 1)

**Age cohort** (consumer level) — spread of just **1.22 FHS points** across all six bands:

| Cohort | Consumers | Mean FHS |
|---|---|---|
| 15–24 | 69 | 65.75 |
| 25–34 | 177 | 65.79 |
| 35–44 | 165 | 66.44 |
| 45–54 | 198 | 65.98 |
| 55–64 | 175 | **66.97 (best)** |
| 65+ | 215 | 66.56 |

**Province** (≥15 consumers) — spread **4.84 pts**, best/worst both thin and near the mean:

| | Province | Consumers | Mean FHS |
|---|---|---|---|
| Worst | Thái Nguyên | 18 | 62.98 |
| … | Đà Nẵng | 31 | 64.66 |
| Best | Hà Nội | 80 | 67.82 |
| Largest | TP. Hồ Chí Minh | 135 | 67.59 |

**Occupation:** 396 distinct titles across 999 consumers → **max 10 consumers per occupation**, only 3 occupations reach 8+. Any occupation ranking is pure sample noise (the ≥6-consumer subset spans 59.1–71.9, driven by 6-person cells).

**BI insight (honest reporting):** Demographics do **not** differentiate health. Age spans 1.2 points (vs a 4.67 cross-consumer std) and province 4.8 points on thin cells; occupation is too fragmented to use at all. This confirms Task 1's conclusion: **target at the behavioural-ratio level, not the demographic level.** The best predictors are Q2's ratios, not who or where the customer is.
*Caveat: FHS is bounded ~42–81 across consumers, so even the "worst" province (63.0) is a healthy customer — these are gaps within a healthy population.*

---

## Q4 — Crossover segment: "Stressed but Engaged" = 43 consumers, ~half of all distress

**Rule (reproducible, consumer-month grain):** `financial_health_score < 40 AND engagement_score >= p75 (81.40)`.
*Applied at the month grain because 0 consumers are chronically stressed (Q1) — the segment only exists as episodes.*

| Metric | Value |
|---|---|
| Stressed consumer-months (FHS<40) | 95 (70 distinct consumers) |
| **Crossover consumer-months** | **49** |
| **Crossover distinct consumers** | **43 (4.3% of 999)** |
| Share of all stressed months | **52%** |

**Profile — crossover months vs all consumer-months (means):**

| Factor | Crossover | All months |
|---|---|---|
| financial_health_score | 29.9 | 66.4 |
| engagement_score | **88.6** | 77.8 |
| spend_to_income_ratio | **1.89** | 0.70 |
| credit_utilization_ratio | **0.55** | 0.19 |
| discretionary_spend_ratio | 0.71 | 0.52 |
| online_spend_ratio | **0.49** | 0.21 |
| spending_volatility | 2.06 | 1.56 |
| essential_spend_ratio | 0.29 | 0.48 |
| transaction_count | 97.5 | 168.5 |

Cohort mix skews to working-age (25–34: 12 months; 45–54: 10), mean age 47 vs 49.

**BI insight:** **More than half of every financial-stress episode happens to a highly engaged customer** — someone spending ~1.9× income, using 55% of their credit, tilting to discretionary (71%) and online (49%, over 2× national). These are not disengaged customers to win back; they are **active, digital, over-extended customers the bank already reaches.** That makes them the single highest-leverage, lowest-cost intervention target: the channel is already open. The right nudge is **non-punitive spend-pacing / utilization alerts delivered in-app in the stress month**, not credit restriction.
*Caveat: 49 months across 43 consumers is a small, synthetic cell — treat the profile as a directional archetype, not a sized market.*

---

## What this means for segmentation & recommendations

1. **Trigger on the month, not the person.** Distress is episodic (0 chronically unhealthy consumers). Segmentation for intervention must read *current-month* FHS, not a static risk list.
2. **Two ratios are the whole game.** spend_to_income (−0.90) and credit_utilization (−0.86) define health; demographics add nothing. Score and alert on these.
3. **The "Stressed but Engaged" 43 are the primary target (Task 5).** They are already active and digital, so reaching them costs nothing — deliver spend-pacing and utilization nudges in-app, framed as wellbeing help, never as a credit decision.
