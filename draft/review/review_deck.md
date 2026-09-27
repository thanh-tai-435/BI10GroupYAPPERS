# Deck review: storyline, framing slides, cross-slide consistency

Reviewed: `draft/YAPPERS_BI10_R01.pptx` (22 slides, rendered to `draft/review/slide-NN.png`).
Checked against `draft/task*_output.txt`, `draft/task*_deep_output.txt`, and two quick recomputations on the raw data (`draft/review/check.py`, `check2.py`).

**Overall:** the numbers are almost all right and they reproduce. The real problems are four wrong claims (C1 to C4), one ranking that contradicts its own chart (C5), and a few words that overclaim. Once those are fixed, slide 2 can carry the whole deck.

---

## 1. Consistency issues

| # | Slides | Version A | Version B | Verdict / source |
|---|---|---|---|---|
| **C1 (wrong claim)** | 2 | "72% of Healthy→Stretched slides happen Nov→Dec" | 18: "a Healthy month is followed by a Stretched month 23% of the time — 72% from November to December"; 19: "Healthy → Stretched 72% Nov → Dec" | **Slide 2 is wrong.** task4_deep: the 72.4% is the *rate* for November-start months ("T11->T12 72.4%", yearly average 23.3%). It is not the share of all slides that fall in Nov→Dec. Correct wording: "72% of Healthy & Engaged customers in November slip into the Stretched profile in December (23% in an average month)." |
| **C2 (wrong claim)** | 19 footnote | "the crossover (43) and distress tail (67) are overlays inside the Stretched segment" | 15/17: 24 of 25 healthy-dormant customers are inside Emerging Digital | **Wrong.** Recomputed: crossover 43 = **39 Stretched + 4 Healthy & Engaged**. Distress tail 67 = **64 Emerging Digital + 3 Stretched**. So Education (67) overlaps almost entirely with Nudges (88), not with Budgeting. |
| **C3 (wrong evidence)** | 19 row ④ | Education target "Distress tail 67"; evidence "discretionary 72% vs 40% under stress" | The 67 are FHS<70 & engagement<70 at consumer level, mean FHS **62.5**. They are not stressed (FHS<40), and 64 of 67 are Emerging Digital | The evidence does not describe this group. The label "distress" overclaims when the mean FHS is 62.5. Use: "Low-health, low-engagement: 67 (6.7%), 64 of them in Emerging Digital". Evidence: "Emerging Digital 86.6% discretionary vs 54.6% base". |
| **C4 (overclaim)** | 15 title | "25 good customers **drifting away**" | Analysis is cross-sectional (yearly means) | No trajectory was measured, so "drifting" is unsupported. Use "25 healthy customers who barely use their card". |
| **C5 (contradiction)** | 20 | Text ranking "by reach × driver": Budgeting → Alerts → Reminders → **Products → Nudges** → Education | The slide 20 chart gives reach × driver ≈ Budgeting 272, Reminders 129, Nudges 83, Products 53, Alerts 37, Education 32. The slide 21 roadmap launches Nudges (31–60) before Products (61–90) | The text contradicts its own chart and the roadmap. Fix the text to Budgeting → Alerts → Reminders → **Nudges → Products** → Education, and say Alerts is lifted to #2 by severity (52% of stress months), not by reach × driver. |
| C6 | 19 vs 20 (and chart) | Reminders target "Power Users 258 + Healthy 351" | 20: "Reminders (258)"; bubble chart reach 258 | The KPI (Nov→Dec Healthy→Stretched 72.4%) is about the **Healthy 351**, so they cannot be dropped. Make slide 20 "Reminders (258 + 351)" and note that the chart plots only the primary 258. The alternative is to re-plot at 609. |
| C7 | 2, 19, CLAUDE.md | 2 and 6: 71.6% vs 40.5% | 19: "72% vs 40%" | Use **71.6% vs 40.5%** everywhere (task1 output). If you round, it becomes 72% vs 41%, not 40%. |
| C8 | 2, 12, 19, 22 | "52% of ALL stress **episodes**" (2, 12) | "52% of stress **months**" (19), "52% of all stress" (22) | Same fact (49 of 95 months). Use "**52% of all stress months**" everywhere. |
| C9 | 2 vs 18 | ARI 0.99 | ARI 0.988 | Fine as rounding. Keep 0.99 on slide 2 only. |
| C10 | 22 vs 18 | "4 **clean** segments" | 18: moderate silhouette 0.251, "three large segments form one continuum" | Slide 22 overclaims. Use "4 **stable** segments". |
| C11 | "Healthy" used 3 ways | healthy months FHS≥80 (6, 9, 10, 12) · "Healthy 4.3%" dataset band (9) · "Healthy & Engaged" k-means segment (17–20) | — | Always write "healthy months (FHS ≥ 80)" vs "Healthy & Engaged segment". The same applies to **Stressed** (FHS<40 month) vs **Stretched** (segment). "Stressed but Engaged" crossover and "Stretched but Highly Engaged" segment read as the same thing, so add a one-line distinction on slide 12. |
| C12 | 4, 5, 18, 22 vs CLAUDE.md | Deck: "two source years folded onto 2025 → volumes inflated" | CLAUDE.md: "No 'two years folded' caveat" | Case §12 does state the folding, so the **deck is right to cite it**. But slide 5 says "treat 15% as directional". Folding preserves month and day patterns, so the **15% share and the 2.8× ratio are the reliable part** and only absolute VND is inflated. Reword (see 5-S1). CLAUDE.md is out of scope for this review, but its line misleads. |

