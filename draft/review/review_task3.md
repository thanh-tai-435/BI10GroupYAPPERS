# Review: Task 3 (Customer Engagement), slides 13–15

Every number below comes from my own code: `draft/review/t3_recompute.py` and `draft/review/t3_charts_v2.py`, plus a few scratch queries on the same raw files. Grain labels: **CM** = consumer-month (10,992 rows). **C** = consumer (999; each metric averaged over the consumer's months).

## The finding that changes the story

**The whole "low-engagement tail" is 91 consumers who used the card on only 1–2 days in all of 2025.**
- 908 consumers have 12 monthly rows. 86 have 1 row and 5 have 2.
- In the transactions file, each of these 91 has an activity span of ≤1 day across the whole year (max = 1 day).
- None of the 908 full-year consumers ever has a "Low" month. They have only 15 "Medium" months, and their lowest consumer-average engagement is 69.79.
- The 91 one-off consumers top out at 61.6. That gap (61.6–69.8) is the "natural gap" that slide 15 cites.
- All 25 people in the D5 group are one-off consumers: the group equals "one-off consumers with FHS ≥ 70".
- 88 of the 91 are exactly Task 4's "Emerging Digital" segment (88/88). This is outside Task 3, but the Task 4/5 owners should know.

What this means for the slides:
- D1–D4 correlations are mostly a two-cluster contrast (one-off vs full-year). They should also be shown within the 908 full-year consumers.
- "Drifting away" on slide 15 should become "went silent after a single 1–2-day burst". This is still a strong at-risk signal: 19 of the 25 bursts happened in Jan–Jul, so those people have been silent for 5+ months.

## 1. Number check

| Slide | Claim | Slide value | Recomputed | Status | Grain |
|---|---|---|---|---|---|
| 13 | engagement mean / median | 77.8 / 78.1 | 77.82 / 78.10 | OK | CM |
| 13 | IQR | 74.8–81.4 | 74.8–81.4 | OK | CM |
| 13 | Low / Medium / High / Very high consumers | 10 / 80 / 740 / 169 (1.0 / 8.0 / 74.1 / 16.9%) | Reproduces only with `s.mode().iloc[0]`. **68 consumers tie** (mostly 6 High / 6 Very high months), and the tie is broken alphabetically toward "cao". Other methods: median month segment gives 10/80/741/168; consumer-average score in the official 40/60/80 bands gives **10 / 80 / 668 / 241 (1.0 / 8.0 / 66.9 / 24.1%)**; `value_counts().idxmax` gives 8/82/710/199 | **FRAGILE**: the High/Very high split depends on the tie-break | C |
| 13 | (month shares, not on slide) | – | 0.1 / 0.9 / 64.2 / 34.8% (10 / 100 / 7,058 / 3,824) | – | CM |
| 13 | channel shares POS / QR / E-com / App / Recurring | 58.8 / 19.8 / 8.7 / 7.7 / 4.9 | 58.82 / 19.85 / 8.73 / 7.69 / 4.92 | OK | txn |
| 13 | non-POS share of trips / value | 41% / 41.5% | 41.18% / 41.46% | OK | txn |
| 13 | average online spend share | 24.7% (range 0–95%) | 24.71%, range 0.0–95.1% | OK, but **misleading**: CM mean is 21.0%, consumer median 20.4%, full-year consumers' mean 20.6% and range 12.2–36.0%. The one-off 91 average 65.4%, and they produce the whole 0–95% spread | C |
| 14 | diversity range | 2–14 | 2–14 (CM) | OK | CM |
| 14 | consumer mean diversity | 12.9 | 12.94 | OK | C |
| 14 | "908 of 999 at 13–14" | 908 | **880** average ≥13; **908** average ≥12.5 (= the full-year consumers, range 12.5–14.0) | **MISMATCH** | C |
| 14 | r(diversity, engagement) | +0.94 | +0.938 (C); +0.590 (CM) | OK | C |
| 14 | "still +0.81 without dormant tail (Spearman +0.85)" | +0.81 / +0.85 | Pearson without tail +0.811 (OK). Spearman without tail = **+0.793**. The +0.845 is Spearman on **all** consumers | **MISMATCH** (mislabelled) | C |
| 14 | recency 0–30 d, median 0 | 0–30, 0 | 0–30, 0 | OK (full-year consumers: 0–4 d) | CM |
| 14 | active days 1–31, median 30 | | 1–31, 30 | OK (full-year: 15–31) | CM |
| 14 | transactions 2–713, median 150 | | 2–713, 150 | OK | CM |
| 14 | r with engagement: active days +0.59 > recency −0.42 > count +0.40 | | Pearson +0.589 / −0.424 / +0.404 OK. **Spearman reverses the order:** count +0.499 > active days +0.423 > recency −0.216 | OK as Pearson; the "consistency beats volume" ranking is **not robust** | CM |
| 14 | heatmap 30–31 days & recency 0 → 79.8, n = 6,614 | | 79.8, 6,614 | OK | CM |
| 14 | every 1–5-active-day cell ≤ 55 | | 54.9 / 54.8 / 52.8 / 43.6 | OK | CM |
| 15 | FHS ≥ 70 ≈ p79, top 21% | | 211 consumers; 70 = p78.9 | OK | C |
| 15 | engagement < 70 below p10 = 71.1 | | p10 = 71.06 | OK | C |
| 15 | group size | 25 (2.5%) | 25 (2.5%) | OK | C |
| 15 | engagement < 60 / 65 / 68 / 70 / 72 / 74 / 75 | 25 / 25 / 25 / 25 / 36 / 52 / 63 | same | OK | C |
| 15 | FHS ≥ 65 / ≥ 75 | 48 / 9 | 48 / 9 (also ≥68: 34, ≥72: 19) | OK | C |
| 15 | profile: FHS, engagement | 74.0 vs 66.1, 46.8 vs 76.1 | 74.03 vs 66.10, 46.83 vs 76.14 | OK | C |
| 15 | transactions / month, active days, recency | 9.9 vs 159, 2.0 vs 27.0, 14.3 vs 0.9 | 9.92 vs 159.06, 2.00 vs 27.04, 14.28 vs 0.91 | OK | C |
| 15 | diversity, online share | 4.7 vs 13.1, 0.61 vs 0.24 | 4.68 vs 13.15, 0.606 vs 0.238 | OK | C |
| 15 | 24 of 25 in Emerging Digital | | 24 (+1 Healthy & Engaged) | OK | C |

Missing from the profile and worth adding (C grain, group vs rest):
- age 61.3 vs 49.8
- discretionary share 0.79 vs 0.54
- spend-to-income 0.46 vs 0.70
- credit utilization 0.12 vs 0.19
- women 14 of 25
- each has exactly 1 month of data
- channel mix of their 248 transactions: POS 44.8%, E-commerce 21.8%, Mobile App 17.7%, QR 13.3%, Recurring 2.4%

## 2. Brief coverage

| Deliverable | Status | Gap or weak reasoning |
|---|---|---|
| D1: distribution + share in **each** segment | Partial | The histogram is at CM grain, but the segment shares are at C grain using a modal rule that ties for 68 consumers. The slide never says why it uses consumer grain. Also, the 100% stacked bar inside `t3_engagement_dist.png` makes Low (0.1%) and Medium (0.9%) invisible. **Fix:** give both grains in one chart (official 40/60/80 bands on the histogram). Label months as the native grain (segments are assigned monthly) and consumers by average score in the same bands, so there is no tie-break. |
| D2: 5-channel breakdown + average online share | Covered, but thin on "adoption" | The slide gives share of transactions only. "Adoption" is naturally the share of **consumers** who use each channel: POS 100%, E-com 99.0%, App 98.1%, QR 97.6%, Recurring 94.3%; 925/999 use all five. The online-share average (24.7%) is inflated by the 91 one-off users, and so is the 0–95% range. Quote the 21.0% month average and the 20.4% consumer median, and the full-year spread of 12–36%. Link to engagement: within full-year consumer-months, online share has r +0.86 with engagement (consumer grain +0.59). That is the strongest correlate among active customers, and it matches case §12. |
| D3: diversity range + link | Covered | The "908 at 13–14" figure is wrong (880). The Spearman label is wrong. The +0.94 is a two-cluster effect; lead with the within-base +0.81. |
| D4: recency and frequency ranges + links, **both** | Covered | Ranges are given only at CM grain. Add that the full-year base has recency 0–4 d and active days 15–31: recency only separates one-off users. The Pearson-based ranking claim "consistency > volume" flips under Spearman. Soften it to "activity (days and count) matters; recency only flags the one-off tail". |
| D5: exact size, profile, cutoff, why not stricter/looser | Covered numerically, **mis-explained** | The "natural gap" is real, but it exists because every engagement < 70 consumer is a one-off user. Say that; it is the actual justification. "Drifting away" is unsupported: we see one burst, not a decline. Missing profile: age 61 and one data month each. The FHS side of the sensitivity is given (≥65: 48, ≥75: 9) but not argued. Argue that ≥70 matches top ~21% / the "healthy" segment edge, while ≥75 shrinks the group to 9, too few to action. |
| D6: fitting chart type | Mostly OK | Histogram and heatmap fit. The single-column 100% stacked bar is the wrong type for shares with 0.1% / 0.9% slices, and the 3-chart squeeze makes it unreadable. The diversity scatter should colour the two clusters, otherwise r = 0.94 looks like a linear relation. The quadrant needs the cutoff-sensitivity evidence on the chart. |

## 3. Proposed slides (paste-ready)

`SM`, `ST` and `SMT` are the existing source constants in `build_deck.js`.

### Slide 13: contentTwo (was contentThree)

```js
contentTwo(++N, "Task 3 · Engagement · D1–D2", "Engagement is saturated; digital share is what varies",
  ["D1: engagement_score mean 77.8, median 78.1, IQR 74.8–81.4 (consumer-month). Segments are assigned monthly: Low 0.1% · Medium 0.9% · High 64.2% · Very high 34.8% of months. Per consumer (average score, same 40/60/80 bands): 1.0% · 8.0% · 66.9% · 24.1%.",
   "All 91 consumers below 'High' used the card on only 1–2 days all year; every one of the 908 full-year consumers averages ≥ 69.8. The score separates one-off users from the base, not good customers from great ones.",
   "D2: POS 58.8% · QR 19.8% · E-commerce 8.7% · Mobile App 7.7% · Recurring 4.9% of trips; 925/999 use all 5. Avg online spend share 21.0% (consumer median 20.4%, full-year range 12–36%); it tracks engagement (r +0.86, full-year months)."],
  "v2_t3_engagement_segments.png", "v2_t3_channel_mix.png",
  { src: SM + " Channels: " + ST, note: "Engagement is table stakes: 99% of months are High/Very high. What differs between active customers is how much of their spend is digital." });
```

Speaker note: "The histogram shows the continuous score. Shading the official 40/60/80 bands answers the share-per-segment question on the same axis, at both month and consumer grain, so the 1% tail stays visible where a stacked bar or pie would hide it. Channels are nominal, so we use a sorted horizontal bar, labelled with trip share, value share and the share of consumers who adopted each channel. Among active customers the online spend share, not the saturated score, is the lever."

### Slide 14: contentTwo

```js
contentTwo(++N, "Task 3 · Engagement · D3–D4", "Breadth and regular use track engagement; recency flags one-offs",
  ["D3: category diversity ranges 2–14 per month; the 908 full-year consumers average 12.5–14, the 91 one-off users 2–7. r = +0.94 across all consumers, and still +0.81 within the full-year base (Spearman +0.79), so breadth matters beyond the tail.",
   "D4: recency 0–30 days (median 0), active days 1–31 (median 30), 2–713 transactions per month (median 150). Full-year consumers: recency ≤ 4 d, active days 15–31. Links (consumer, full-year): active days r +0.80, count +0.76, recency −0.58.",
   "Heatmap: 30–31 active days & recency 0 → engagement 79.8 (n = 6,614 months); every 1–5-active-day cell stays ≤ 55. Low recency alone does not lift a one-off user above 55."],
  "v2_t3_diversity_engagement.png", "t3_recency_frequency.png",
  { note: "Watch category breadth and active days, not recency: recency only moves once a customer has already gone quiet." });
```

Speaker note: "Diversity and engagement are both continuous, so a scatter fits. Colouring the one-off users shows the r = 0.94 is two clusters, and the within-base r = 0.81 shows the link holds anyway. Recency × frequency is an interaction of two binned variables, so a heatmap of mean engagement with cell counts fits. It shows that consistent daily use is where the high scores sit."

### Slide 15: contentOne

```js
contentOne(++N, "Task 3 · Engagement · D5", "25 healthy customers used the card on only 1–2 days all year",
  ["Cutoff: FHS ≥ 70 (top 21%, p79) AND engagement < 70 (below consumer p10 = 71.1) → 25 consumers = 2.5% of the base, 11.8% of the 211 healthy.",
   "Why 70: one-off users score ≤ 61.6, full-year consumers ≥ 69.8, so cutoffs 60–70 all give 25; < 72 / 75 add active users (36 / 63). FHS ≥ 65 → 48 (not clearly healthy), ≥ 75 → 9.",
   "Profile vs rest: 2.0 vs 27.0 active days · 9.9 vs 159 txns/month · diversity 4.7 vs 13.1 · online 0.61 vs 0.24 · age 61 vs 50 · spend/income 0.46 vs 0.70.",
   "19 of 25 went silent in Jan–Jul and stayed silent 5+ months. 24 of 25 are Emerging Digital → play = win back everyday use, not budgeting."],
  "v2_t3_quadrant.png",
  { fs: 12, cav: "n = 25, one month of data each: FHS is a single reading. A watch-list, not a sized forecast. Never used to limit credit.",
    note: "The inset answers 'why not stricter or looser': the group size is flat from 60 to 70, then grows as the cutoff enters the active base." });
```

Speaker note: "Health and engagement are two continuous scores, so a quadrant scatter with the two cutoffs drawn in is the natural chart. The shaded empty band between 61.6 and 69.8 and the inset sensitivity curve show that the 70 cutoff sits in a real gap in the data rather than an arbitrary line. These are not stressed customers: they are healthy, older, low-spend users whose single burst of activity was mostly digital. The play is reactivation."

## 4. New charts (`outputs/figures/`, 150 dpi, from `draft/review/t3_charts_v2.py`)

| File | Replaces | Type and why |
|---|---|---|
| `v2_t3_engagement_segments.png` (7.2×4.05 in, contentTwo) | `t3_engagement_dist.png` + `t3_segment_share.png` | A single-panel histogram coloured by the official segment bands, with month and consumer share printed per band and an arrow to the 110-month tail. One chart now covers all of D1. |
| `v2_t3_channel_mix.png` | `t3_channel_mix.png` | A sorted horizontal bar, labelled with trip share, value share and consumer adoption. Covers the "adoption" wording of D2. |
| `v2_t3_diversity_engagement.png` | `t3_diversity_vs_engagement.png` | A scatter that colours full-year vs one-off users and prints both correlations (all consumers, within the base). |
| `v2_t3_quadrant.png` (7.2×5.46 in, contentOne) | `t3_health_vs_engagement_quadrant.png` | A quadrant scatter that marks the empty 61.6–69.8 gap, colours the other one-off users, and adds an inset showing group size vs engagement cutoff. |
| (keep) `t3_recency_frequency.png` | – | The heatmap is already the right type. |

The script ends with an assert that the group has 25 members, all from the 91 one-off consumers.
