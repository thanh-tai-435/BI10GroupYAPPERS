# Review — Task 2 (Financial Health), slides 9–12

Reproduce: `PYTHONUTF8=1 py draft/review/t2_recompute.py` (output in `draft/review/t2_recompute_output.txt`), charts: `PYTHONUTF8=1 py draft/review/t2_charts_v2.py`.
All numbers below come from that independent code (raw files only; nothing read from the team's intermediate CSVs).

**Grain key:** CM = consumer-month (n = 10,992) · C = consumer level, mean of each consumer's available months (n = 999) · TX = transactions joined to CM on consumer_id + month (1,852,394 rows, 0 unmatched).

---

## 1. Number check

### Slide 9 — D1

| Slide claim | Grain | Recomputed | Status |
|---|---|---|---|
| mean 66.3, median 66.2, std 4.7 | C | 66.30 / 66.24 / 4.67 | OK |
| IQR 63.4–69.3, range 42.3–80.8, skew −0.32 | C | 63.40–69.28 / 42.32–80.83 / −0.315 | OK |
| month std 9.5, "twice the consumer spread" | CM | 9.48 (2.03×) | OK |
| Stable 72.5 · Watch 22.4 · Healthy 4.3 · Stressed 0.9 % | CM | 72.5 / 22.4 / 4.3 / 0.9 | OK |
| "0 of 999 have a 12-month mean below 40" | C | 0 — **but only 908 consumers have 12 months; 86 have 1 month, 5 have 2** | WORDING |
| Feb 73.6 → Dec 54.2 | CM monthly mean | 73.6 / 54.2 | OK |

### Slide 10 — D2

| Slide claim | Grain | Recomputed | Status |
|---|---|---|---|
| r spend-to-income −0.90, utilization −0.86, volatility −0.50 | CM, Pearson | −0.898 / −0.862 / −0.496 | OK |
| stressed vs healthy spend/income 2.10 vs 0.29; utilization 0.58 vs 0.08 | CM (95 vs 475 months) | 2.098 vs 0.289; 0.582 vs 0.078 | OK |
| FHS 72.4 → 68.4 → 66.0 → 63.8 → 60.9 by STI quintile, −11.4 | **C** (not stated on slide) | 72.38 / 68.43 / 65.99 / 63.76 / 60.94; −11.44 | OK (grain missing) |
| "~10× the age spread" | C | 11.44 / 1.22 = 9.4× | OK |
| engagement stressed 81.1 vs healthy 72.7 | CM | 81.14 vs 72.74 (Welch p = 1e-13) | OK |

### Slide 11 — D3

| Slide claim | Grain | Recomputed | Status |
|---|---|---|---|
| 22 of 27 provinces (≥15 consumers) CI contains 66.3 | C, bootstrap | 22/27 | OK |
| "extremes Thai Nguyen 63.0, HCMC 67.6" | C | Thai Nguyen 62.98 is the min, but the **max is Ha Noi 67.82** (HCMC 67.59 is 3rd, after Tuyen Quang 67.65) | **MISMATCH** |
| all six age-cohort CIs overlap (65.8–67.0) | C | means 65.75–66.97; all pairwise CIs overlap | OK |
| 396 titles → 8 keyword groups | C | 396 titles; the map yields 8 groups **+ "Other" (45 consumers)** = 9 buckets | MINOR |
| Eng/sci/IT 69.1 (229), Business 68.7 (126), Office 64.5 (443), Manual 62.9 (23) | C | 69.13 (229), 68.65 (126), 64.50 (443), 62.94 (23) | OK |
| STI 0.60 vs 0.76–0.79 | C | 0.605 / 0.612 vs 0.756 / 0.793 | OK |

### Slide 12 — D4

| Slide claim | Grain | Recomputed | Status |
|---|---|---|---|
| p75 engagement = 81.4 | CM (all 10,992 rows, pandas linear quantile) | 81.4000 | OK |
| 43 consumers / 49 months / 52% of stress episodes | CM | 43 / 49 / 51.6% | OK |
| p70 / p80 → 44 / 41 consumers (53% / 48%) | CM | 44 / 41 (52.6% / 48.4%) | OK |
| spend/income 1.89, utilization 0.55, online share 0.49 "2× national" | CM | 1.890 / 0.548 / 0.486 vs 0.210 (2.3×) | OK |
| 22–23h: 23.5% of value vs 8.3%; count 11.6% vs 9.7% | TX | 23.5 / 8.3; 11.6 / 9.7 | OK |
| Sunday + Monday 42% vs 34% | TX, pooled value | 41.9 vs 34.0 | OK numerically — **not robust**, see §2 |

Also verified: `transaction_day_of_week` 0 = Monday, `transaction_hour` and `transaction_month` agree with `activity_datetime` on 100% of a 2,000-row sample.

**One mismatch, one wording error.** Everything else reproduces to the decimal.

---

## 2. Brief coverage and statistical issues

| Deliverable | Covered? | Gaps |
|---|---|---|
| D1 Distribution | Yes | "12-month mean" is wrong for 91 consumers with 1–2 months (they average 9 transactions per month vs 170). The existing histogram only shows the month level, so the "consumer band vs month spread" point is made in text, not in the chart. The strongest D1 fact is missing: **869 of 999 consumers (87%) fall below 60 in at least one month**. Consumer identity explains only 22% of month-level FHS variance and calendar month explains 25% (within-consumer std 8.4 vs between-consumer std 4.4), which is the quantitative proof of "episodic". Stressed months cluster in **Jan (21) + Dec (25) = 48% of 95**, a sharper fact than "Feb → Dec". |
| D2 Low-health factors | Yes | (a) STI and utilization correlate at r = 0.90 with each other, so they are **one factor** and should not be presented as two. Together they give R² = 0.82. (b) The slide says "directional, not causal", which is right; keep it. (c) Robustness is missing but holds: Spearman −0.95 / −0.87, and the **within-consumer** (demeaned) r is −0.90 / −0.89, so this is not only a between-person effect. (d) The quintile chart grain (consumer level) is not stated. A month-level threshold is more actionable: **97.9% of stressed months have spend > income**, and 99.3% of the 1,470 months with STI > 1 score below 60. (e) The transaction file is not used on D2, although the brief asks for category/merchant detail. Stressed months are 71.6% discretionary by value vs 40.5% healthy (transaction flag), and e-commerce + mobile-app take 23.2% vs 11.8% of value. |
| D3 Occupation / age / province | All three present | (a) Province: HCMC is labelled as the maximum, but Ha Noi is. (b) "Barely" is too strong for province. 5 of 27 CIs exclude the mean when about 1.4 would by chance, and ANOVA gives p = 0.009 (η² = 0.05; p = 2e-7 across all 34 provinces). The honest statement is that province gaps are real but **fully explained by spend-to-income** (ANOVA on STI-adjusted FHS p = 0.62; range 4.8 → 1.6 pts). (c) Occupation: η² = 0.22, the largest demographic effect. After STI adjustment the spread falls from 6.2 to 1.3 pts, which is the right proof of "acts through spending" and is currently shown only as an STI side-by-side. (d) The keyword map is coarse. "Office / public services" (443, 44%) is a catch-all: "nhà" catches scientists (Nhà hải dương học, Nhà sinh thái học), and lawyers and paramedics also land there. Say "rule-based keyword grouping; Office is a residual bucket". (e) Age: ANOVA p = 0.13, η² = 0.008, so "weak" is fine. Note that after STI adjustment the age spread slightly widens (1.2 → 1.7 pts, p = 3e-6), so do not claim "everything is spending" for age. (f) Multiple comparisons: 27 province CIs are read without correction. Use one omnibus test per dimension instead of counting CIs. (g) The 15×6.5 chart is squeezed into a 12.3×3.45 slot, so the 27-row province labels will be about 5 pt: illegible. |
| D4 Crossover rule | Rule stated; mostly precise | Missing for full reproducibility: (a) **how p75 is computed**: over all 10,992 consumer-months, pooled across months, pandas `quantile(0.75)` linear, which gives exactly 81.4. It is **not** consumer level (79.9) and not per month; freeze it as the fixed constant 81.4. (b) Boundaries: FHS **strictly** < 40, engagement **≥** 81.4 (inclusive, 64 months sit exactly at 81.4). (c) Consumer-level membership = any month meeting the rule. (d) Significance: under independence 25% of stress months would clear p75; the observed 51.6% gives binomial p = 2.5e-8. That is a real co-occurrence, but n = 49 months is small, so present the profile as an archetype. (e) All 43 crossover consumers are full 12-month consumers, and their other months average FHS 62.3: they are normal customers having a bad month. 14 of 49 crossover months are January. (f) **Sun+Mon is not robust**: the per-month median Sun+Mon share is 34.0% for stressed vs 33.6% for healthy months, and by count stressed months (37.2%) sit below mid months (38.3%). The pooled 42% comes from a few large months. Case §12 also says two source years were folded onto 2025, preserving month/day/time but **not the weekday**, so day-of-week is the least trustworthy timing cut. **Drop Sun–Mon; keep 22–23h**, which is robust: per-month median 23.0% vs 7.5% (Mann-Whitney p = 5e-8), monotonic across bands 8.3 → 10.2 → 14.0 → 23.5, and 51/95 stressed months above 20%. The category mix at 22–23h (transaction file) makes it actionable: online shopping 39%, in-store shopping 16%, travel 14%, other online services 12% (healthy late-night: home/utilities 20%, kids/pets 19%). (g) "Bigger late tickets" is shown in VND. Better as a ratio: the late-night median ticket is 0.95× the daytime ticket in stressed months vs 0.67× in healthy months. |
| Ethics | Good | The slides never use FHS for credit. Keep "never to deny credit, cut a limit or block" explicit on D4, because D4 names individuals. |

Other notes:
- The existing `t2_low_health_drivers.png` still charts `average_transaction_value_vnd`, a raw-VND field. Drop it or label it "(VND, magnitude only)" to respect the ratios-only rule.
- `draft/task2.py` carries a comment "panel is balanced (~11 mo/consumer)". That is false (908 × 12, 86 × 1, 5 × 2). Harmless for the means, but the "12-month" wording propagated to the deck and the findings.

---

## 3. Proposed slides (paste-ready for `build_deck.js`)

Constants reused: `SM`, `ST`, `SMT` as defined in build_deck.js.

### Slide 9 — D1 · `contentOne`
- **Title:** `Nobody is stressed on average, yet 87% dip below 60 at some point`
- **Bullets:**
  1. `Consumer level (average of each consumer's months, n = 999): mean 66.3, median 66.2, std 4.7, IQR 63.4–69.3, range 42.3–80.8 — a tight band.`
  2. `Month level (n = 10,992): std 9.5, 2× wider. Stable 72.5% · Watch 22.4% · Healthy 4.3% · Stressed (<40) 0.9% = 95 months across 70 consumers.`
  3. `0 of 999 average below 40, but 869 (87%) fall below 60 in at least one month; who you are explains only 22% of monthly variance, the calendar 25%.`
  4. `Stress peaks at year-ends: Jan + Dec hold 46 of 95 stressed months (mean FHS Feb 73.6 → Dec 54.2) → trigger support on the month, not a static list.`
- **Chart:** `v2_t2_distribution.png`
- **Stat box (optional):** `87% dip below 60 at least once`
- **Source:** `SM + " Consumer level = mean of available months (908 consumers have 12, 91 have 1–2)."`
- **Speaker note:** Averaging each person makes everyone look fine: the lowest consumer average is 42. Month by month, almost everyone has a bad month, and stress spikes in December and January. So the right unit for help is the customer-month, and the right trigger is this month's numbers.

### Slide 10 — D2 · `contentTwo`
- **Title:** `Low health is overspending: it breaks once spend passes income`
- **Bullets:**
  1. `One factor dominates (month grain, n = 10,992): spend-to-income r −0.90 and credit-utilization r −0.86 move together (r 0.90) and jointly explain 82% of FHS variance; also holds within each consumer (r −0.90).`
  2. `Threshold: 98% of stressed months spend more than income; in the top spend-to-income quintile (avg 1.21) 93% of months fall below 60, and none do in the bottom two quintiles.`
  3. `What they buy (transactions): stressed months are 72% discretionary by value vs 40% in healthy months, with 2× the e-commerce + app share (23% vs 12%). Stressed months are also MORE engaged (81.1 vs 72.7). Shared inputs → directional, not causal.`
- **Charts:** `v2_t2_sti_threshold.png` (left), `t2_low_health_drivers.png` (right; drop the VND bar if regenerated)
- **Source:** `SM + " Category mix: " + SMT`
- **Speaker note:** The two headline ratios are really one story, spending relative to capacity. The practical line is spend-to-income above 1: almost every stressed month crosses it. The transaction file shows the extra spend is discretionary and online, which tells us what a budgeting tool should watch.

### Slide 11 — D3 · `contentWide`
- **Title:** `Occupation and province gaps are really spending gaps; age is flat`
- **Bullets:**
  1. `Occupation (396 titles → 8 keyword groups + Other; consumer level): Eng/science/IT 69.1 (n = 229) and Business/finance 68.7 (126) vs Office/public 64.5 (443) and Manual/trades 62.9 (23), a 6.2-pt spread mirroring spend-to-income 0.61 vs 0.76–0.79.`
  2. `Province (27 with ≥ 15 consumers): Thai Nguyen 63.0 to Ha Noi 67.8; real but small (ANOVA p = 0.009, 5% of variance). Age: six cohorts within 65.8–67.0, not significant (p = 0.13).`
  3. `Hold spend-to-income constant and the occupation spread falls to 1.3 pts and province to 1.6 pts (p = 0.62). Target the ratio, never the group — the fair and more effective lever.`
- **Chart:** `v2_t2_demog_adjusted.png` (built for the wide 12.3×3.45 slot; keep `t2_demographics.png` as a backup/appendix)
- **Source:** `SM + " Consumer level, n = 999; adjustment = residual of FHS on spend-to-income (linear)."`
- **Speaker note:** All three cuts the brief asks for are here. Occupation shows the biggest gap, but the chart on the right shows it almost disappears once we account for how much people spend relative to income. The same holds for province. That is why the recommendations target behaviour, not demographics, which also avoids disadvantaging any region or job group.

### Slide 12 — D4 · `contentTwo`
- **Title:** `43 active customers carry 52% of stress episodes — reach them late evening`
- **Bullets:**
  1. `Rule (consumer-month): financial_health_score < 40 AND engagement_score ≥ 81.4, the p75 of all 10,992 consumer-months (fixed constant). Hits 49 months / 43 consumers = 52% of stressed months vs 25% by chance (p < 0.001); p70/p80 give 44/41 consumers.`
  2. `Profile: spend/income 1.89, utilization 0.55, discretionary 71%, online share 0.49 (2.3× the 0.21 average). All 43 are full-year customers averaging FHS 62 in their other months: normal customers in a bad month.`
  3. `When (transactions): 22:00–23:59 carries 23.5% of stressed-month spend value vs 8.3% healthy (count only 11.6% vs 9.7%), led by online shopping 39% and travel 14% → in-app spend alerts before 22:00. Wellbeing use only, never credit decisions.`
- **Charts:** `t2_crossover.png` (left), `v2_t2_latenight.png` (right)
- **Source:** `SM + " Timing: " + SMT`
- **Speaker note:** The rule has two fixed thresholds on monthly fields, so anyone can rerun it. More than half of all stress happens to customers who are already very active in our channels, so the channel to help them already exists. The transaction file tells us when (late evening, big online baskets), so a gentle alert before 22:00 is the intervention. We dropped the Sunday–Monday claim because it does not hold month by month.

---

## 4. New charts

| File | Slot | What it shows |
|---|---|---|
| `outputs/figures/v2_t2_distribution.png` | contentOne right (5.8×4.4) | Consumer-average vs consumer-month distributions overlaid; <40 and <60 lines with counts (95 months / 70 consumers / 0 on average; 869 of 999 below 60 once). |
| `outputs/figures/v2_t2_sti_threshold.png` | contentTwo (5.95×3.35) | % of months with FHS < 60 by month-level spend-to-income quintile: 0 / 0 / 1 / 22 / 93%, with mean FHS and % < 40. Replaces the consumer-level quintile bars with an actionable threshold view. |
| `outputs/figures/v2_t2_demog_adjusted.png` | contentWide (12.3×3.45) | Group-mean spread per dimension, observed vs STI-adjusted: age 1.2→1.7, province 4.8→1.6, occupation 6.2→1.3 pts. Three rows only, so it stays legible at slide size (unlike the 27-row province panel). |
| `outputs/figures/v2_t2_latenight.png` | contentTwo (5.95×3.35) | 22–23h share of spend value vs count across four FHS bands: value 8.3→10.2→14.0→23.5%, count 9.7→11.6%. |

All charts were generated at 150 dpi (top/right spines off, light grid, team palette) and inspected for legibility. Script: `draft/review/t2_charts_v2.py`. It reuses the occupation keyword map from `draft/task2_deep.py` by reading that file, so the groups match the deck exactly.
