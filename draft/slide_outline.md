# Slide Deck Outline — BI10 Round 01, Group YAPPERS

*16:9 · English · 18 slides (max 22) · Charts referenced by filename from `outputs/figures/`.*

> **Update 27/09 — deck is now 22 slides; `draft/build_deck.js` is the source of truth for slide text.** Four slides added: **8** Task 1 Q3 channel breakdown by province (`t1_province_channel.png`) · **12** Task 2 differences by province / occupation / age (`t2_demographics.png`) · **18** Task 4 validation & monthly migration (`t4_pca.png`) · **21** Task 5 impact, KPIs & 90-day roadmap (`t5_impact_scenario.png`). Slides 6, 7, 10, 11, 13, 14 gained a second chart from the deep-dives (`draft/taskN_deep.py`). Numbering below is the original 18-slide plan.
*Spine of the narrative: Q2's essential↔discretionary inversion + episodic stress → segmentation → the 6-tool plan.*
*Required 04 sections present: (1) Executive Summary = slide 2, (2) Table of Contents = slide 3, (3) Introduction to the Case = slide 4, (4) Analysis Results Tasks 1–5 = slides 5–17.*

---

## Slide 1 — Title
- **ITB Consumer Wellbeing & Segmentation — BI10 Round 01**
- Subtitle: *A non-punitive plan built on spending behaviour, not credit risk*
- Group YAPPERS · September 2026
- One-line hook: "999 consumers, 1.85M transactions — and one finding that reframes everything."
- Charts: none.
- Speaker note: Set the wellbeing frame from second one — this is customer understanding, never credit scoring.

## Slide 2 — Executive Summary
- **Overspend, not low income, drives poor health:** spend-to-income (r = −0.90) and credit-utilization (r = −0.86) explain almost all of financial health.
- **The budget mix inverts under stress:** stressed customers spend 71.6% discretionary vs healthy customers' 40.5% — the single strongest signal in the data.
- **Stress is episodic, and hits the most engaged:** 0/999 chronically stressed; the "Stressed but Engaged" crossover = 43 consumers / 49 months = 52% of ALL stress episodes.
- **Four actionable segments** (k-means, k=4, 999/999 covered): sizes 351 / 302 / 258 / 88.
- **Headline recommendation:** a 6-tool wellbeing plan — lead with Budgeting (302) + in-app Spend Alerts (43); FHS is never used to deny/cut/block credit.
- Charts: none (text summary); optionally a small t4_segment_sizes.png thumbnail.
- Speaker note: If a judge reads only this slide, they get the whole story — inversion, episodic stress, 4 segments, 6 tools, ethical guardrail.

## Slide 3 — Table of Contents
- 1 · Introduction to the Case
- 2 · Task 1 — Exploratory Data Analysis
- 3 · Task 2 — Financial Health Analysis
- 4 · Task 3 — Customer Engagement Analysis
- 5 · Task 4 — Customer Segmentation
- 6 · Task 5 — Business Recommendations & Impact
- Charts: none.
- Speaker note: Show the arc — EDA and segmentation carry the most weight; recommendations are the payoff.

## Slide 4 — Introduction to the Case
- **Business context:** ITB, a Vietnamese consumer-finance company, wants to understand customer wellbeing, spending, and engagement — this is customer understanding & segmentation, **NOT** credit-risk decision-making.
- **Dataset:** 999 consumers · 1,852,394 transactions · calendar year 2025 · VND · two linked files (consumer-month + transaction level).
- **Synthetic-data caveat:** income/credit/balance magnitudes are inflated and not realistic — **we read ratios and shares, not absolute VND**, throughout.
- **Ethical framing (stated up front):** `financial_health_score` is a wellbeing measure, never used to deny credit, cut a limit, or block an account.
- **Method note:** distress analysed at the consumer-MONTH grain (episodic); "what kind of customer" analysed at consumer level.
- Charts: none.
- Speaker note: Plant the two rules that govern the whole deck — ratios over magnitudes, wellbeing over credit.