Verified correct (no action): 351/302/258/88 and percentages; 43 consumers / 49 months; p75 81.4 (month grain); 0.46pp; r −0.90 / −0.86 / −0.50; quintiles 72.4 → 60.9; Feb 73.6 → Dec 54.2; 15.04% December; 488.0B / 174.4B = 2.8×; non-POS 41.2% of trips / 41.5% of value; Emerging Digital 60.5% of spend via E-com + Mobile (34.3 + 26.2); 693 merchants; 34 provinces; 344/351 and 273/302 cross-check; silhouette 0.251 / k=2 0.557; bootstrap ARI 0.911; GMM ARI 0.26; PCA 41% + 32% = 73%; scenario 95 → 80 → 65 → 49; 25 dormant (flat from eng<60 to <70); gradient 71.6 → 40.6.

---

## 2. Compliance issues

**Sources and captions.** Every chart slide (5–21) has a source line. Two contain a doubled prefix:
- Slide 12: "…2025. Timing: Source: transactions file…" should read "…2025. Timing: transactions file…"
- Slide 13: "…2025. Channels: Source: consumer_transactions_2025…" should read "…2025. Channels: consumer_transactions_2025…"

**Claims without numbers.**
- Slide 22: "near-zero cost" has no number anywhere. Delete it.
- Slide 22: "reaching every customer" is only true through the 4-segment partition. Say "every one of the 999 through its segment".
- Slide 2: "explain almost all of financial health" is not supported. r −0.90 gives r² = 0.81, so say "explains ~81% of month-to-month variation".
- Slide 1: "one finding that reframes everything" is vague. Name the finding.

**Ethics (credit use of FHS).** Good overall: the rule appears on slides 2, 4, 18, 20, 22. Three risks:
- Slide 18 future work, "Chronological model for next_month_low_health_flag… as an early-warning": add "to offer help, never for credit decisions", because "early warning" reads as risk scoring.
- Slide 19 ⑥: "never auto-extend credit" is good. Also add "no offer depends on FHS".
- Slide 2 row 5 is fine. Also add that the tools are **opt-in**.

**Jargon without explanation.** A business audience will not follow these as written:

| Term | Slides | Suggested plain gloss (inline or in speaker notes) |
|---|---|---|
| ARI | 2, 18 | "agreement between two groupings, 1 = identical" |
| silhouette | 16, 18 | "separation score, 0 = overlapping, 1 = perfectly distinct" |
| p75 / p10 / p79 | 12, 15, 16 | "top 25% of engagement" / "bottom 10%" |
| GMM, PCA, z-scaled | 16, 18 | "alternative soft-clustering model" / "2-D projection of 8 features" / "standardised" |
| IQR, skew, CI, Spearman | 8, 9, 11, 14 | Keep, but add "95% range" wording on the CI |
| FHS | first use on slide 2 | Define: "financial health score (FHS, 0–100)" on slides 2 and 4 |

**Titles that do not state an insight.**
- 16 "Preprocessing, features and model choice"
- 17 "Four segments, side by side"
- 21 "Expected impact, measurement & a 90-day roadmap"
- 3 is the TOC, which is fine.

Replacement titles are in section 5.

**Overload (from renders).** 7, 12, 16, 17 and 18 are dense but readable, and 18 is the heaviest (4 bullets + chart + 2 boxes). Other issues:
- Slide 20 chart: the legend is drawn as three bubbles labelled "Track / Wellbeing / Growth" at x ≈ 170, so they look like three extra tools. This needs fixing in `make_charts.py`.
- Slide 12 chart: the in-plot annotation overlaps the dashed threshold line. Minor.

