# Task 1 — Exploratory Data Analysis: Findings

*Group YAPPERS · BI10 Round 01 · 999 consumers, 1,852,394 transactions, 2025, VND. All figures reproducible via `draft/task1_eda.py`.*

**Read the ratios, not the magnitudes.** Synthetic income/credit/balance are inflated; every insight below leans on shares and ratios, per the case caveats.

---

## Q1 — December is the year's spending engine, and it runs on frequency, not bigger baskets

| Metric | Peak (Dec) | Trough (Feb) |
|---|---|---|
| Total spend | 488.03B VND (**15.04%** of the 3.24T annual) | 174.37B VND (5.37%) |
| Transactions | 280,598 | 97,657 |
| Avg ticket | 1.74M VND | 1.79M VND |

December alone is **~1 in every 6.6 VND spent all year** and is **2.8× the trough month**. The decomposition is unambiguous: transaction **count is +187%** peak-vs-trough while **ticket size actually falls 2.6%**. Customers don't buy *pricier* things in December — they buy *more often* (year-end/Tết-prep bunching).

**BI insight:** Peak demand is a frequency phenomenon. Capacity, fraud monitoring, and engagement campaigns should scale to transaction *volume*, not basket value. The lever to grow peak revenue is trip frequency and channel availability, not upsell.
*Caveat: all 1,852,394 timestamps are in 2025, and December's uplift is uniform across all 14 categories (+181% to +193%) — it looks like a synthetic seasonal multiplier, so treat the 15% as directional, not a forecast.*

---

## Q2 — Financial stress flips the budget from essential to discretionary *(headline finding)*

| Segment | Consumers (cons-months) | Essential | Discretionary |
|---|---|---|---|
| **Stressed** (FHS < 40) | 70 (95) | **28.4%** | **71.6%** |
| **Healthy** (FHS ≥ 80) | 303 (475) | **59.5%** | **40.5%** |

The composition **inverts completely**. Healthy customers spend the majority of their money on essentials (mean essential ratio 0.61); stressed customers spend nearly **three-quarters on discretionary** (essential ratio 0.29).

**BI insight:** Low financial health is not a story of people scraping by on necessities — in this data it co-occurs with a **discretionary-heavy budget mix**. That reframes the intervention (Task 5): the highest-leverage, *non-punitive* help is budgeting visibility and spend alerts on discretionary categories, not credit restriction. This single contrast is the strongest driver in the dataset and should anchor the segmentation and recommendations.

---

## Q3 — There is essentially **no regional digital divide** (a finding worth stating plainly)

National digital share: **41.2%** (POS 58.8%). Every high-spend province sits within **±0.5pp** of that average:

| Province | Total spend | Digital share | Gap vs national |
|---|---|---|---|
| Hà Nội | 267.26B | 40.9% | −0.3pp |
| Đồng Nai | 183.07B | 40.7% | −0.5pp |
| Lâm Đồng | 135.39B | 41.1% | −0.1pp |
| Hưng Yên | 116.44B | 40.8% | −0.4pp |
| Hải Phòng | 103.15B | 40.8% | −0.3pp |

**BI insight (honest reporting):** These provinces *technically* qualify as "high spend, below-average digital," but the gaps are within noise — digital adoption is effectively **flat across geography** in this dataset. The correct conclusion is that **province is not a useful lever for a digital-adoption campaign**; targeting must be done at the *customer* level (channel mix, category diversity), which the case study itself confirms. Do not build a "lagging-region" narrative the data won't support.

---

## Q4 — Two different shopping rhythms: habitual fuel vs. high-value grocery baskets

| | Category | Volume | Avg ticket |
|---|---|---|---|
| **Top by count** | Xăng dầu và di chuyển (Fuel & transport) | 188,029 txns | 1.59M VND |
| **Top by spend** | Siêu thị và tạp hóa (In-store groceries) | 513.77B VND | 2.92M VND |

Groceries carry a **1.8× larger ticket** than fuel. Fuel is the **most frequent, lowest-value habit** (many small refuels); groceries are **fewer, larger stock-up baskets**. (Travel has the single highest ticket, 2.79M, but only 57,956 txns — occasional big-spend.)

**BI insight:** Frequency ≠ revenue. Fuel is the best *engagement/touchpoint* category (nudges, recurring-payment enrolment, habit loops); groceries are the best *value* category (basket-level offers, essential-spend rewards). Product design should treat them oppositely.

