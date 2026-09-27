# Review — Task 4 Customer Segmentation (slides 16–18)

Reviewer re-derivation, independent of `draft/task4.py`:
- `draft/review/t4_recheck.py` → `t4_recheck_output.txt` (all slide numbers, migration, bias)
- `draft/review/t4_recheck2.py` → `t4_recheck2_output.txt` (months observed, channel mix, sensitivity)
- `draft/review/t4_charts_v2.py` → `outputs/figures/v2_t4_*.png` (5 charts)

Run each with `PYTHONUTF8=1 py <script>` (run `t4_recheck.py` before `t4_recheck2.py`, which reads its scratchpad CSV).

---

## 1. Number check

| Slide | Claim on slide | Recomputed | Status |
|---|---|---|---|
| 16 | 10,992 consumer-months → 999 consumers, 0 nulls | 10,992 → 999, 0 nulls | OK |
| 16 | 8 z-scaled features | same 8 | OK |
| 16 | Diversity / active days / recency excluded, "p75 = max" | diversity p75 = max = 14 and active days p75 = max = 31 hold. Recency p75 = **0 = min**, not max | WORDING (say "p75 = best value") |
| 16 | k = 4 silhouette 0.251; k = 2 0.557 | 0.2508 (n_init 10 scan) / 0.2510 (final); k = 2 0.5574 | OK |
| 16 | "k = 4 via elbow" | inertia 5212 → 3720 → 3228 → 2880: the only bend is at k = 3. CH peaks at k = 3 (572 vs 490 at k = 4) | WEAK (no elbow at 4) |
| 16 | Coverage 999/999, 7 minors kept | 999/999; 7 consumers aged 15–17 (6 High-Activity, 1 Healthy) | OK |
| 17 | Healthy 351 (35.1%), FHS 70.5, S/I 0.571, util 0.148 | 351, 35.1%, 70.49, 0.571, 0.148 | OK |
| 17 | Stretched 302 (30.2%), FHS 62.6, S/I 0.835, util 0.248, engagement 76.5 | 302, 30.2%, 62.64, 0.835, 0.248, 76.52 | OK |
| 17 | Power Users 258 (25.8%), 251 txn/month (1.6× avg), volatility 1.91, engagement 80.2 | 258, 25.8%, 251.0 (1.62× of 155.3), 1.910, 80.16 | OK |
| 17 | Emerging 88 (8.8%), 9.7 txn, engagement 49.6, online 67.1%, discretionary 86.6% | 88, 8.8%, 9.74, 49.55, 0.671, 0.866 | OK |
| 17 | Essential-focused = 4; Healthy-but-Disengaged = 25, 24 in Emerging | 4 (3 Stretched, 1 Healthy); 25 (24 Emerging, 1 Healthy) | OK |
| 18 | Seed ARI 0.988 (20 seeds) | mean 0.988, min 0.931 | OK |
| 18 | Bootstrap 80% × 50 ARI 0.911 | mean 0.911, p5 0.843 | OK |
| 18 | GMM ARI 0.26; Emerging identical | 0.259; 88/88 in one GMM component | OK |
| 18 | 344 of 351 Healthy / 273 of 302 Stretched "in the matching halves" | 344 = 182 H+Disengaged + 162 H+Engaged; 273 = 110 S+Engaged + **163 Vulnerable+Disengaged** | NUMBERS OK, CLAIM MISLEADING (only the health half matches, see M4) |
| 18 | Healthy month → Stretched month 23% of the time | 23.0% pooled (23.3% mean of monthly rates) | NUMBER OK, METHOD FLAWED (M5) |
| 18 | 72% Nov → Dec | 72.4% | NUMBER OK, INTERPRETATION WRONG (M5) |
| 18 | Chi-square age & gender p < 0.01 | gender p = 0.0008 (Cramér's V 0.13); age p < 0.0001 (V 0.23), but 4/28 cells have expected count < 5. With 4 bins: p = 3e-19, V 0.19, min expected 18.9 | OK (use 4 bins + V) |
| 18 | PCA = 73% of variance (41% + 32%) | 41.0% + 32.3% = 73.3% | OK |
| 18 | Limitations: "two source years folded onto 2025" | Contradicts the project's own finding (CLAUDE.md: all timestamps are 2025, no two-years caveat) | MISMATCH, remove |
| 19 (knock-on) | "crossover (43) … overlays inside the Stretched segment" | 39 of 43 are Stretched, 4 are Healthy | MINOR MISMATCH ("39 of the 43") |

Every number on the slides reproduces. The problems are in labels and interpretation, covered below.

---

## 2. Method review (issue → fix)

**M1. Emerging Digital (88) is mostly a data-coverage group (critical).**
Months observed per consumer: 908 consumers have 12 months, 86 have 1 month, 5 have 2. The Emerging segment holds 83 of the one-month consumers and all 5 two-month ones; 0 of its members are full-year. A simple rule, "observed < 12 months", reproduces the cluster with ARI 0.978. Its profile follows from that: 1.1 months observed, 1.9 active days, recency 12.9 days, diversity 4.9. The k = 2 silhouette winner (0.557) is exactly this 88/89-vs-rest split, and the seed/bootstrap/GMM agreement on this group is trivially high for the same reason.
→ **Fix:** say it on the slide. Rename to **"Occasional Online-First"** (keep "maps to the brief's Emerging Digital") and add "months observed" as a profile column. Their FHS/engagement comes from about one month, so label it low-confidence. In the method bullet, describe the model honestly: the first split separates part-year customers, and the next two split the 908 full-year customers on health and on activity. Optional for a v2 model: a hybrid, with a rule for "< 12 months observed" and k-means k = 3 on the 908. With the same scaler this reproduces the current three large segments (ARI 0.860).

**M2. "Digital Power Users" is not more digital (naming).**
Online share is 21.2%, below the base average of 24.7% and level with Healthy (20.0%) and Stretched (20.8%). From the transactions file, non-POS share of value is 41.7% vs 40.9% / 41.3% for the other full-year segments, and online-flagged trips are 22.0% vs 20.9%. What does set them apart: 251 transactions/month (1.62× average), 30.2 active days, the highest volatility (1.91), 47.8% of months in the "very high" engagement band (vs about 30%), the youngest group (mean age 43), and 60% female. At k = 3 they split almost evenly into Healthy (134) and Stretched (124), so they form an activity axis, not a digital one.
→ **Fix:** rename to **"High-Activity Users"** and pitch the action as "keep heavy everyday usage healthy: volatility smoothing, instalment/budget caps opt-in". Drop "monetise" wording that reads like credit push.

**M3. "Highly Engaged" is not true in relative terms.**
Mean engagement is Healthy 77.4 and Stretched 76.5 against a base of 75.4. Share above the engagement median: Healthy 46.7%, Stretched 37.4%, High-Activity 87.6%. On the case's own `engagement_segment`, though, 99.8% and 99.6% of their months are "High" or "Very high".
→ **Fix:** use "Healthy & Engaged" / "Stretched & Engaged" (the chart labels already do). Justify it with the case's own bands ("99.6% of months in the High/Very-high engagement band"), not "highly".

**M4. The 2×2 cross-check is only half a match.**
344 of 351 Healthy sit above the FHS median and 273 of 302 Stretched below it, so the health axis agrees. On the engagement axis, 182 of 351 Healthy fall in "Disengaged" and 163 of 302 Stretched fall in "Vulnerable + Disengaged". Engagement is saturated (median 78.2) and does not separate these two groups.
→ **Fix:** restate as "health axis agrees (344/351, 273/302); engagement does not separate them (the median splits both), which is why k-means adds an activity axis instead". This is more honest and it justifies k-means over the 2×2 rule.

**M5. The monthly migration measures seasonality, not customer movement (method flaw).**
The method projects each monthly row onto centroids fitted on yearly means, using the yearly scaler. Monthly rows are about 2× as dispersed as yearly means (std ratio: FHS 2.03, spend-to-income 2.26), so assignments are noisy. Only 60.3% of consumer-months land in their own yearly segment (High-Activity only 45.2%). More importantly, month-level segment shares swing with the calendar: "Healthy" rows go from 81% in January to **1.7% in December**, and 77% of all December rows are labelled Stretched, because base-wide spend-to-income jumps from 0.65 to 1.25 and FHS from 67.5 to 54.2. After de-seasonalising (subtract each month's mean, add back the annual mean), the Healthy → Stretched rate is flat at 15–23% every month, 22.5% for Nov → Dec, with no spike.
→ **Fix:** replace "a Healthy month is followed by a Stretched month 23% of the time — 72% Nov → Dec" with a claim that holds: **"December cuts FHS by 12.8 / 14.1 / 13.4 pts in the Healthy / Stretched / High-Activity segments alike, a calendar effect, not a customer type. Year-end reminders go to all 908 full-year customers."** Chart: `v2_t4_monthly_fhs.png`. Knock-on: Task 5 row ③ on slide 19 cites "Healthy → Stretched 72% Nov → Dec". Use the parallel −13-point drop instead.

**M6. The choice of k is argued from preference, not from the data.**
"Best silhouette in the 4–6 range" is circular, and there is no elbow at 4.
→ **Fix:** argue from what each extra cluster separates (checked with crosstabs). k = 2 splits part-year from full-year customers. k = 3 splits the full-year customers on health (Healthy 350/351 vs Stretched 302/302). k = 4 splits off the activity axis (High-Activity 258). k = 5 and 6 only subdivide further (the 5th cluster splits existing segments; smallest clusters 49/39 at k = 6) with lower silhouette. Chart: `v2_t4_k_selection.png`.

**M7. Robustness beyond seeds is modest; say so.**
Seed and bootstrap ARIs test the optimiser, not the design. Design sensitivity (ARI vs the current labels): dropping December 0.873; adding FHS within-year SD + active days 0.870; median instead of mean aggregation 0.633; a reduced 5-feature set (dropping collinear spend/income, utilization, discretionary) 0.620; GMM on the 911 non-Emerging 0.181. Per-segment silhouette: Healthy 0.27, Stretched 0.22, High-Activity 0.19, Occasional 0.47. The three full-year segments are a continuum (908-only silhouette about 0.19 for any k).
→ **Fix:** one clause on slide 18: "robust to seeds, resampling and dropping December (ARI 0.87–0.99); feature and aggregation choices move about a third of assignments (ARI 0.62–0.63), so treat the three full-year segments as zones on a continuum, not hard types".

**M8. Feature redundancy and missing engineered features.**
The health block is triple-counted (FHS vs spend-to-income r −0.88, vs utilization −0.79; S/I vs utilization +0.72), and discretionary vs online is r +0.83. This is defensible because PCA confirms two axes (PC2 = health, PC1 = activity vs online/discretionary, 73% combined), but it should be stated. No engineered features were built (the brief lists them as optional). Cheap, relevant candidates, used as profile columns rather than as new model inputs:
- months observed
- FHS within-year SD (Healthy 7.7, Stretched 9.7, High-Activity 7.7, Occasional 17.1)
- any month with FHS < 40 (Stretched 20.2% of consumers vs ≤ 1.7% elsewhere)
- next-month low-health flag rate (Stretched 2.12% of months vs ≤ 0.05%)
- non-POS value share

→ **Fix:** add these to the profile heatmap (done in v2) and to `task4_features.csv` if the team wants to. Mention on slide 16: "health block collinear by design — PCA confirms two axes".

**M9. Bias check: report effect size and valid bins.**
Age with 7 bins has 4 of 28 cells with expected count < 5. Use 4 bins (15–34 / 35–49 / 50–64 / 65+): p = 3e-19, Cramér's V 0.19. Gender: p = 0.0008, V 0.13. The effect sizes are weak to moderate. The pattern: High-Activity is younger (33% aged 15–34, mean 43) and 60% female; Occasional is older (mean 58, 0% aged 35–49). Occupation reads V 0.71, but every cell has expected count < 5, so do not report it.

**M10. Visual consistency.**
The current PCA chart uses different colours from the size and profile charts (Emerging is green on slide 18 but amber on slide 17). → Use the v2 charts, which apply the fixed segment colours everywhere and label the centroids directly.

**M11. Brief checklist**

| Brief item | Status |
|---|---|
| Feature selection and engineering | OK (engineered ratios are optional; see M8) |
| Model selection and parameter justification | Weak (M6) |
| 100% coverage | OK |
| Validation of quality | OK, but over-sold (M4, M7) |
| Business labels | Two of four labels are misleading (M1, M2) |
| Side-by-side post-segmentation comparison with recommendations | Comparison present; the action per segment is thin |
| Limitations and future work | Present, but one false item (the "two years" caveat) |
| Preprocessed dataset deliverable | OK (`task4_features.csv` + data dictionary in the ZIP) |

Wellbeing framing: keep "never for lending" and add "segments never change limits or pricing".

---

## 3. Proposed slides (paste-ready)

Segment display names: **Healthy & Engaged**, **Stretched & Engaged**, **High-Activity Users**, **Occasional Online-First** (brief's "Emerging Digital"). Short forms: Healthy / Stretched / High-Activity / Occasional. If the team wants to keep the names used elsewhere in the deck (Task 5, CLAUDE.md), the minimum change is "Digital Power Users" → "High-Activity Users"; the Task 5 table (slide 19) must follow.

### Slide 16 — Method (contentOne, fs 12)

**Tag:** Task 4 · Segmentation · Method
**Title:** Three business axes, one model: coverage, health and activity (57 chars)

Bullets (4, each ≤ 170 chars):
1. `Preprocessing: 10,992 consumer-months → 999 consumers (yearly mean per ratio), 0 nulls, raw VND excluded; dataset + dictionary in ZIP (task4_features.csv).`
2. `8 z-scaled inputs: health (FHS, spend/income, utilization, volatility) · activity (engagement, transactions) · mix (discretionary, online). PCA: 2 axes, 73% of variance.`
3. `Excluded: essential (= 1 − discretionary); diversity, active days, recency (p75 already at best value). Demographics used for profiling only, never as inputs.`
4. `k-means k = 4: k=2 splits off part-year customers, k=3 adds health, k=4 adds activity; k≥5 only subdivides. Silhouette 0.25; coverage 999/999 incl. 7 minors.`

**Chart:** `v2_t4_k_selection.png`
**Source:** `Source: team k-means on 8 z-scaled ratios, consumer_financial_health_engagement_2025 (999 consumers, 2025).`
**Speaker note:** We cluster on ratios only, one row per customer, and keep demographics out of the model so the segments describe behaviour, not who people are. We did not pick k = 4 for taste: each added cluster separates a new business axis, and beyond four the model only subdivides existing groups. The first split is customers we see in only one or two months, the next two are health and activity.

### Slide 17 — Profiles (contentTwo)

**Tag:** Task 4 · Segmentation · Profiles
**Title:** Four segments, four different jobs for the product team (54 chars)

Bullets (3, each ≤ 260 chars):
1. `Healthy & Engaged 351 (35.1%): best FHS 70.5, lowest spend/income 0.57, utilization 0.15 → savings & opt-in product offers. · Stretched & Engaged 302 (30.2%): spend/income 0.84, utilization 0.25, 20% had a stress month → budgeting tool + spend alerts.`
2. `High-Activity Users 258 (25.8%): 251 transactions/month (1.6× avg), 30 active days, highest volatility 1.91; not more online (21% vs 25% avg); youngest (43), 60% female → volatility smoothing, year-end planning reminders.`
3. `Occasional Online-First 88 (8.8%) = brief's Emerging Digital: seen 1.1 of 12 months, 1.9 active days, 67% online, 75% of value non-POS → digital-channel nudges to build a habit; their scores rest on ~1 month (low confidence).`

**Charts:** left `v2_t4_sizes.png`, right `v2_t4_profile_heatmap.png` (give the heatmap the wider slot, about 60/40).
**Source:** `Source: team k-means (k=4), consumer-month file; non-POS share from consumer_transactions_2025 (1.85M transactions).`
**Speaker note:** The heatmap is the side-by-side comparison: top rows are model inputs, bottom rows are profile-only checks. Health splits Healthy from Stretched, activity isolates High-Activity, and the Occasional group is defined by how rarely we see them, not by being more digital. Each segment maps to one tool in Task 5, and none of them touches credit decisions.

### Slide 18 — Validation & limits (custom layout: bullets left, chart right, two boxes)

**Tag:** Task 4 · Segmentation · Validation & limits
**Title:** Stable where it matters, honest where it is thin (47 chars)

Bullets (4, 12 pt):
1. `Stability: 20 seeds ARI 0.988; 80% bootstrap × 50 ARI 0.911; dropping December ARI 0.873. Changing features/aggregation moves ~⅓ of labels (ARI 0.62–0.63).`
2. `Structure: Occasional is distinct (silhouette 0.47; = "seen < 12 months", ARI 0.98); 3 full-year segments form a continuum (0.19–0.27; GMM ARI 0.26) → zones, not types.`
3. `2×2 cross-check: health axis agrees (344/351 Healthy above FHS median, 273/302 Stretched below); engagement median (78.2) does not separate them → activity axis added.`
4. `December cuts FHS 12.8 / 14.1 / 13.4 pts in all 3 full-year segments alike → calendar effect: reminders for all 908. Age/gender differ (V 0.19 / 0.13) → act on behaviour.`

**Chart:** `v2_t4_pca.png`. Alternative: `v2_t4_monthly_fhs.png` if the team prefers to show the December finding; PCA better supports "validation".
**Caption:** `Source: team k-means (k=4), 999 consumers; PCA of 8 z-scaled features = 73% of variance.`

Box **Limitations** (3 lines, ≤ 110 chars each):
- `Moderate separation (silhouette 0.25); full-year segments are a continuum sensitive to feature choice.`
- `Yearly means hide trajectory; 91 customers seen < 12 months carry ~1-month scores (low confidence).`
- `Synthetic data, engagement saturated (median 78). Wellbeing groups only: never lending, limits or pricing.`

Box **Future work** (3 lines):
- `Hybrid model: rule for part-year customers + k-means k=3 on full-year (same scaler: ARI 0.86 vs today).`
- `Add trajectory features (FHS within-year SD: 17.1 Occasional vs 7.7 Healthy) and GMM soft membership.`
- `Chronological early-warning on next_month_low_health_flag (train Jan–Aug, test Nov), support-only.`

**Speaker note:** The segments survive re-seeding, resampling and removing December, so they are safe to act on. We are explicit that the three full-year groups are zones on a continuum and that the smallest group is defined by how rarely we see them. The December drop hits every segment equally, so year-end reminders go to everyone rather than to one segment.

---

## 4. New charts (`outputs/figures/`, 150 dpi, fixed segment colours; palette validated: CVD ΔE ≥ 9.1, amber < 3:1 contrast is relieved by direct labels)

| File | Use | What it shows |
|---|---|---|
| `v2_t4_k_selection.png` | Slide 16 | Silhouette k = 2..8, k = 4 circled, annotation of what each k separates |
| `v2_t4_sizes.png` | Slide 17 left | Horizontal bars with n and %, 100% coverage in the axis label |
| `v2_t4_profile_heatmap.png` | Slide 17 right | 8 inputs + 6 profile-only rows (months observed, active days, non-POS value, stress month, age, female), z-coloured, raw values |
| `v2_t4_pca.png` | Slide 18 | PCA with named axes, centroid labels, same colours as slide 17 |
| `v2_t4_monthly_fhs.png` | Slide 18 alternative / Task 5 reminders | Monthly FHS by full-year segment with the parallel December drop |

Regenerate: `PYTHONUTF8=1 py draft/review/t4_charts_v2.py` (self-contained; asserts sizes 351/302/258/88).

## Knock-on items outside slides 16–18 (for the deck owner)
- Slide 19, Task 5 row ③: replace "Healthy → Stretched 72% Nov → Dec" with the parallel −13-point December drop. The reminders target becomes the 908 full-year customers, or keep High-Activity + Healthy but cite the drop.
- Slide 19 footnote: "the crossover (43) … inside the Stretched segment" → "39 of the 43 inside Stretched".
- If renamed, update "Digital Power Users" / "Emerging Digital" everywhere (Task 5 table, CLAUDE.md key findings).