**Language and typos.**
- Slide 8 title "Age: active 25–34 is weakest — barely" is awkward. Replacement in 5-S3.
- Slide 16: "k-means over a pure 2×2: boundaries form across all 8 dimensions" is unclear. Replacement in 5-S8.
- Slide 4: "consumer-MONTH" should not be in caps.
- Spelling mixes British and US forms ("behaviour", "prioritization"). Pick one. British is the majority, so change "Prioritization" (slide 20) to "Prioritisation".

**Structure.**
- The 4 required sections are present (2 Exec, 3 TOC, 4 Intro, 5–21 Tasks), with 22 slides and 16:9.
- Slides 2 and 22 have no footer or slide number. Slide 2 should get one for consistency.
- The file still needs renaming to `[YAPPERS_<Leader>_BI10_R01]`.

---

## 3. Storyline

- **Slide 2.** It nearly gives the whole answer, but it has the C1 error and it merges Task 2 and Task 3 into one row, so Task 3 (engagement) has no finding of its own.
  - A judge wants **one row per task** plus the recommendation and the ethical rule. Five rows cannot do that, so merge by argument: Task 1 inversion, Task 2 driver + episodic, Task 3 engagement, Task 4 segments, Task 5 plan + rule. The proposal below does exactly that and still fits 5 rows.
  - The title "One inversion drives the whole story" sits under a first row about overspend. The proposal gives a title that answers the case in one line.
- **Slide 3.** The TOC matches the actual order: 5–8 T1, 9–12 T2, 13–15 T3, 16–18 T4, 19–21 T5.
  - **Yes, show slide numbers**, because they cost nothing and help judges navigate. Put them in the item text.
  - The closing slide 22 has no TOC entry. That is acceptable, but it can be folded into item 06.
- **Slide 4.** It is solid on framing and data quality, which is what the 15% data-quality criterion rewards.
  - Add the one quality fact that is missing: minors (7 aged 15–17) were kept.
  - Add engagement skew (§12). Doing this means merging two ✓ lines to stay at 7.
- **Slide 22.** It lands the "contract". It needs three changes:
  - Remove "clean" and "near-zero cost".
  - Mention the 90-day test.
  - Add the Power Users to the slogan, because the current line covers only 3 of the 4 segments.
- **Arc.** The sequence is Problem → spine (6) → driver (10) → who and when (12) → engagement nuance (13–15) → segments (16–18) → plan (19–21). This works.
  - The weakest joint is 15 → 16. Slide 15's dormant 25 needs a bridge line saying it becomes part of Emerging Digital.

---

## 4. Proposed slides 1–4 & 22 (paste-ready)

### Slide 1: Title
- **Title:** ITB CONSUMER WELLBEING & SEGMENTATION
- **Subtitle (italic):** Overspending, not low income, drives financial stress, and help can be timed to reach it
- **Line 1:** 999 consumers · 10,992 consumer-months · 1.85M transactions · calendar year 2025
- **Line 2:** Group YAPPERS  ·  BI10 Round 01  ·  September 2026
- **Notes:** "This is a wellbeing study, not credit scoring. In one line: people slide into stress because they overspend on wants, usually in specific months, and those months are predictable. So ITB can offer help at the right time and never touch anyone's credit."

### Slide 2: Executive Summary
- **Tag:** EXECUTIVE SUMMARY
- **Title:** Overspending, not low income, drives stress, and it is timed, reachable and fixable
- **Rows (label | sentence):**
  1. **T1 · The budget flips under stress** | In stressed months (FHS < 40) 71.6% of spend is discretionary vs 40.5% in healthy months (FHS ≥ 80). The share falls steadily across every FHS band, and December is 15% of annual spend.
  2. **T2 · Overspend drives low health** | Spend-to-income (r −0.90) and credit utilization (r −0.86) explain ~81% of the variation in the financial health score (FHS, 0–100). 0 of 999 customers are stressed all year: stress comes in episodes, and 43 highly engaged customers account for 52% of all stress months.
  3. **T3 · Engagement is high; consistency differentiates** | 91% of customers are High / Very-high engaged. Category diversity (r +0.94) and active days separate them, and 25 healthy customers barely use the card.
  4. **T4 · Four stable segments** | Healthy & Engaged 351 · Stretched & Engaged 302 · Digital Power Users 258 · Emerging Digital 88. All 999 customers are covered, and the groups come out the same across random seeds (agreement 0.99, where 1 = identical).
  5. **T5 · Six opt-in tools, one rule** | Lead with Budgeting (302) and Sun–Mon evening Spend Alerts (43), then a November planning reminder (72% of Healthy & Engaged customers slip into the Stretched profile in December). An illustrative 10% spend trim cuts stress months ~32%. FHS never denies, cuts, prices or blocks credit.
