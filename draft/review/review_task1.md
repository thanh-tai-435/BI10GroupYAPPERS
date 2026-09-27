# Review — Task 1 (EDA) slides 5–8

Reviewer recomputation: `draft/review/t1_verify.py` (output `draft/review/t1_verify_output.txt`) and `draft/review/t1_charts_v2.py`. I wrote both from scratch against the raw files: the monthly CSV and the transactions CSV inside the `.parquet/` folder. No `.gz` files were used, and all 999 consumers are kept, including the 7 minors aged 15–17.

Checks the data passes: 10,992 consumer-months, 999 consumers and 1,852,394 transactions. Every timestamp year is 2025. Transaction spend reconciles to monthly `total_spend_vnd`. Age never changes within a consumer, so assigning cohorts by month or by consumer gives identical groups.

---

## 1. Number check

| # | Slide | Claim on slide | My value | Status |
|---|---|---|---|---|
| 1 | 5 | Dec = 488.0B VND | 488.03B | OK |
| 2 | 5 | 15.04% of annual | 15.041% | OK |
| 3 | 5 | Annual 3.24T | 3.2446T | OK |
| 4 | 5 | Feb = 174.4B | 174.37B | OK |
| 5 | 5 | 5.37% | 5.374% | OK |
| 6 | 5 | 2.8× Feb | 2.799× | OK |
| 7 | 5 | Txn count +187% | +187.3% (97,657 → 280,598) | OK |
| 8 | 5 | Ticket −2.6% | −2.59% | OK |
| 9 | 5 | 1.74M vs 1.79M | 1.739M vs 1.785M | OK |
| 10 | 5 | "All 14 categories grow +181% to +193%" | This is **transaction count** growth (+181.2% to +192.7%). **Spend** growth ranges +145.9% to +233.5% | WORDING — say "transactions" |
| 11 | 5 | Caveat "treat 15% as directional" | Folding two years inflates the **absolute** VND in every month. The share (15.04%) and the 2.8× ratio are not biased by it | WORDING — the caveat points at the wrong number |
| 12 | 6 | Stressed: 95 months, 70 consumers | 95 / 70 | OK |
| 13 | 6 | 28.4% / 71.6% | 28.36 / 71.64 | OK |
| 14 | 6 | Healthy: 475 months, 303 consumers | 475 / 303 | OK |
| 15 | 6 | 59.5% / 40.5% | 59.46 / 40.54 | OK |
| 16 | 6 | Gradient 71.6 → 64.2 → 57.3 → 54.4 → 49.2 → **40.6** | 71.64 → 64.17 → 57.30 → 54.36 → 49.17 → **40.54** | **MISMATCH**: the ≥80 band is the same 475 months as "healthy", so it should read 40.5, as bullet 1 already says |
| 17 | 6 | FHS<35 vs ≥85: 73.5% vs 30.2% | 73.51 / 30.24 | OK |
| 18 | 7 | "**5** provinces" above-median spend and below-average digital | **6 qualify**. The 6th is Nghe An: 101.7B VND, digital 41.15% vs 41.18%, gap −0.03pp. `task1_deep.py` keeps only `.head(5)` | **MISMATCH** |
| 19 | 7 | POS 58.9–59.3% vs 58.8% | 58.85–59.27 vs 58.82 | OK |
| 20 | 7 | QR ~19.8–20.1% | 19.73–20.26 with Nghe An (19.73–20.12 without) | Minor — use 19.7–20.3 |
| 21 | 7 | E-com ~8.5%, Mobile ~7.5%, Recurring ~5% | 8.42–8.65 / 7.36–7.67 / 4.73–5.13 | OK |
| 22 | 7 | Largest gap −0.46pp (Dong Nai) | −0.455pp | OK |
| 23 | 7 | Digital value share 40.9–41.5% vs 41.5% | 40.91–41.51 (Nghe An 42.73) vs 41.46 | OK for the 5; Nghe An is outside the range |
| 24 | 7 | HCMC 13.6% of spend at 41.3% digital | 13.63% / 41.31% | OK |
| 25 | 7 | Cao Bang 43.1% (0.5% of spend) | 43.11% / 0.46% | OK |
| 26 | 7 | Quang Ngai 39.2% | 39.22% | OK |
| 27 | 7 | All 34 within 3.9pp | 3.88pp | OK |
| 28 | 7 | "Statistically real" gap | Province binomial z: Dong Nai −3.0, Ha Noi −2.4, Hung Yen −2.1, Hai Phong −1.7, Lam Dong −0.45, Nghe An −0.15. Only **3 of 6** reach p<0.05, before any correction for transactions clustering within consumers (5–135 consumers per province) | **OVERSTATED** |
| 29 | 7 | Stat box "≤ 0.46pp" | 0.455 | OK |
| 30 | 8 | Fuel & Transport 188,029 txns | 188,029 | OK |
| 31 | 8 | Avg ticket 1.59M | 1.587M | OK |
| 32 | 8 | 96.8% of consumers buy fuel | 96.80% (967/999) | OK |
| 33 | 8 | 17.3 per buyer-month | 17.34 | OK |
| 34 | 8 | Groceries 513.8B, ticket 2.92M | 513.77B / 2.916M | OK |
| 35 | 8 | 1.8× ticket | 1.84× | OK |
| 36 | 8 | 25–34: 178.7 txns/month | 178.75 | OK |
| 37 | 8 | Cohort median 177.8 | 177.80 | OK |
| 38 | 8 | Lowest FHS 65.8 (best 67.0) | 65.79 (55–64: 67.00) | OK at consumer-month grain |
| 39 | 8 | Spend-to-income 0.716 vs 0.700 | 0.716 / 0.6995 | OK |
| 40 | 8 | Essential 0.468 vs 0.481 | 0.468 / 0.4807 | OK |
| 41 | 8 | "CIs of all six cohorts overlap (65.8–67.0)" | Overlap confirmed (consumer-cluster bootstrap CIs span 64.9–67.6). The "65.8–67.0" in brackets is the range of point means, not the CIs | WORDING |
| 42 | 8 | (implicit) 25–34 is the lowest | If each consumer counts once rather than each consumer-month, **15–24 is lowest** (65.75 vs 65.79). ANOVA across cohorts p = 0.13 | NOT ROBUST — disclose |

