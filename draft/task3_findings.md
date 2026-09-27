# Task 3 — Customer Engagement Analysis: Findings

*Group YAPPERS · BI10 Round 01 · 999 consumers, 10,992 consumer-months, 1,852,394 transactions, 2025. All figures reproducible via `draft/task3.py`.*

**This is a wellbeing study, not credit scoring — read shares and ratios, not VND magnitudes.** And read every engagement number against one fact: **the base is saturated at the top.** 99.0% of consumer-months sit in "high" or "very high" engagement (mean score 77.8). Differentiation lives in the *tails* and in *what people do* (digital mix, category diversity), not in the average. Every section below reflects that honestly.

---

## Q1 — Engagement is saturated high; the whole story is in a thin low tail

| Statistic (engagement_score) | Consumer-month | Consumer-level |
|---|---|---|
| Mean | 77.82 | 75.40 |
| Median | 78.10 | 78.17 |
| Min / Max | 9.70 / 99.60 | 12.80 / 84.32 |
| Std | 6.33 | — |

| Engagement segment | Consumer-months | Share | Consumers (modal) | Share |
|---|---|---|---|---|
| Tương tác rất cao (very high) | 3,824 | 34.8% | 169 | 16.9% |
| Tương tác cao (high) | 7,058 | 64.2% | 740 | 74.1% |
| Tương tác trung bình (medium) | 100 | 0.9% | 80 | 8.0% |
| Tương tác thấp (low) | 10 | 0.1% | 10 | 1.0% |

**BI insight:** Engagement does not segment the base — **91.0% of consumers are "high," and only 90 consumers (9.0%) fall below it.** The consumer-level mean (75.4) sits *below* the median (78.2), the classic signature of a left-skewed distribution: a small dormant tail (min 12.8) drags the average while the mass piles against the ceiling. Practically, "engagement" is table stakes here — targeting must key on *behaviour beneath the score* (Q2–Q4), and the only genuinely actionable engagement cohort is the thin low tail (Q5).
*Caveat: synthetic cards are engineered to be very active, so the high skew is partly a data artefact — do not present "99% highly engaged" as an organic win.*
*Chart: **histogram** of engagement_score (bin width ~5) to expose the left tail, with a **100% stacked bar** for segment share.*

---

## Q2 — One in five VND is digital; POS still owns the base *(channel reality check)*

| Channel | Transactions | Share |
|---|---|---|
| POS | 1,089,518 | 58.8% |
| QR Payment | 367,682 | 19.8% |
| E-commerce | 161,670 | 8.7% |
| Mobile App | 142,399 | 7.7% |
| Recurring Payment | 91,125 | 4.9% |

- **Digital share ≈ 41.2%** (QR + E-com + Mobile + Recurring), POS 58.8% — matches the Task 1 national context exactly.
- **Average online spend share (online_spend_ratio): 21.0%** at consumer-month grain, **24.7%** at consumer level, ranging **0.0% → 95.1%** across customers.

**BI insight:** Adoption breadth exists (QR is a real second rail at ~20% of trips) and value follows: non-POS channels carry 41.2% of trips and 41.5% of spend value (same ticket size as POS). *(Corrected 27/09: an earlier draft compared the channel count share with the separate `online_spend_ratio` field, 21%, which counts only truly online spend.)* The wide per-customer online_spend_ratio range (0–95%) is the real segmentation lever the flat engagement score cannot give — this is where digital-adoption campaigns should target.
*Chart: **stacked/treemap bar** for channel mix; **histogram or box plot** of online_spend_ratio to show the 0–95% spread.*

---

## Q3 — Category diversity is the cleanest engagement signal in the dataset

Range: category_diversity spans **2 → 14** (consumer-month; consumer-level mean 12.94, median 14 — most customers touch nearly every category).

| Engagement segment | n (cons-mo) | Mean category_diversity | Mean engagement |
|---|---|---|---|
| Tương tác thấp (low) | 10 | 4.20 | 25.15 |
| Tương tác trung bình (medium) | 100 | 5.78 | 52.06 |
| Tương tác cao (high) | 7,058 | 13.65 | 75.03 |
| Tương tác rất cao (very high) | 3,824 | 13.91 | 83.78 |