- **Notes:** "One row per task. Row 1 is the signal, row 2 the driver and timing, row 3 engagement, row 4 the segments, row 5 the plan and the ethical rule. The 81% is r² of −0.90. The 32% is a scenario, not a forecast; it is validated by holdout on slide 21."

### Slide 3: Table of Contents
- **Tag:** CONTENTS · **Title:** What this deck covers
- **Items (number | text):**
  - 01 | Introduction to the Case & data quality · slide 4
  - 02 | Task 1 — Exploratory Data Analysis · slides 5–8
  - 03 | Task 2 — Financial Health Analysis · slides 9–12
  - 04 | Task 3 — Customer Engagement Analysis · slides 13–15
  - 05 | Task 4 — Customer Segmentation · slides 16–18
  - 06 | Task 5 — Recommendations, Impact & Closing · slides 19–22
- **Notes:** "Four required sections: Executive Summary (2), Contents (3), Introduction (4), Task results (5–21). Each task follows the brief's question order."

### Slide 4: Introduction + data quality
- **Tag:** INTRODUCTION · **Title:** The case: understand wellbeing, never score credit
- **Bullets (4):**
  1. ITB, a Vietnamese consumer-finance company, wants to understand customers' financial wellbeing, spending and channel engagement, and to segment them. It does not want credit-risk decisions.
  2. We compare ratios and shares, never absolute VND: synthetic income, credit and balance amounts are inflated (case §12).
  3. Stress is measured per customer-month, because it comes and goes. Segments are measured per customer, as a yearly average profile.
  4. Process: data-quality checks → EDA → financial health → engagement → segmentation → recommendations. Every number reproduces from notebooks/full_pipeline.ipynb (in the data ZIP).
- **Stat cards (4):** 999 | consumers · 10,992 | consumer-months · 1.85M | transactions · 34 | provinces
  (The consumer-months card replaces merchants, because it is the grain used on 12 of 17 analysis slides. 693 merchants moves into data-quality line 3.)
- **Data-quality box.** Heading: "Data-quality checks — both files"
  1. ✓ 0 missing cells · 0 duplicate transaction IDs or consumer-months · 0 negative amounts
  2. ✓ Every timestamp falls in 2025; each consumer has 1–12 months (10,992 of 11,988 possible)
  3. ✓ 1 name and birth date per consumer; 1 name per merchant (693 merchants)
  4. ✓ Transactions reconcile 100% to monthly total_spend (10,992 / 10,992 months)
  5. ✓ 5 over-limit months (utilization 1.03–1.5, all FHS < 35) kept as real behaviour
  6. ✓ 7 minors (aged 15–17) kept and binned, not dropped
  7. ⚠ Synthetic caveats (case §12): two source years folded onto 2025 inflate volumes, and engagement is skewed high. Ratios and shares are the signal.
- **Ethical-rule box:** **Ethical rule** financial_health_score is a wellbeing indicator. It is never used to approve or deny credit, cut a limit, raise a rate or block an account. A low score only triggers help the customer can accept or ignore.
- **Notes:** "Two rules govern the deck: ratios over magnitudes, and wellbeing over credit. The data is clean. The only caveats are the synthetic ones the case itself documents, and we state them wherever they touch a number."

### Slide 22: Closing
- **Tag:** The contract
- **Headline:** Protect the stretched, plan with the active, activate the dormant, grow the healthy, without ever touching their credit.
- **Rows (label | sentence):**
  - **The spine** | Overspend drives poor health (r −0.90). Under stress the budget flips to 71.6% discretionary. Stress comes in episodes and peaks in December.
  - **The segments** | 4 stable segments (351 / 302 / 258 / 88) covering all 999 customers, each with its own opt-in tool.
  - **Lead action** | Budgeting for the Stretched 302, plus Sun–Mon evening Alerts for the 43 customers behind 52% of stress months. Every tool is measured against a randomised holdout within 90 days.
  - **Honest limits** | Synthetic data (two source years folded onto 2025, engagement skewed high), and segments sit on a continuum. Sizes are directional; conclusions rest on ratios.
- **Footer line (italic):** One guarantee: wellbeing help, never a credit decision.
- **Notes:** "Close on the contract. If a judge remembers three things: overspend, not income; timing, not a blacklist; help offered, never credit taken away."

---

## 5. Prioritized fixes, slides 5–21

