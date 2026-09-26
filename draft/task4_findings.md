# Task 4 — Customer Segmentation: Findings

*Group YAPPERS · BI10 Round 01 · 999 consumers aggregated from 10,992 consumer-months, 2025. Wellbeing study — segments describe behaviour, **not** credit risk. All figures reproducible via `draft/task4.py`; labelled feature table in `draft/task4_features.csv`.*

**Read the ratios, not the magnitudes.** Clustering uses only behavioural ratios and scores; raw VND is excluded per the case caveat on inflated synthetic income/credit/balance.

---

## Method & justification

**Grain.** The source is monthly (12 rows/consumer). We aggregate to **one row per consumer (999)** by taking the **yearly mean** of each feature. A ratio's annual mean is the consumer's *typical* monthly profile and is robust to a single anomalous month — the right summary for a "what kind of customer is this" question.

**Features (8), spanning the three required axes.** All z-scaled (`StandardScaler`) before clustering so no feature dominates by unit.

| Axis | Features |
|---|---|
| Financial health / stress | `financial_health_score`, `spend_to_income_ratio`, `credit_utilization_ratio`, `spending_volatility` |
| Engagement | `engagement_score`, `transaction_count` |
| Spending behaviour | `discretionary_spend_ratio`, `online_spend_ratio` |

Deliberately **excluded**: `essential_spend_ratio` (= 1 − discretionary, perfectly collinear); `category_diversity`, `active_transaction_days`, `transaction_recency_days` (near-constant — 75th percentile equals the max, so no discriminating signal). This mirrors Task 1's conclusion that behavioural ratios, not demographics, carry the signal — so **age, gender, province are excluded from clustering** and used only for post-hoc profiling.

**Model: k-means.** Chosen over the pure rule-based 2×2 because it lets the data set the boundaries across all 8 dimensions at once, rather than forcing two hard median splits. We still build the 2×2 as an independent cross-check (below).

**Choosing k.** Elbow (inertia) + silhouette over k = 2…8:

| k | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|
| inertia | 5212 | 3720 | **3228** | 2880 | 2670 | 2478 | 2301 |
| silhouette | 0.557 | 0.295 | **0.251** | 0.232 | 0.220 | 0.206 | 0.217 |

k=2 wins silhouette outright but collapses the population into a single healthy/stretched dichotomy — it throws away the engagement and digital-behaviour structure the case explicitly asks us to surface. The inertia elbow bends at **k=4**, which is also the best silhouette (0.251) inside the business-interpretable 4–6 range. **We select k=4**: four segments that are each actionable and non-overlapping.

**Quality.** Final silhouette **0.251** (moderate, expected for behavioural data with continuous gradients rather than isolated blobs). Validation is reinforced by the 2×2 cross-check agreeing on the poles (see below).

**Coverage: 999 / 999 consumers assigned to exactly one segment — PASS.** All 7 minors (age 15–17) are retained.

---

## Segment profiles (cluster means, unscaled)

Global means for reference: FHS 66.3 · spend/income 0.693 · credit-util 0.190 · volatility 1.49 · engagement 75.4 · txns/mo 155 · discretionary 0.546 · online 0.247.

| Segment | n | % | FHS | spend/inc | credit-util | volatility | engage | txns/mo | discret. | online |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **Financially Healthy & Highly Engaged** | 351 | 35.1% | **70.5** | **0.571** | **0.148** | 1.44 | 77.4 | 153 | 0.513 | 0.200 |
| **Financially Stretched but Highly Engaged** | 302 | 30.2% | **62.6** | **0.835** | **0.248** | 1.42 | 76.5 | 119 | 0.519 | 0.208 |
| **High-Activity Digital Power Users** | 258 | 25.8% | 65.1 | 0.718 | 0.188 | **1.91** | **80.2** | **251** | 0.514 | 0.212 |
| **Low Engagement & Emerging Digital** | 88 | 8.8% | 65.7 | 0.614 | 0.173 | **0.68** | **49.6** | **9.7** | **0.866** | **0.671** |

**Bold = the defining extreme for that segment.** Each segment is named after the pole that separates it: highest health, most stretched (highest spend/income + credit-util), most transactions, and lowest engagement.