## Slide 5 — Task 1 · Q1: December is the spending engine, and it runs on frequency
- December = 488.03B VND = **15.04% of the 3.24T annual spend**; trough Feb = 174.37B (5.37%) → December is 2.8× the trough.
- Decomposed: transaction **count +187%** peak-vs-trough, while **avg ticket falls 2.6%** (1.74M vs 1.79M).
- Consumers buy *more often*, not *pricier* — year-end / Tết-prep bunching.
- Implication: scale capacity, fraud monitoring and campaigns to transaction **volume**, not basket value.
- *Caveat: two source years folded onto 2025 (case §12) inflate monthly volume; the Dec uplift is uniform across 14 categories — treat 15% as directional.*
- Charts: **t1_monthly_spend.png**.
- Speaker note: Peaks are a frequency phenomenon — the lever is trip frequency, not upsell.

## Slide 6 — Task 1 · Q2: Financial stress flips the budget essential→discretionary *(the spine)*
- **Stressed (FHS < 40):** 28.4% essential / **71.6% discretionary** (70 consumers, 95 cons-months).
- **Healthy (FHS ≥ 80):** 59.5% essential / 40.5% discretionary (303 consumers, 475 cons-months).
- The composition **inverts completely** — low health co-occurs with a discretionary-heavy mix, not with people scraping by on necessities.
- This reframes the intervention: highest-leverage, non-punitive help = budgeting visibility on discretionary spend, **not** credit restriction.
- This single contrast is the strongest driver in the dataset — it anchors segmentation (Task 4) and recommendations (Task 5).
- Charts: **t1_essential_discretionary.png**.
- Speaker note: This is THE slide — every later decision traces back to this inversion.

## Slide 7 — Task 1 · Q3–Q5: Where the signal is NOT (geography, category rhythms, age)
- **Q3 — No regional digital divide:** national digital share 41.2%; every high-spend province within ±0.5pp (Hà Nội 40.9%, Đồng Nai 40.7%). Province is not a targeting lever.
- **Q4 — Two shopping rhythms:** Fuel = most frequent (188,029 txns, 1.59M ticket = engagement touchpoint); Groceries = top spend (513.77B, 2.92M ticket, 1.8× larger basket = value category).
- **Q5 — 25–34 is the vulnerability hotspot:** lowest FHS among active cohorts (65.8), highest spend/income (0.716), below-average essential ratio (0.468); 177 consumers.
- **Honest caveat:** age spreads only 65.8–67.0 across cohorts — a weak differentiator; behavioural ratios beat demographics.
- Charts: **t1_category_ticket.png**, **t1_age_cohort.png**.
- Speaker note: Two honest negatives (geography, age are flat) + one behavioural positive — target customers, not the map or the birth year.

## Slide 8 — Task 2 · Q1: Health is a tight band; distress is episodic, never chronic
- Consumer-level FHS: mean 66.30, std 4.67, range 42.32–80.83 — a narrow band around ~66 with a mild low tail.
- Segment shares (cons-months): Stable 72.5% · Watch 22.4% · Healthy 4.3% · **Stressed only 0.9%**.
- Decisive fact: only **95 of 10,992 cons-months** score FHS < 40, and **0 of 999 consumers** have a 12-month mean below 40 (lowest = 42.3).
- Monthly swing: mean FHS 73.6 (Feb) → 54.2 (Dec) — December's surge drags health system-wide.
- Implication: interventions must be **event-triggered on the current month**, not a static "high-risk list."
- Charts: **t2_fhs_distribution.png**.
- Speaker note: Nobody is chronically unhealthy — healthy people dip in specific months. Trigger on the month, not the person.

## Slide 9 — Task 2 · Q2: Low health is an overspend story
- Top FHS correlates: **spend_to_income −0.90**, **credit_utilization −0.86**, volatility −0.50, essential ratio +0.48.
- Stressed vs Healthy months: spend/income **2.10 vs 0.29**; credit-util **0.58 vs 0.08**; discretionary 0.71 vs 0.39 — the same inversion as Task 1 Q2.
- The counter-intuitive row: **stressed months are MORE engaged (81.1 vs 72.7, r = −0.30)** — distress and engagement move together.
- Demographics add nothing (age spread 1.2 pts, occupation too fragmented — 396 titles / max 10 each).
- Implication: score and alert on two ratios; reach the stressed through the channel they already use.
- *Caveat: FHS and essential/discretionary ratios share spend fields — directional, not causal proof.*
- Charts: **t2_low_health_drivers.png**.
- Speaker note: Two ratios are the whole game — and the stressed are active, not disengaged. That sets up the crossover.

