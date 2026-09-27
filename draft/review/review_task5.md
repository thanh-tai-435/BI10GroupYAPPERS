# Review — Task 5 slides (19–21)

Scripts (all run, output captured):
- `draft/review/t5_recompute.py` → `draft/review/t5_recompute_output.txt` (every number below)
- `draft/review/t5_extra.py` (distress-tail profile, spend-weighted discretionary share, scenario slope sensitivity)
- `draft/review/t5_charts_v2.py` → `outputs/figures/v2_t5_priority_score.png`, `outputs/figures/v2_t5_impact_scenario.png` (asserts the ranking order and the 95/80/65/49 path)

Sources: monthly file (10,992 consumer-months, 999 consumers), transactions CSV (1,852,394 rows), `draft/task4_features.csv` (segment labels). The Nov→Dec slip was recomputed independently by assigning each consumer-month to its nearest segment centroid in z-space. At k-means convergence this matches `km.predict`.

---

## 1. Number check

| Slide | Claim on slide | Recomputed | Status |
|---|---|---|---|
| 19 | Stretched & Engaged 302 (30.2%) | 302 (30.2%) | OK |
| 19 | spend_to_income r −0.90 | −0.898 (month level) | OK |
| 19 | segment spend/income 0.835 | 0.835 (Healthy 0.571) | OK |
| 19 | Crossover 43 (4.3%) = 52% of stress months | 43 consumers; 49 of 95 stress months = 51.6%; p75 = 81.40 | OK |
| 19 | 23.5% of spend at 22–23h | stressed 23.5% vs healthy 8.3%; Sun+Mon 41.9% vs 34.0% | OK |
| 19 | Power Users 258 (25.8%) + Healthy 351 (35.1%) | 258 / 351 | OK (but see issue 3) |
| 19 | Healthy → Stretched 72% Nov → Dec | 72.4% (base: 519 Healthy-state November months; yearly mean 23.3%) | OK |
| 19 | volatility r −0.50 | −0.496 (month); **−0.125 at consumer level** | OK (month grain only) |
| 19 | Distress tail 67 (6.7%) | 67 | OK (but see issue 2) |
| 19 | discretionary 72% vs 40% under stress | spend-weighted 71.6% vs 40.5%; row mean 71.2% vs 38.9% | OK |
| 19 | Emerging Digital 88 (8.8%) | 88 | OK |
| 19 | diversity r +0.94 | +0.938 with **engagement**, consumer level (month level +0.590; with FHS −0.069) | OK as stated, but it is an engagement driver, not a health driver |
| 19 | 60.5% of spend via E-com + Mobile | 34.3% + 26.2% = 60.5% (other segments 16.8–17.4%) | OK |
| 19 | lowest utilization 0.148, FHS 70.5 | 0.148 (lowest), 70.49 (highest) | OK |
| 19 | "crossover (43) and distress tail (67) are overlays inside the Stretched segment" | crossover = **39 Stretched + 4 Healthy**; distress tail = **64 Emerging + 3 Stretched** | **MISMATCH** |
| 20 | Ranking "reach × driver strength": Budgeting → Alerts → Reminders → Products → Nudges → Education | reach × \|r\| does not give this order (see issue 4) | **MISMATCH** |
| 20 | Budgeting (302, \|r\| 0.90) | 302, 0.898 | OK |
| 20 | Alerts (43, 52% of stress) | 43, 51.6% | OK |
| 20 | "segments correlate with age/gender" | segment × gender p = 0.001, × age group p < 0.001 (T4); per-target figures in issue 5 | OK |
| 21 | FHS = 84.1 − 25.3 × spend-to-income (r −0.90) | 84.08 − 25.33 × STI, r −0.898 | OK |
| 21 | 5% trim → 95 → 80 (−16%) | 80 (−15.8%) | OK |
| 21 | 10% → 65 (−32%) | 65 (−31.6%) | OK |
| 21 | 15% → 49 | 49 | OK |
| 21 | stat "−32% stress months at a 10% trim" | −32% with the pooled slope; **−28% (68)** with the Stretched-only slope (−22.2) | OK, but the number depends on the slope and should be shown as a range |
| 21 | Budgeting holdout 10%, 3 months | design choice, not data | n/a |