**Summary:** 2 hard mismatches (#16 and #18), 1 overstated claim (#28), 1 non-robust ranking (#42) and 4 wording fixes (#10, #11, #20, #41). Every other number reproduces exactly.

---

## 2. Brief coverage

### Q1 — peak month
| Sub-question | Status | Gap / fix |
|---|---|---|
| Highest month + VND | Covered | — |
| % of annual | Covered | — |
| Compared to lowest month | Partial | Only the 2.8× ratio is given. Add the absolute gap (+313.7B VND) and the share gap (+9.7pp). |
| Count vs ticket | Covered | Make the decomposition explicit: in log terms, count explains 102.5% of the lift and ticket −2.5%. |
| What it reveals | Weak | The current slide says "Tết preparation", but nothing in the data shows that. What the data does show: active consumers are flat (919 → 918), so the peak is the **same customers** transacting 2.9× as often (106 → 306 txns per consumer). Feb's 28 days are not the explanation, because per-day spend is still 2.5×. December is also the **lowest-health month** (mean FHS 54.2 vs 73.6 in Feb), which gives a direct bridge to Q2 and Task 2. |
| Caveat | Wrong target | Reword: absolute volumes are inflated; shares and ratios hold. |

### Q2 — essential vs discretionary by health
| Sub-question | Status | Gap / fix |
|---|---|---|
| Proportions for stressed vs healthy | Covered | Fix 40.6 → 40.5 in the gradient. |
| What the composition reveals | Shallow | The slide says "stress re-allocates toward wants". The **mechanism** is missing, and it is the most useful new insight in this review: |
| | | • Essentials are the **same share of transactions** in both groups (46.3% stressed vs 47.8% healthy). The flip happens in **value**, not in habits. |
| | | • The average discretionary ticket is **3.94M vs 1.06M VND** (3.7×), while the essential ticket is flat (1.81M vs 1.69M). |
| | | • Transactions of 10M VND or more are 4.3% of stressed-month purchases but **54.4% of their value** (healthy: 0.36% of purchases, 3.3% of value). |
| | | • Travel alone shifts **+22.2pp** of value share (ticket 21.4M vs 0.6M), online shopping +11.1pp and in-store shopping +5.5pp. |
| | | • The result holds without travel: 37.1% vs 60.3% essential. |
| | | → Stress coincides with a few large discretionary purchases, not a daily drift. The lever is pre-purchase or large-ticket alerts. |
| Caveat to add (speaker note) | Missing | FHS is partly built from spend-to-income, so a large purchase mechanically lowers that month's FHS. Treat the link as directional, not causal. |

### Q3 — provinces with a digital gap
| Sub-question | Status | Gap / fix |
|---|---|---|
| 2 or more high-spend provinces below the average digital share | Covered but incomplete | 6 qualify, not 5. Add Nghe An, or say "top 5 of 6 by spend". |
| Channel breakdown POS vs digital | Covered | — |
| Quantify the gap | Covered | Drop "statistically real". Only 3 of 6 are significant, even on a naive test. |
| Explain the nature of the gap | Weak | The gap is **not** in QR, which is at par (−0.12 to +0.41pp vs national). **All 6 are below national on both E-commerce (up to −0.31pp) and Mobile App (up to −0.32pp).** The shortfall is in remote/app channels, not in-store digital. |
| Deliverable 3 — top-performing and lagging | Covered | HCMC, Cao Bang and Quang Ngai are shown. Stronger contrast to add: customers vary **8.7pp** (p10–p90 digital share 37.2–45.9%) against 3.9pp across all 34 provinces, so the lever is the customer, not the map. |
| Definition | Missing | "Digital" = non-POS (includes QR). `online_transaction_flag` excludes QR (national 21.3%). Under that definition Lam Dong drops out (+0.04pp) and the other gaps stay ≤0.6pp. State the definition on the slide. |
| Layout | Over budget | The slide has 5 bullets plus a stat box on contentOne (budget ≤ 4). |

### Q4 — top category by count vs by spend
| Sub-question | Status | Gap / fix |
|---|---|---|
| Top by count / top by spend | Covered | — |
| Compare tickets | Covered | 1.59M vs 2.92M, 1.8×. Medians agree (1.57M vs 2.63M), so the gap is not driven by outliers. |
| How usage differs | Covered | Add the share view: Fuel is 10.2% of transactions but 9.2% of value; Groceries is 9.5% of transactions but 15.8% of value. Both are essential and near-universal (96.8% / 99.3% reach). |
| Chart | Defect | In `t1_category_ticket.png` the Online Groceries bubble has no label. v2 labels every bubble and adds the overall-average line. |

### Q5 — vulnerable age cohort
| Sub-question | Status | Gap / fix |
|---|---|---|
| Cohort that is active with the lowest FHS | Covered | 25–34 clears the "active" bar by only 0.9 txn/month (178.7 vs 177.8). Say so. |
| Contrast essential ratio and spend-to-income | Covered | Add the contrast that explains the driver: 15–24 has an even lower essential ratio (0.355) but the lowest spend-to-income (0.676). 25–34 is the only cohort **above** national on spend-to-income **and below** it on essential ratio. |
| Honesty | Partial | Add ANOVA p = 0.13. Add the grain sensitivity: weighted per consumer, 15–24 ties at 65.75 vs 65.79. |
| Chart | Defect | In `t1_age_cohort.png` the FHS axis runs 64–68 with no CIs, which visually exaggerates a 1.2-pt spread. v2 shows means with 95% CIs next to the two ratios. |

### Deliverables
1. **Exact numbers:** met, with the fixes above.
2. **Decomposition:** met for count vs ticket. Strengthen with the log split and the consumers × frequency split. For essential vs discretionary, add the count-vs-value split.
3. **Top and lagging segments:** met for regions and categories.
4. **Business interpretation:** present. Q1 and Q2 interpretations get sharper with the new mechanisms above.

---

## 3. Proposed slides (ready to paste into `build_deck.js`)

Budget check (characters per bullet, measured): slide 5 ≤ 164; slide 6 ≤ 240; slide 7 ≤ 170; slide 8 ≤ 254. All titles ≤ 69.

### Slide 5 — Q1 (contentOne)
- **Title:** December = 15% of annual spend, driven by trip frequency, not tickets
- **Chart:** `v2_t1_q1_decomposition.png` (spend, txns per consumer, active consumers, ticket, indexed Feb = 100)
- **Stat box:** `["2.9×", "transactions per customer, Dec vs Feb"]`
- **Source:** `ST`
- **Caveat:** Case §12: two source years folded onto 2025 inflate absolute VND in every month; shares and ratios (15.04%, 2.8×) are the reliable signal.
- **Speaker note:** December is not new customers or pricier baskets. The same ~918 customers transact almost three times as often, even after adjusting for February's 28 days (per-day spend still 2.5×). That burst coincides with the year's lowest average health score (54.2), so the peak is also the pressure point we return to in Task 2.

```js
contentOne(++N, "Task 1 · EDA · Q1", "December = 15% of annual spend, driven by trip frequency, not tickets",
  ["Peak: December 488.0B VND = 15.04% of the 3.24T annual spend. Trough: February 174.4B = 5.37%. Gap +313.7B VND (+9.7pp): December is 2.8× February.",
   "Driver is count: transactions +187% (97,657 → 280,598) while the average ticket slips 2.6% (1.79M → 1.74M VND). Count explains the entire lift.",
   "Same customers, more trips: active consumers flat (919 → 918), transactions per consumer 106 → 306. All 14 categories grow +181% to +193% in transactions.",
   "Reveals: the peak is a burst of everyday frequency, and December is the weakest-health month (avg FHS 54.2 vs 73.6 in Feb) → plan budgeting support before December."],
  "v2_t1_q1_decomposition.png",
  { src: ST, stat: ["2.9×", "transactions per customer, Dec vs Feb"],
    cav: "Case §12: two source years folded onto 2025 inflate absolute VND in every month; shares and ratios (15.04%, 2.8×) are the reliable signal.",
    note: "December is not new customers or pricier baskets: the same ~918 customers transact almost three times as often, even per day (2.5x after adjusting for February's 28 days). That burst coincides with the year's lowest average health score (54.2), so the peak is also the pressure point we return to in Task 2." });
```

### Slide 6 — Q2 (contentTwo)
- **Title:** Stress flips the budget: 71.6% discretionary vs 40.5% when healthy
- **Charts:** `t1_essential_discretionary.png` (keep) + `v2_t1_q2_category_shift.png` (new; replaces `t1_discretionary_gradient.png`, whose numbers move into bullet 1)
- **Source:** `SMT`
- **Speaker note:** People under stress do not buy wants more often: essentials are about 47% of their transactions, exactly as for healthy customers. The inversion comes from a few very large discretionary tickets, above all travel. Because FHS partly reflects spend-to-income, read this as co-occurrence, not cause. It points to large-purchase alerts, never to restricting credit.

```js
contentTwo(++N, "Task 1 · EDA · Q2 — the spine", "Stress flips the budget: 71.6% discretionary vs 40.5% when healthy",
  ["Stressed months (FHS < 40; 95 consumer-months, 70 consumers): 28.4% essential / 71.6% discretionary. Healthy (FHS ≥ 80; 475 months, 303 consumers): 59.5% / 40.5%. A steady gradient across FHS bands: 71.6 → 64.2 → 57.3 → 54.4 → 49.2 → 40.5%.",
   "The flip is in value, not habits: essentials are ~47% of transactions in both groups, but the discretionary ticket is 3.9M vs 1.1M VND. Purchases ≥ 10M VND are 4.3% of stressed-month transactions yet 54% of their value (healthy: 0.4% → 3%).",
   "Travel alone adds +22pp of value share (ticket 21.4M vs 0.6M), online shopping +11pp; the mix stays inverted without travel (37% vs 60% essential). Stress = a few large discretionary purchases → pre-purchase alerts, not credit restriction."],
  "t1_essential_discretionary.png", "v2_t1_q2_category_shift.png",
  { src: SMT, note: "Stressed customers do not buy wants more often: essentials are about 47% of their transactions, exactly like healthy customers. The inversion comes from a few very large discretionary tickets, above all travel. FHS partly reflects spend-to-income, so read this as co-occurrence, not cause; it points to large-purchase alerts, never to restricting credit." });
```

### Slide 7 — Q3 (contentOne)
- **Title:** High-spend hubs trail digital by ≤0.46pp; geography is not the lever
- **Chart:** `v2_t1_q3_channel_gap.png` (pp gap per channel for the 6 qualifying provinces, with reference rows for HCMC, Cao Bang and Quang Ngai). Alternative: keep `t1_province_channel.png` and add Nghe An.
- **Stat box:** `["−0.46pp", "largest digital gap among high-spend hubs"]`
- **Source:** `ST`
- **Caveat:** Digital = non-POS incl. QR. On online_transaction_flag (excl. QR, national 21.3%) Lam Dong drops out; other gaps stay ≤ 0.6pp.
- **Speaker note:** Six high-spend provinces technically qualify. They lag only in app and e-commerce use, and by fractions of a point. Customers within any province differ far more than provinces do (8.7pp vs 3.9pp), so a regional digital campaign would miss the real variation. Target the individual customer's channel mix.

```js
contentOne(++N, "Task 1 · EDA · Q3", "High-spend hubs trail digital by ≤0.46pp; geography is not the lever",
  ["6 provinces combine above-median spend (> 82.7B VND) with below-average digital share (non-POS; national 41.2%): Ha Noi, Dong Nai, Lam Dong, Hung Yen, Hai Phong, Nghe An.",
   "Breakdown: POS 58.9–59.3% vs 58.8% nationally; QR at par (19.7–20.3% vs 19.9%). All 6 trail on both E-commerce (to −0.31pp) and Mobile App (to −0.32pp).",
   "Size: largest gap −0.46pp (Dong Nai); only 3 of 6 are significant (p < 0.05). Leaders: HCMC 13.6% of spend at 41.3%; range Cao Bang 43.1% → Quang Ngai 39.2%.",
   "Customers differ 8.7pp (p10–p90 digital share 37.2–45.9%) vs 3.9pp across all 34 provinces → drive digital adoption per customer, not per region."],
  "v2_t1_q3_channel_gap.png",
  { src: ST, stat: ["−0.46pp", "largest digital gap among high-spend hubs"],
    cav: "Digital = non-POS incl. QR. On online_transaction_flag (excl. QR, national 21.3%) Lam Dong drops out; other gaps stay ≤ 0.6pp.",
    note: "Six high-spend provinces technically qualify, but they lag only in app and e-commerce use, and by fractions of a point. Customers within any province differ far more than provinces do (8.7pp vs 3.9pp), so a regional digital campaign would miss the real variation. Target the individual customer's channel mix." });
```

### Slide 8 — Q4 & Q5 (contentTwo)
- **Title:** Fuel is the habit, groceries the wallet; 25–34 is weakest, barely
- **Charts:** `v2_t1_q4_category.png` + `v2_t1_q5_age.png`
- **Source:** `ST + " Age cohorts: consumer-month file; 95% CIs from 3,000 consumer-level bootstrap resamples."`
- **Speaker note:** Fuel and groceries are both near-universal essentials but serve different jobs: fuel is a frequent top-up, groceries a stock-up basket worth 1.8× more per visit. On age, 25–34 answers Q5 as asked: active, lowest score, highest spend-to-income. The whole cohort spread is only 1.2 points and is not statistically significant, so the actionable variable is spend-to-income, not age.

```js
contentTwo(++N, "Task 1 · EDA · Q4 & Q5", "Fuel is the habit, groceries the wallet; 25–34 is weakest, barely",
  ["Q4 — Top by count: Fuel & Transport, 188,029 txns (10.2%), avg ticket 1.59M VND, 17.3 buys per buyer-month; top by spend: in-store Groceries, 513.8B VND (15.8% of value), avg ticket 2.92M, 1.8× fuel. Fuel = frequent top-ups; groceries = stock-up baskets.",
   "Q5 — 25–34 has the lowest mean FHS (65.8 vs best 67.0) while staying active (178.7 txns/month vs cohort median 177.8). It is the only cohort above national spend-to-income (0.716 vs 0.700) AND below national essential ratio (0.468 vs 0.481).",
   "Honest limit: the cohort spread is 1.2 pts, 95% CIs overlap and ANOVA p = 0.13; counting each consumer once, 15–24 ties (65.75 vs 65.79). Age is a weak lever: target spend-to-income, not birth year."],
  "v2_t1_q4_category.png", "v2_t1_q5_age.png",
  { src: ST + " Age cohorts: consumer-month file; 95% CIs from 3,000 consumer-level bootstrap resamples.",
    note: "Fuel and groceries are both near-universal essentials but serve different jobs: fuel is a frequent top-up, groceries a stock-up basket worth 1.8x more per visit. On age, 25-34 answers Q5 as asked (active, lowest score, highest spend-to-income), but the whole cohort spread is 1.2 points and not statistically significant, so the actionable variable is spend-to-income." });
```

Check before pasting slide 8, bullet 2: "the only cohort above national spend-to-income AND below national essential ratio". The data supports it. Spend-to-income is above national (0.700) only for 25–34 (0.716) and 45–54 (0.712). Of those two, only 25–34 is below the national essential ratio (0.468 < 0.481); 45–54 is at 0.493.

### Knock-on edits outside slides 5–8 (for the lead to decide)
- Slide 2, exec summary: 71.6 / 40.5 is consistent. No change needed.
- `CLAUDE.md` says "No 'two years folded' caveat". The case study §12 explicitly says the two years were folded, so the caveat is legitimate. The reworded caveat above targets absolute VND, not the shares.
- If slide 6 drops `t1_discretionary_gradient.png`, the gradient numbers still appear in bullet 1.

---

## 4. New charts (`outputs/figures/`, made by `draft/review/t1_charts_v2.py`, 150 dpi)

| File | What it shows | Replaces |
|---|---|---|
| `v2_t1_q1_decomposition.png` | Four lines indexed to Feb = 100: total spend (Dec 280), transactions per active consumer (288), active consumers (100), average ticket (97). Shows that spend is fully explained by frequency. | `t1_monthly_spend.png` (dual axis; did not show the decomposition) |
| `v2_t1_q2_category_shift.png` | Value-share difference, stressed minus healthy, for each of the 14 categories, coloured essential/discretionary and annotated with the average ticket in each group. Travel +22.2pp (21.4M vs 0.6M ticket). | `t1_discretionary_gradient.png` (its numbers move into the bullet) |
| `v2_t1_q3_channel_gap.png` | Heatmap of the pp gap vs the national mix per channel for the 6 qualifying provinces, plus reference rows for HCMC (top spend), Cao Bang (most digital) and Quang Ngai (least). Makes the "E-com + Mobile App" nature of the gap visible. | `t1_province_channel.png` |
| `v2_t1_q4_category.png` | Bubble map (transactions × average ticket, size = spend) with every category labelled, both winners highlighted, and the overall average ticket line (1.75M). | `t1_category_ticket.png` (one unlabelled bubble) |
| `v2_t1_q5_age.png` | Left: mean FHS by cohort with 95% cluster-bootstrap CIs on an honest 60–70 axis. Right: spend-to-income and essential ratio by cohort against the national lines. | `t1_age_cohort.png` (truncated 64–68 axis, no CIs) |