Correlation(category_diversity, engagement_score): **+0.590** (consumer-month), **+0.938** (consumer-level).

**BI insight:** Category diversity tracks engagement almost perfectly at the customer level (**r = 0.94**) — the disengaged tail is disengaged precisely because it is *narrow* (4–6 categories) while the engaged mass is broad (~14). But note the ceiling effect: once inside "high," diversity barely separates high (13.65) from very-high (13.91), so **diversity discriminates the dormant tail from everyone else, not the good from the great.** It is the best early-warning flag for disengagement: a customer whose category count is falling is disengaging before the composite score moves.
*Chart: **scatter** of category_diversity vs engagement_score (consumer-level, showing the tight line), with a **bar** of mean diversity per segment.*

---

## Q4 — Recency and frequency confirm the same split: dormant tail vs saturated core

| Metric | Min | Median | Mean | Max |
|---|---|---|---|---|
| transaction_recency_days | 0.0 | 0.0 | 0.2 | 30.0 |
| transaction_count (per month) | 2 | 150 | 168.5 | 713 |
| active_transaction_days (per month) | 1 | 30 | 28.6 | 31 |
| txn_per_active_day | 1.30 | 5.03 | 5.70 | 23.0 |

Correlation with engagement_score: active_transaction_days **+0.589**, transaction_count **+0.404**, txn_per_active_day **+0.349**, transaction_recency_days **−0.424**.

| Engagement segment | Recency (days) | Txn count | Active days | Engagement |
|---|---|---|---|---|
| Tương tác thấp (low) | 21.10 | 7.4 | 1.80 | 25.15 |
| Tương tác trung bình (medium) | 10.73 | 13.2 | 4.42 | 52.06 |
| Tương tác cao (high) | 0.06 | 148.0 | 28.44 | 75.03 |
| Tương tác rất cao (very high) | 0.02 | 210.9 | 29.69 | 83.78 |

**BI insight:** The engaged core transacts on **28–30 of ~31 days** with **near-zero recency** (they used the card today) — recency and active-days are effectively maxed out, so among engaged customers they carry no signal. The discriminating power is entirely at the bottom: the low tail sits at **~2 active days, 21-day recency, 7 transactions.** Consistency of activity (active_transaction_days, r=+0.59) beats raw volume (transaction_count, r=+0.40) as the engagement driver — *how regularly*, not *how much*.
*Chart: **box plots** of transaction_count / active_days by segment; a **recency histogram** (spike at 0, thin tail to 30).*

---

## Q5 — High-health, low-engagement: 25 customers, financially fine but drifting away *(headline finding)*

**Stated cutoff: financial_health_score ≥ 70 (high) AND engagement_score < 70 (low), at consumer level.**

**Group size: 25 consumers = 2.5% of the base.** They are 11.8% of all 211 high-health customers, and the healthy half of the 92-consumer low-engagement tail (67 of the other 92 are low-engagement *and* low-health — a different, stress-driven problem, not this one).

### Why exactly these cutoffs
- **Low engagement < 70 sits in a natural gap, not an arbitrary line.** The sensitivity sweep returns the *identical 25 consumers* at eng < 65, < 68, and < 70 — nobody in the high-health group scores between 65 and 70, so the cluster is genuinely isolated. Loosening to < 72 adds 11 (36 total) and < 74 adds 27 (52), because at ~72 you start eating into the healthy-engaged mass (consumer-level p10 = 71.1). **70 is the last cutoff before the tail bleeds into the core** — stricter costs nothing, looser dilutes the segment with normal customers.
- **High health ≥ 70 is roughly the top quartile of wellbeing** (consumer-level health p75 = 69.3, p90 = 72.2). A stricter ≥ 75 would drop below the p90 and shrink the group to near-zero without changing its character; ≥ 70 keeps it identifiable while still meaning "clearly healthy."