---

## Q5 — The 25–34 cohort is the vulnerability hotspot: active, over-extended, discretionary-tilted

| Cohort | Consumers | Avg FHS | Avg txns/mo | Essential ratio | Spend/income |
|---|---|---|---|---|---|
| 15–24 | 69 | 65.9 | 221.6 | 0.355 | 0.676 |
| **25–34** | **177** | **65.8 (lowest)** | **178.7** | **0.468** | **0.716 (highest)** |
| 35–44 | 165 | 66.4 | 199.4 | 0.464 | 0.694 |
| 45–54 | 198 | 66.0 | 176.9 | 0.493 | 0.712 |
| 55–64 | 175 | 67.0 | 129.6 | 0.508 | 0.696 |
| 65+ | 215 | 66.9 | 139.1 | 0.509 | 0.685 |

Among cohorts with above-median activity, **25–34 records the lowest financial health (65.8)** while carrying the **highest spend-to-income ratio (0.716** vs 0.700 national**)** and a **below-average essential ratio (0.468** vs 0.481**)**. Young working adults are transacting heavily, spending the largest slice of income, and skewing that spend toward discretionary.

**BI insight:** Vulnerability here is behavioural, not demographic scarcity — high activity + high spend-to-income + discretionary tilt. The 25–34 group (177 customers) is the natural primary target for budgeting tools and spend-pacing alerts (Task 5), and a likely core of the "financially stretched but highly engaged" segment (Task 4).
*Coverage: all 999 consumers binned (min age 15). Caveat: FHS spreads only 65.8–67.0 across cohorts — age is a weak differentiator on its own; the ratio signals matter more than the age band. Note the youngest cohort includes 7 minors aged 15–17.*

---

## What this means for the rest of the case

1. **Q2 is the spine.** The essential↔discretionary inversion by health is the strongest, cleanest signal — build segmentation (Task 4) and interventions (Task 5) around spend *composition*, not credit.
2. **Target at the customer level, not the map.** Q3 shows geography carries no digital signal; Q5 shows age carries little health signal. The differentiators are behavioural ratios (spend/income, essential ratio, digital mix, category diversity).
3. **Frequency drives peaks and engagement; value lives elsewhere.** Q1 + Q4 separate the "how often" story (December, fuel) from the "how much" story (groceries, travel).

---

## Deep-dive (27/09) — `draft/task1_deep.py`, output in `task1_deep_output.txt`

- **Q3 channel breakdown (new slide).** The five high-spend, below-average-digital provinces (Ha Noi, Dong Nai, Lam Dong, Hung Yen, Hai Phong) have POS 58.9–59.3% of transactions vs 58.8% nationally; QR 19.7–20.1%, E-com 8.4–8.7%, Mobile 7.4–7.6%, Recurring 4.8–5.1%. Largest digital gap is **−0.46pp** (Dong Nai); digital *value* share 40.9–41.5% vs 41.5%. The "gap" is statistically real but commercially negligible — geography is not a lever. Chart: `t1_province_channel.png`.
- **Q2 is a gradient, not a threshold artefact.** Discretionary share by FHS band: **71.6% (<40) → 64.2 (40s) → 57.3 (50s) → 54.4 (60s) → 49.2 (70s) → 40.6% (80s)**. Every cutoff pair keeps the direction (FHS<35 vs ≥85: 73.5% vs 30.2%; <50 vs ≥70: 65.4% vs 48.7%); Spearman −0.47 at month grain. Chart: `t1_discretionary_gradient.png`.
- **Q1 December driver.** Dec − Feb adds 182,941 transactions, spread across **all 14 categories at +181% to +193%** — no category leads (largest contributor Fuel & Transport 10.2% of the increase). All timestamps are 2025, so the earlier "two years folded" caveat is withdrawn; the uniform uplift reads as a synthetic seasonal multiplier.
- **Q4 reach.** Fuel & Transport is bought by **96.8%** of consumers (17.3 purchases per buyer-month, 11.2 months/yr); in-store Groceries by **99.3%** (16.1 per buyer-month) — both are near-universal habits.
- **Q5 age is not a differentiator.** Bootstrap 95% CIs of mean FHS overlap for all six cohorts (65.75–66.97; max lower bound 66.35 < min upper bound 66.43). 25–34 is lowest in point estimate only. CI table: `draft/task1_age_ci.csv`.