Numbers that are not on the slide but that change the story:
- The Stretched 302 hold **86 of the 95** stress months, so the scenario can never go below 9.
- The 43 crossover consumers hold **67 of the 95** stress months (70.5%) in total. The 49 crossover months are the 51.6% quoted above.
- R² of FHS on spend-to-income + utilization is **0.823**, so FHS is largely a function of those two ratios.
- 78.9% of consumers have a yearly-mean FHS below 70. "FHS < 70" is therefore not a distress threshold.

---

## 2. Critical review (issue → fix)

1. **Wrong overlap statement (slide 19 footer).** The slide says both overlays sit inside Stretched. In fact:
   - Crossover 43 = 39 Stretched + 4 Healthy.
   - Distress tail 67 = 64 Emerging + 3 Stretched.
   - The real double-contact is **Education and Nudges: 64 of the 67 Education targets are also Nudges targets.** Crossover and distress tail never overlap each other (0).
   → Fix: replace the footer with the true overlaps (text below). Sequence Education and Nudges for those 64 so no one gets two campaigns in the same week.
2. **"Distress tail" is a misnomer and the evidence does not fit.** The group is consumer-mean FHS < 70 and engagement < 70. Mean FHS is 62.5 against a base of 66.3, and only **2 of the 95** stress months fall on it. It is really "low-engagement, discretionary-heavy". The "72% vs 40% under stress" evidence describes stressed *months*, not this group.
   → Fix: rename it "Low-health & low-engagement (67)". Use the group's own evidence: **86% discretionary vs 55% base, 66% online**. Keep 72% vs 40% as the population-level rationale only.
3. **Reminders target is inconsistent.**
   - The table says Power 258 + Healthy 351 (= 609).
   - The ranking and chart use 258.
   - Healthy 351 is also the Products target, which is an unstated overlap.
   - The 72.4% evidence is about *Healthy-state months* (519 in November), not the Power segment.
   → Fix: target = Power Users 258 (volatility 1.91, the highest). Use the 72.4% Nov→Dec slip as the **timing** evidence (send in November), not as a second target group. This removes the 351 double count.
4. **The ranking is not reproducible.** The old chart's y-axis mixes different quantities:
   - \|r\| with FHS (0.90, 0.86, 0.50, 0.48)
   - \|r\| with *engagement* (0.94)
   - a utilization *level* (0.15)

   It is then read qualitatively. With score = reach × \|r\|, the stated order does not come out (Alerts would be 5th of 6, Products 1st if its trigger were scored against FHS).
   → Fix: define it explicitly and compute it:
   - **score = reach (consumers in target) × driver strength**
   - **driver strength = \|r\| between the tool's trigger column and the outcome it is meant to move**, month level, n = 10,992
   - outcome = FHS for wellbeing tools and engagement_score for growth tools
   - **Rule: the wellbeing track ranks ahead of the growth track** (it is a wellbeing study).

   Result (asserted in `t5_charts_v2.py`):

   | Rank | Tool | Trigger column | Reach | \|r\| | Score |
   |--:|---|---|--:|--:|--:|
   | 1 | Budgeting | spend_to_income_ratio → FHS | 302 | 0.898 | 271 |
   | 2 | Planning reminders | spending_volatility → FHS | 258 | 0.496 | 128 |
   | 3 | Spend alerts | credit_utilization_ratio → FHS | 43 | 0.862 | 37 |
   | 4 | Financial education | discretionary_spend_ratio → FHS | 67 | 0.481 | 32 |
   | 5 | Product suggestions | credit_utilization_ratio → engagement | 351 | 0.212 | 74 |
   | 6 | Digital nudges | category_diversity → engagement | 88 | 0.590 | 52 |

   **Corrected order: Budgeting → Reminders → Alerts → Education → Products → Nudges.**

   The old narrative "lead with Budgeting + Alerts" survives as a **launch** decision, not a rank. The 43 alert customers carry 67 of 95 stress months (71%) at near-zero cost. Say this openly as the one exception.