### Must-fix (errors or contradictions a judge can catch)
- **M1 · Slide 19 footnote.** Replace with: "No double-counting: the 4 segments partition all 999 consumers. The overlays sit inside them: crossover 43 = 39 Stretched + 4 Healthy & Engaged; low-health, low-engagement 67 = 64 Emerging Digital + 3 Stretched."
- **M2 · Slide 19 row ④.**
  - Target: "Low-health, low-engagement: 67 (6.7%), 64 of them in Emerging Digital"
  - Evidence: "FHS < 70 & engagement < 70; Emerging Digital spends 86.6% on discretionary vs 54.6% base"
  - Also change "Crossover & distress tail" to "Crossover & low-health/low-engagement group" in the source line.
- **M3 · Slide 20 bullet 1.** Replace with: "Ranking: wellbeing need first, then reach × driver strength. ① Budgeting (302, |r| 0.90) → ② Alerts (43 customers behind 52% of stress months; ranked 2nd for severity, not reach) → ③ Reminders (258 + 351) → ⑤ Nudges (88) → ⑥ Products (351) → ④ Education (67)." Update CLAUDE.md or the findings order separately if the lead agrees.
- **M4 · Slide 20 chart** (`make_charts.py`, t5 prioritization). Remove the "Track / Wellbeing / Growth" pseudo-bubbles, or move them into a real legend. They read as three extra tools.
- **M5 · Slide 15 title.** Replace with: "High health, low engagement: 25 healthy customers who barely use their card"
- **M6 · Slide 18 bullet 3.** Replace with: "Monthly migration: 23% of Healthy & Engaged months are followed by a Stretched month; for November → December it is 72%." (This matches the proposed slide 2.)

### Should-fix (clarity and rubric points)
- **S1 · Slide 5 caveat.** Replace with: "⚠ Case §12: two source years folded onto 2025 inflate absolute VND volume. The 15% share and the 2.8× ratio are the reliable signal."
- **S2 · Slides 12 and 13 source lines.** Delete the second "Source:" (see section 2).
- **S3 · Slide 8 title.** Replace with: "Fuel is bought most often, groceries cost most; age barely moves health"
- **S4 · Slide 12.** Add a line under bullet 1: "Note: this crossover is a *month-level* flag (FHS < 40 & engagement in the top 25%). It is different from the Stretched & Engaged *segment* (302) on slide 17; 39 of the 43 sit inside it."
- **S5 · Slide 16 title.** Replace with: "From 10,992 months to 999 profiles: 8 ratios, k-means with k = 4"
- **S6 · Slide 17 title.** Replace with: "Four segments: one healthy, one stretched, one hyperactive, one dormant-digital"
- **S7 · Slide 21 title.** Replace with: "A 10% spend trim could cut stress months by a third, tested in 90 days"
- **S8 · Slide 16 bullet 4.** Replace with: "Why k-means, not a simple 2×2 split: real boundaries run across all 8 ratios. k = 4 by elbow plus the best separation score (silhouette 0.251, scale 0–1) within 4–6. k = 2 separates better (0.557) but merges the personas the case asks for. All 999 covered, 7 minors kept."
- **S9 · Slide 18 bullet 1.** Replace with: "Stability: re-running with 20 random seeds gives the same groups (agreement ARI 0.988, where 1 = identical); on 80% resamples ×50, ARI 0.911. An alternative soft-clustering model (GMM) agrees only 0.26: Emerging Digital is identical, and the three large segments form one continuum."
- **S10 · Slide 18 future work bullet 3.** Append: "…as an early prompt to offer help, never as a credit input."
- **S11 · Slide 12 bullet 1.** Replace "p75 (81.4)" with "the top 25% (≥ 81.4)", and "52% of ALL stress episodes" with "52% of all stress months".
- **S12 · Slide 19 row ② evidence.** Replace "engagement ≥ p75" with "engagement in the top 25%". Replace row ④ evidence as in M2.
- **S13 · Slide 20 title.** Change "Prioritization" to "Prioritisation", for consistent British spelling.

### Nice-to-have
- **N1 · Slide 9 bullet 2.** Rename the dataset band "Healthy 4.3%" to "Healthy (FHS ≥ 80) 4.3%", to avoid a clash with the Healthy & Engaged segment.
- **N2 · Slide 13 bullet 1.** Add "(91% High or Very high)" after the segment list, to tie it to slide 2.
- **N3 · Slide 7.** The chart label "Hai Phong" and the text are fine. Consider lowering to 4 bullets by merging bullets 2 and 3 to reduce density.
- **N4 · Slide 12 chart.** Move the in-plot annotation off the dashed threshold line.
- **N5 · Slide 2.** Add a footer or slide number for consistency with 3–21.
- **N6 · Speaker notes.** Add a one-line glossary (ARI, silhouette, p75, PCA) to the notes of slides 16 and 18, for the Q&A.