## Slide 10 — Task 2 · Q4: The "Stressed but Engaged" crossover
- **Rule (reproducible, month grain):** FHS < 40 AND engagement ≥ p75 (81.40).
- **43 distinct consumers / 49 cons-months = 52% of ALL stress episodes.**
- Crossover profile: spend/income **1.89**, credit-util **0.55**, discretionary 0.71, **online 0.49** (2× national), engagement 88.6.
- These are active, digital, over-extended customers the bank **already reaches** — highest leverage, near-zero cost.
- Right nudge: non-punitive in-app spend-pacing / utilization alert in the stress month — never credit restriction.
- *Caveat: 49 months / 43 consumers is a small synthetic cell — a directional archetype, not a sized market.*
- Charts: **t2_crossover.png**.
- Speaker note: More than half of every stress episode happens to someone we can text right now for free — the #2 intervention target.

## Slide 11 — Task 3 · Q1–Q2: Engagement is saturated; digital is broad but shallow
- **Q1:** 99.0% of cons-months are "high"/"very high" engagement (mean 77.8); only 90 consumers (9.0%) fall below — the score does NOT segment the base.
- Consumer-level mean 75.4 < median 78.2 = left-skew; the story lives in the thin dormant tail (min 12.8).
- **Q2 — channel mix:** POS 58.8% · QR 19.8% · E-com 8.7% · Mobile 7.7% · Recurring 4.9% → digital share 41.2% of trips but only **21.0% of spend**.
- Digital handles many small tickets (QR); big baskets stay on POS. Grow digital *value*, not just reach.
- *Caveat: synthetic cards are engineered highly active — the 99% is partly an artefact, not an organic win.*
- Charts: **t3_engagement_dist.png**, **t3_channel_mix.png**.
- Speaker note: Don't segment on the engagement score — it's a ceiling. Segment on behaviours underneath it.

## Slide 12 — Task 3 · Q3–Q4: What actually discriminates — diversity & consistency
- **Q3 — category diversity is the cleanest signal:** range 2–14; correlation with engagement **+0.94 at consumer level**. The dormant tail is disengaged because it is *narrow* (4–6 categories) vs ~14 for the core.
- Diversity separates the dormant tail from everyone else — the best early-warning flag for disengagement.
- **Q4 — recency/frequency confirm the split:** engaged core transacts 28–30 of 31 days, near-zero recency; low tail = ~2 active days, 21-day recency, 7 txns.
- Consistency (active_days r = +0.59) beats raw volume (txn_count r = +0.40) as the engagement driver.
- Charts: **t3_diversity_vs_engagement.png**.
- Speaker note: A falling category count flags disengagement before the composite score moves — build the early warning on it.