5. **Fairness (case §11) is asserted, not quantified.** Triggers are behavioural, but the targets they produce are skewed:

   | Target | Age mean (base 50.1) | Female (base 50.6%) | Minors (of 7) | χ² p age / gender / province |
   |---|--:|--:|--:|---|
   | Budgeting (302) | 50.6 | 43.4% | 0 | 0.018 / 0.004 / 0.057 |
   | Alerts (43) | 47.4 | 44.2% | 0 | 0.73 / 0.49 / 0.067 |
   | Reminders (258) | **43.2** | **60.5%** | **6** | <0.001 / <0.001 / 0.13 |
   | Education (67) | **57.7** | 47.8% | 0 | <0.001 / 0.73 / 0.046 |
   | Nudges (88) | **57.9** | 47.7% | 0 | <0.001 / 0.66 / 0.16 |
   | Products (351) | 52.7 | 50.1% | **1** | <0.001 / 0.90 / 0.13 |

   - **Age:** Education and Nudges have no 25–44-year-olds (age-band ratio 0.0); 18–24 is 3.3×, 55+ is 1.6–1.75×.
   - **Province:** no target over-represents a province. The only p < 0.05 is Education at 0.046, on a sparse 34-province table.
   - **Occupation:** there are 396 occupations for 999 people, so χ² is unreliable. Its low p for Budgeting and Products reflects the occupation–spend-to-income link from Task 2, not targeting.

   Fixes:
   - Keep triggers behaviour-only.
   - Monitor uptake and opt-out by age band, gender and province against the base.
   - Make Education and Nudges content age-neutral (the targets are bimodal: young and 55+).
   - **Exclude under-18s from Product suggestions** (1 minor is in the Healthy 351) and review reminder content for the 6 minors among Power Users.
6. **Punitive / credit risk.** The wording is already good ("never auto-extend credit", "dismissible", rule stated). Two tightenings:
   - Product suggestions are selected on *low credit utilization*. State that they are savings/loyalty only and **never a credit-line increase or new credit offer**. An unrequested limit increase is the flip side of "cut a limit".
   - Alerts must be opt-in and informational ("heads-up"), with no friction on the transaction.
7. **Impact wording (slide 21).** It is honest ("scenario to test, not a forecast"), but it leaves out two facts that matter:
   - FHS is ~82% explained by spend-to-income + utilization, so the −32% partly restates the score formula.
   - The pooled slope (−25.3) is steeper than the slope inside Stretched (−22.2), so a 10% trim gives 65–68 stress months (−28% to −32%), not a single −32%.

   → Fix: show the range, name the mechanical link, and show the 9-month floor (the v2 chart does all three).
8. **Evidence column grain.** Volatility r −0.50 is month level; at consumer level it is −0.125. That is fine for a monthly-triggered reminder, but label it "month level" in the caption.
9. **Out of scope, flagged.** The closing slide and the T4 limitations slide in `build_deck.js` still say "two source years folded onto 2025". CLAUDE.md says this caveat was retired (all timestamps are 2025).

---

## 3. Proposed slides (paste-ready)

### Slide 19 — custom table (layout unchanged)

**Title:** Six non-punitive tools, each tied to a measured data finding

| Tool | Target group (n, % of 999) | Data evidence | Action | KPI |
|---|---|---|---|---|
| ① Budgeting tool | Stretched & Engaged: 302 (30.2%) | spend/income 0.835 vs 0.571 Healthy; r(STI, FHS) −0.90 | Spend-vs-income dashboard + self-set discretionary budget | spend/income; % months FHS < 40 |
| ② Spend alerts | Crossover: 43 (4.3%) — 39 Stretched + 4 Healthy | 49 of 95 stress months (52%); 23.5% of stress spend at 22–23h | Opt-in, dismissible pacing alert Sun–Mon evening, before 22:00 | stress months per consumer |
| ③ Planning reminders | Digital Power Users: 258 (25.8%) | highest volatility 1.91, r −0.50; Healthy→Stretched 72.4% Nov→Dec | Monthly "set aside" prompt; year-end plan sent in November | Nov→Dec slip vs 72.4% baseline |
| ④ Financial education | Low-health & low-engagement: 67 (6.7%) | 86% discretionary vs 55% base; stressed months 72% vs 40% | Needs-vs-wants micro-modules built on their own spend mix | essential share next month |
| ⑤ Digital nudges | Emerging Digital: 88 (8.8%) | 60.5% of spend via E-com + Mobile; diversity–engagement r +0.94 | Onboarding + category-broadening nudges in their app | active days; categories / month |
| ⑥ Product suggestions | Healthy & Engaged: 351 (35.1%), adults only | lowest utilization 0.148, highest FHS 70.5 | Opt-in savings / loyalty; never a credit-line increase | opt-in uptake; FHS stable |