### Profile vs the rest of the base (consumer-level means)

| Metric | Group (n=25) | Rest (n=974) |
|---|---|---|
| financial_health_score | 74.03 | 66.10 |
| engagement_score | 46.83 | 76.14 |
| category_diversity | 4.68 | 13.15 |
| online_spend_ratio | 0.606 | 0.238 |
| transaction_count (per mo) | 9.9 | 159.1 |
| active_transaction_days | 2.0 | 27.0 |
| transaction_recency_days | 14.3 | 0.9 |

**BI insight:** This is a **dormancy risk, not a distress risk.** These 25 are financially healthier than average (74 vs 66) yet transact ~10 times a month on ~2 days, touch only ~5 categories, and last used the card ~2 weeks ago — a near-churned profile hiding inside a "healthy" label. The tell is **online_spend_ratio 0.61 vs 0.24**: when they *do* pay, it is overwhelmingly digital — they have not abandoned spending, they have moved it off this card to a narrow set of online use-cases. The retention play is not credit or budgeting help (they don't need it); it is **reactivation of offline/everyday use** — bring back the daily POS and category breadth the engaged core shows.
*Caveat: n=25 is small and engagement is synthetic-inflated, so treat this as a qualitatively distinct cohort to watch, not a precisely sized forecast. The stricter, larger sibling problem (67 low-health + low-engagement) belongs to the Task 5 intervention track, not retention.*
*Chart: **2×2 quadrant scatter** (x = engagement, y = financial_health, reference lines at 70/70) — the group is the isolated lower-right cluster.*

---

## What this means for segmentation & recommendations

1. **Do not segment on the engagement score.** It is saturated (91% "high") — a synthetic ceiling, not a differentiator. Segment on the *behaviours underneath it*: online_spend_ratio (0–95% spread), category_diversity, and consistency of activity.
2. **Category diversity is the master signal (r = 0.94).** A falling category count is the earliest, cleanest flag that a customer is disengaging — build the churn/health early-warning on it, not on the composite score.
3. **Two distinct at-risk tails, two different playbooks.** The 25 high-health/low-engagement are a **reactivation** problem (win back everyday offline use). The 67 low-health/low-engagement are a **wellbeing-intervention** problem (Task 5). Same low engagement, opposite remedies — do not merge them.
4. **Digital is broad but shallow.** Non-POS is 41% of trips and of value, but truly online (E-com + Mobile) is only ~17% of value and concentrated in Emerging Digital — grow online depth, not just QR reach.

---

## Deep-dive (27/09) — `draft/task3_deep.py`, output in `task3_deep_output.txt`

- **D1 shares per segment (consumers, modal month):** Low **1.0%** (10) · Medium **8.0%** (80) · High **74.1%** (740) · Very high **16.9%** (169). Chart: `t3_segment_share.png` (bar, not pie — a pie hides the 1% tail).
- **D2 online share & who is digital.** Average online spend share **24.7%** (consumer level; 21.0% month level). By Task 4 segment, Emerging Digital sends **60.5% of spend through E-commerce + Mobile App** (34.3% + 26.2%) vs ~17% for the other three segments, whose channel mix is near-identical (POS ~58–59%).
- **D3 diversity.** 908/999 consumers average 13–14 categories; the tail ≤8 is only 91. Excluding the tail, r(diversity, engagement) is still **+0.81** (Spearman on all +0.85) — the +0.94 is not a tail artefact. Chart: `t3_diversity_hist.png` (log y keeps the tail visible).
- **D4 recency × frequency heatmap.** Engagement peaks at 30–31 active days & recency 0 (79.8, n=6,614); every 1–5-active-day cell stays ≤55 whatever the recency → consistency of activity matters more than recency. Chart: `t3_recency_frequency.png`.
- **D5 cutoff justification.** FHS≥70 & engagement<60/65/70 all give **25** consumers (a natural gap in the data); engagement<75 jumps to 63 as it reaches the main body; FHS≥65 gives 47–48, FHS≥75 gives 9. The 70/70 rule sits in the gap.