## Slide 13 — Task 3 · Q5: High-health, low-engagement — a dormancy risk hiding in "healthy"
- **Cutoff: FHS ≥ 70 AND engagement < 70 (consumer level) → 25 consumers (2.5%).**
- Why 70: the same 25 return at eng < 65/68/70 — a natural gap; looser cutoffs bleed into the healthy-engaged core.
- Profile vs rest: FHS 74.0 vs 66.1; engagement 46.8 vs 76.1; category diversity **4.68 vs 13.15**; **online_spend_ratio 0.61 vs 0.24**; ~10 txns/mo on ~2 days.
- Tell: they haven't stopped spending — they moved it off this card to a narrow set of online use-cases.
- Play = **reactivation of everyday offline use**, NOT budgeting/credit help (they don't need it). Distinct from the 67 low-health/low-engagement distress tail.
- *Caveat: n=25, synthetic-inflated engagement — a cohort to watch, not a sized forecast.*
- Charts: **t3_health_vs_engagement_quadrant.png**.
- Speaker note: Two low-engagement tails, opposite remedies — reactivation (25 good) vs wellbeing intervention (67 stressed). Don't merge them.

## Slide 14 — Task 4 · Method & model selection
- **Grain:** aggregate 10,992 cons-months → 999 consumers (yearly mean = typical monthly profile).
- **8 z-scaled behavioural features** across 3 axes (health/stress, engagement, spending); demographics excluded (Tasks 1–2 showed they carry no signal).
- **Model: k-means**, chosen over a pure 2×2 so the data sets boundaries across all 8 dimensions.
- **k selection:** inertia elbow + silhouette over k=2–8 → **k=4** (silhouette 0.251); k=2 wins silhouette but collapses out the engagement/digital structure the case asks for.
- **Coverage: 999/999 assigned, all 7 minors retained — PASS.** 2×2 cross-check agrees on the poles and confirms k-means adds the Emerging-Digital group a 2×2 buries.
- Charts: **t4_silhouette.png**.
- Speaker note: Justify k=4 honestly — moderate silhouette is expected for behavioural continua; the 2×2 validates the poles.

## Slide 15 — Task 4 · The four segments
- **Financially Healthy & Highly Engaged — 351 (35.1%):** FHS 70.5, lowest spend/income 0.571, lowest util 0.148 → retain & grow value.
- **Financially Stretched but Highly Engaged — 302 (30.2%):** lowest FHS 62.6, highest spend/income 0.835, highest util 0.248, still engaged → the wellbeing priority.
- **High-Activity Digital Power Users — 258 (25.8%):** most active (251 txns/mo), most volatile (1.91) → monetise & monitor drift.
- **Low Engagement & Emerging Digital — 88 (8.8%):** near-dormant (9.7 txns/mo) but 67.1% online, 86.6% discretionary → activate; highest growth headroom.
- *Limitations: moderate silhouette; mean aggregation hides trajectory; synthetic single-year data — sizes are directional.*
- Charts: **t4_segment_sizes.png**, **t4_segment_profiles.png**.
- Speaker note: Segment 2 is the payoff of the spine — Task 1's 25–34 vulnerability made into an addressable 302-person segment.

## Slide 16 — Task 5 · The six-tool non-punitive action plan
- ① **Budgeting tools → Stretched-Engaged (302, 30.2%)** — "spend vs income this month" dashboard; hook = spend/income 0.835, driver −0.90.
- ② **Spend alerts → Stressed-Engaged crossover (43, 4.3% = 52% of all stress)** — event-triggered in-app pacing/utilization alert; free channel already open.
- ③ **Planning reminders → Digital Power Users (258, 25.8%)** — pre-December pacing; hook = volatility 1.91 (r −0.50).
- ④ **Education content → Distress tail (67, 6.7%)** — needs-vs-wants modules; hook = essential ratio +0.48; reaches the low-engagement group alerts can't.
- ⑤ **Digital nudges → Emerging Digital (88, 8.8%)** — onboarding + habit loops; hook = category diversity r +0.94.
- ⑥ **Product suggestions → Healthy-Engaged (351, 35.1%)** — savings/loyalty; hook = util 0.148 = headroom; opt-in, never auto-extend.
- Charts: **t5_target_sizes.png**.
- Speaker note: One tool per required type, each bound to an exact size and a real ratio — no generic ideas.

## Slide 17 — Task 5 · Prioritization & the ethical rule
- **Ranking (reach × driver strength):** 1) ① Budgeting (302, −0.90) → 2) ② Alerts (43, −0.86 + 52% of stress) → 3) ③ Reminders (258, −0.50) → 4) ⑥ Products (351, growth) → 5) ⑤ Nudges (88) → 6) ④ Education (67).
- Verdict: lead with **① Budgeting + ② Alerts** — the wellbeing mission; ③–⑥ layer growth on top.
- **No double-counting:** the four segments partition 999; crossover (43) and distress tail (67) are month-grain overlays inside segment ②, not new populations.
- **Ethical rule (absolute):** `financial_health_score` and any flag derived from it MUST NEVER deny credit, cut a limit, raise a rate, or freeze an account. Every tool is show / remind / suggest / alert — opt-in, dismissible. Credit runs on the bank's separate, governed risk models.
- **Fairness:** targeting on ratios, not demographics → structurally fair; monitor a mild male skew (56.6% vs 49.4%) without using gender as a lever.
- Charts: **t5_priority_ranking.png**.
- Speaker note: The rule is the deck's contract — a low score triggers help offered, never access removed.

## Slide 18 — Closing / Impact
- **The spine:** overspend (not low income) drives poor health, the budget inverts under stress, and stress is episodic — striking the most engaged customers.
- **The payoff:** 4 clean segments (351/302/258/88) and a 6-tool plan that reaches every customer with the right non-punitive touch.
- **Lead action:** Budgeting for 302 + real-time Alerts catching 52% of all stress episodes — highest reach × strongest driver, at near-zero channel cost.
- **Honest limits:** synthetic single-year data, flat geography/age signal, engineered engagement skew — sizes directional, conclusions robust on ratios.
- **One guarantee:** wellbeing help, never a credit decision.
- Charts: none (or a recap thumbnail of t4_segment_sizes.png).
- Speaker note: Close on the contract — we grew the healthy, activated the dormant, and protected the stretched, all without ever touching their credit.