**Source caption:** Source: team k-means (k=4) on 8 z-scaled ratios, 999 consumers; crossover, tail & r: consumer-month file (10,992); timing & channel: transactions file.

**Footer line (replaces the wrong overlay sentence):** Segments ①③⑤⑥ partition all 999. Overlays: Alerts 43 = 39 Stretched + 4 Healthy; Education 67 = 64 Emerging + 3 Stretched, so 64 get ④ and ⑤ in sequence.

**Speaker note:** One tool per required type, each with an exact size, the column it rests on and a KPI. The only double contact is 64 Emerging customers who get education and nudges, staggered.

### Slide 20 — contentOne

**Title:** Prioritization — reach × driver strength, and the credit rule

**Bullets:**
1. Score = reach (consumers) × driver strength (|r| of the tool's trigger column with its outcome, month level). Wellbeing tools (outcome FHS) rank before growth (outcome engagement).
2. Wellbeing: ① Budgeting 271 → ③ Reminders 128 → ② Alerts 37 → ④ Education 32. Growth: ⑥ Products 74 → ⑤ Nudges 52. Alerts still ships first: 43 people hold 71% of stress months.
3. Fairness audit: triggers are behaviour only, but targets skew. Reminders 60.5% female (base 50.6%); Education/Nudges mean age ~58 (base 50). We track uptake by age/gender; minors get no offers.
4. RULE: financial_health_score is never used to deny credit, cut a credit limit, raise a rate or block an account. A low score only triggers help that is offered.

**Chart:** `v2_t5_priority_score.png`
**Stat box:** ["NEVER", "FHS → credit decision"] (keep)
**Source caption:** Source: team analysis, consumer-month file (10,992 months) + task4_features.csv; |r| = Pearson, month level.
**Speaker note:** The axes are the two ranking inputs, so the order is reproducible. Budgeting wins on both. Alerts is small but precise, so it launches in wave 1. The rule is the contract: help offered, never access removed.

### Slide 21 — contentOne

**Title:** Expected impact, measurement and a 90-day roadmap

**Bullets:**
1. What-if: FHS = 84.1 − 25.3 × spend-to-income (r −0.90). If the Stretched 302 cut spend-to-income 10%, stress months fall 95 → 65–68 (−28% to −32%).
2. Directional only: spend-to-income + utilization explain 82% of FHS (R² 0.82), so part of the gain is mechanical; 9 of 95 stress months sit outside the 302.
3. Measurement: each tool has one KPI against a random 10% holdout for 3 months; Reminders are judged on the Nov→Dec slip (baseline 72.4%).
4. Days 0–30: Budgeting + Alerts · 31–60: November Reminders + Digital Nudges · 61–90: Education + opt-in Products. Scale only what beats its holdout.

**Chart:** `v2_t5_impact_scenario.png`
**Stat box:** ["65–68", "stress months (from 95) at a 10% trim"]
**Caveat line:** Illustrative: the slope is built into the FHS formula, so only the holdout test can show real behaviour change.
**Source caption:** Source: team what-if on the consumer-month file (10,992 months); slopes from OLS, all customers vs Stretched only.
**Speaker note:** This is a hypothesis we will measure, not a promise. Even the conservative slope removes about a quarter of stress months, and the holdout tells us which tools earn scale.

---

## 4. New charts

- `outputs/figures/v2_t5_priority_score.png` replaces `t5_priority_ranking.png`.
  - x-axis = reach (consumers), y-axis = |r| of trigger column with outcome (month level).
  - Dashed iso-score curves (reach × |r| = 50/100/200/300).
  - Each point labelled "#rank tool, n × r = score"; colour = track (wellbeing accent, growth primary).
  - The script asserts the order Budgeting → Reminders → Alerts → Education → Products → Nudges.
- `outputs/figures/v2_t5_impact_scenario.png` replaces `t5_impact_scenario.png`.
  - Paired bars: pooled slope (95/80/65/49) vs Stretched-only slope (95/81/68/53).
  - Dotted floor at 9 stress months that sit outside the Stretched segment.
  - Title: "What-if, not a forecast".

To adopt them in `build_deck.js`, swap the two chart file names on slides 20 and 21 and replace the bullets above. No layout change is needed.