---

## Post-segmentation analysis — key differentiators & recommendations

**1 · Financially Healthy & Highly Engaged (351, 35.1%).** The anchor segment. Highest FHS (70.5), lowest spend-to-income (0.571) and credit utilisation (0.148), essential-leaning spend (discretionary 0.513, below the 0.546 average), and active (153 txns/mo). Financially comfortable and habitually transacting.
*Recommendation:* **retain and grow value.** Low-touch — offer premium/loyalty and cross-sell (savings, investment nudges). Do not spend acquisition-style budget here; protect the relationship.

**2 · Financially Stretched but Highly Engaged (302, 30.2%).** The wellbeing priority. Lowest FHS (62.6) with the **highest spend-to-income (0.835)** and **highest credit utilisation (0.248)** — spending a large slice of income and leaning hardest on credit, while still fully engaged (76.5, 119 txns/mo). This is Task 1's 25–34 vulnerability pattern made into a segment.
*Recommendation:* **non-punitive budgeting support** — spend-pacing alerts, discretionary-category visibility, a "spend vs income this month" view. Framed as wellbeing tooling, not credit restriction. Highest-leverage target for Task 5.

**3 · High-Activity Digital Power Users (258, 25.8%).** Mid health (65.1) but the **most active** (251 txns/mo, ~1.6× average) and **most volatile** (1.91) with the highest engagement (80.2). Heavy, spiky transactors — not yet stressed, but volatility is a watch signal.
*Recommendation:* **monetise engagement, monitor drift.** Ideal for rewards, recurring-payment enrolment and real-time features; flag the volatile sub-tail before it slides into segment 2.

**4 · Low Engagement & Emerging Digital (88, 8.8%).** The smallest, most distinct segment. Near-dormant (9.7 txns/mo, engagement 49.6) but what little they do is **overwhelmingly online (0.671 vs ~0.20 elsewhere) and discretionary (0.866 vs 0.55)**. Health is average — these are low-frequency, digital-first, discretionary spenders, not vulnerable customers.
*Recommendation:* **activate.** Digital-channel onboarding and habit-forming nudges (the fuel/frequency lever from Task 1) to convert sporadic online use into regular engagement. Highest growth headroom.

**Rule-based 2×2 cross-check (validation).** An independent health×engagement matrix on medians (FHS 66.2, engagement 78.2) produces four near-equal quadrants (238–260 each). Crosstab vs k-means confirms the poles align — the Healthy cluster maps to Healthy+Engaged/Disengaged (344/351), the Stretched cluster to Stretched+Engaged/Vulnerable (273/302) — while k-means additionally isolates the **Emerging Digital** group (88) that a 2×2 buries inside its quadrants. That extra structure is exactly why we deliver k-means over the 2×2.

---

## Limitations & future work

**Technical.**
- **Moderate silhouette (0.251).** Behaviour is a continuum, not sharp clusters; boundary consumers could plausibly sit in a neighbouring segment. k-means imposes convex boundaries — GMM (soft assignment) or HDBSCAN would express membership uncertainty.
- **Mean aggregation hides within-year trajectory.** A consumer trending from healthy → stretched is averaged flat. Trend/slope or volatility-of-ratios features would capture drift.
- **Feature selection is a judgement call.** We dropped near-constant columns and one collinear ratio; a different set (e.g. keeping category_diversity) would shift boundaries slightly.

**Operational / data.**
- **Synthetic, single-year (2025) data** with the two-years-folded-onto-2025 quirk from Task 1 — segment *sizes* are directionally real, not a production census.
- **Engagement is skewed high** (mean 75.4, mostly 74–81); the Emerging-Digital tail (engagement 49.6) is real but small, so that segment is the least statistically robust (n=88).
- Segments are **not credit-risk tiers** and must not be used for lending decisions — this is a wellbeing lens.

**Future work.** (1) Re-fit on multi-year data to make segments temporally stable and migration-trackable. (2) Add GMM/soft membership to quantify boundary confidence. (3) Engineer trajectory features (health slope, volatility trend) to catch consumers *entering* the stretched segment early — the highest-value early-warning signal for Task 5. (4) Validate segment stability via bootstrap resampling.
