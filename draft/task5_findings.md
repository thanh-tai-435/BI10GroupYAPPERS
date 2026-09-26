# Task 5 — Business Recommendations: A Non-Punitive Wellbeing Action Plan

*Group YAPPERS · BI10 Round 01 · 999 consumers, 10,992 consumer-months, 1,852,394 transactions, 2025, VND. Every size and % below is recomputed and asserted in `draft/task5.py`; captured output in `draft/task5_output.txt`.*

**This is a wellbeing programme, not a credit programme.** Every recommendation is grounded in a real ratio from the data (Tasks 1–4), targets an exactly-sized group, and is delivered as *supportive tooling the customer can accept or ignore* — never a restriction imposed on them. The single ethical constraint (stated in full in §4) is that `financial_health_score` never touches a credit decision.

---

## 0 · The one-page story (reconciled across Tasks 1–4)

Four verified facts drive the whole plan, and they agree:

1. **Low health = overspend, not low income.** `spend_to_income_ratio` (corr **−0.90** with FHS) and `credit_utilization_ratio` (**−0.86**) explain almost all of financial health (T2). Stressed months spend ~72% on discretionary vs ~40% for healthy — the budget mix *inverts* with stress (T1 Q2).
2. **Stress is episodic, not chronic.** 0 / 999 consumers are chronically stressed; only 0.9% of months score FHS < 40 (T2 Q1). So the sharpest interventions must be **event-triggered on the current month**, not a static risk list.
3. **The people sliding into stress are the most engaged ones.** 52% of *all* stress episodes happen to highly-engaged customers (T2 Q4). The channel to reach them is already open and free.
4. **Segment on behaviour, not demographics.** Geography and age are flat on health (T1 Q3/Q5, T2 Q3); the four k-means segments (T4) and the two rule-based tails (T2/T3) are the real, actionable groups.

The plan therefore has two tracks: a **wellbeing track** (help the stretched/stressed pace their spend) and a **growth track** (activate the dormant and monetise the healthy) — with wellbeing prioritised because its drivers are the strongest signals in the data.

**Groups used (all recomputed, internally consistent — see `task5_output.txt`):**

| Group | Size | % of 999 | Source rule |
|---|--:|--:|---|
| Financially Healthy & Highly Engaged | 351 | 35.1% | T4 segment 1 |
| Financially Stretched but Highly Engaged | 302 | 30.2% | T4 segment 2 |
| High-Activity Digital Power Users | 258 | 25.8% | T4 segment 3 |
| Low Engagement & Emerging Digital | 88 | 8.8% | T4 segment 4 |
| Distress tail (FHS<70 **AND** eng<70) | 67 | 6.7% | T3 rule (consumer level) |
| Stressed **AND** Engaged crossover | 43 | 4.3% | T2 rule (49 stress-months = 52% of all stress; month grain) |
| Dormant good (FHS≥70 **AND** eng<70) | 25 | 2.5% | T3 rule (consumer level) — reactivation sub-target |

---

## 1 · Six proposals — one per tool type

### ① Budgeting tools → *Financially Stretched but Highly Engaged*
- **Target: 302 consumers (30.2%).**
- **Data hook:** this segment carries the **highest spend-to-income (0.835)** and **highest credit-utilization (0.248)** in the base (T4), and `spend_to_income_ratio` is the **strongest driver of low health (−0.90)** (T2). They are still fully engaged (76.5, 119 txns/mo), so they will open an in-app tool.
- **The tool:** a "**spend vs income this month**" dashboard + discretionary-category breakdown, with a self-set monthly discretionary budget. Reads directly off `spend_to_income_ratio` and `discretionary_spend_ratio`.
- **Expected effect:** visibility on the exact ratio that predicts stress; nudges the 0.835 ratio down before a month tips into FHS<40. Non-punitive — it shows, it does not block.

### ② Spend alerts → *Stressed AND Engaged crossover*
- **Target: 43 consumers (4.3%) — but 49 consumer-months = 52% of ALL stress episodes** in the entire dataset.
- **Data hook:** in their stress months these customers spend **1.89× income**, burn **55% of their credit line**, and skew 71% discretionary / 49% online (T2 Q4) — over 2× the national online share, so an **in-app push reaches them instantly and free**. Stress is episodic (T2 Q1), so the alert must fire on the *current* month.
- **The tool:** an **event-triggered, in-app spend-pacing / utilization alert** — "your spend is outpacing your income this month" and "you're at 55% of your limit" — fired when current-month `spend_to_income_ratio` or `credit_utilization_ratio` crosses a threshold. Framed as a heads-up, dismissible.
- **Expected effect:** highest *leverage per customer* in the plan — catching half of all stress episodes at the moment they happen, on a channel already open, at near-zero cost.

### ③ Financial-planning reminders → *High-Activity Digital Power Users*
- **Target: 258 consumers (25.8%).**
- **Data hook:** they are the **most volatile spenders (spending_volatility 1.91, ~1.3× base)** and most active (251 txns/mo) (T4). Volatility correlates **−0.50** with FHS (T2) — they are not stressed yet, but volatility is the watch-signal for drift into segment ②. December amplifies this system-wide (mean FHS falls 73.6→54.2, T1 Q1).
- **The tool:** scheduled **planning reminders** — a pre-December "pace your year-end spend" reminder and a "set aside for next month" prompt after a high-volatility month. Also the vehicle to re-touch the **25 dormant good customers (2.5%)** with a gentle "haven't seen you — here's your snapshot" reactivation.
- **Expected effect:** smooths the spikes that precede stress; pre-empts the December health dip before it becomes an alert.

### ④ Financial-education content → *Distress tail (low-health AND low-engagement)*
- **Target: 67 consumers (6.7%).**
- **Data hook:** the **essential-spend inversion** — stressed customers spend ~72% discretionary vs ~40% for healthy (T1 Q2), and `essential_spend_ratio` correlates **+0.48** with health (T2). This tail is *both* low-health and low-engagement (T3 Q5), so a passive dashboard won't reach them — they need pushed, plain-language content.
- **The tool:** short **financial-education modules** on needs-vs-wants budgeting and credit-utilization basics, pushed (email + in-app), tied to their own discretionary/essential mix so it's concrete, not generic.
- **Expected effect:** rebuilds the essential-first habit that separates healthy from stressed customers; addresses the group that alerts alone can't reach because engagement is low.

### ⑤ Digital-channel nudges → *Low Engagement & Emerging Digital*
- **Target: 88 consumers (8.8%)** (+ the 25 dormant good as a reactivation overlap).
- **Data hook:** near-dormant (9.7 txns/mo, engagement 49.6) but what they *do* spend is **67.1% online** vs ~20% base and **86.6% discretionary** (T4). Category diversity is the master engagement signal (r **+0.94**, T3 Q3) and these customers are narrow. **Highest growth headroom** of any segment.
- **The tool:** **digital-channel onboarding + habit-forming nudges** — QR/app setup, a first-recurring-payment prompt (fuel/transport is the top-frequency touchpoint, T1 Q4), and category-broadening offers to lift diversity off its floor.
- **Expected effect:** converts sporadic online use into regular engagement — pure growth, no wellbeing risk (their health is average).

### ⑥ Suitable product suggestions → *Financially Healthy & Highly Engaged*
- **Target: 351 consumers (35.1%) — the largest reach.**
- **Data hook:** lowest spend-to-income (0.571), **lowest credit-utilization (0.148)** and highest FHS (70.5) in the base (T4). Low utilization = genuine capacity headroom, and this is the one group where a product suggestion is *appropriate and beneficial* rather than a stress risk.
- **The tool:** **suitable-product suggestions** — savings/investment nudges, loyalty/premium tier, cross-sell. Suggestions the customer opts into; the low utilization is used to *offer*, never to auto-extend.
- **Expected effect:** grows relationship value with the segment that can absorb it, funding the wellbeing track for the rest of the base.

---

## 2 · Prioritization — reach × driver strength

**Reach** = # customers a tool touches. **Driver strength** = how strong the underlying data signal is (correlation with FHS, or the share-of-stress leverage). We rank wellbeing-weighted, because the case is a wellbeing study and the strongest signals in the data are wellbeing signals.

| Rank | Tool → Target | Reach | Driver strength (the number) | Why this rank |
|--:|---|--:|---|---|
| **1** | ① Budgeting → Stretched-Engaged | **302 (30.2%)** | **−0.90** (spend/income) — strongest driver in the data | Big reach × strongest driver. The anchor intervention. |
| **2** | ② Spend alerts → Stressed-Engaged crossover | 43 (4.3%) | **−0.86** (credit-util) + **52% of ALL stress episodes** | Small reach but unmatched *leverage per customer*; free channel, event-triggered. |
| **3** | ③ Planning reminders → Digital Power Users | 258 (25.8%) | **−0.50** (volatility) | Large reach, moderate driver; pre-empts drift + December dip. |
| **4** | ⑥ Product suggestions → Healthy-Engaged | **351 (35.1%)** | Weak wellbeing driver (util 0.148 = headroom, growth not health) | Largest reach but growth play, not wellbeing; funds the rest. |
| **5** | ⑤ Digital nudges → Emerging Digital | 88 (8.8%) | +0.94 category-diversity signal; growth headroom | Moderate driver, smaller reach; highest growth upside. |
| **6** | ④ Education → Distress tail | 67 (6.7%) | ±0.48 (essential/discretionary) | Smallest reach × moderate driver, but reaches the group nothing else can. |

- **By pure reach:** ⑥ 351 > ① 302 > ③ 258 > ⑤ 88 > ④ 67 > ② 43.
- **By pure driver strength:** ① −0.90 > ② −0.86 > ③ −0.50 > ④ 0.48 > ⑤ (engagement signal) > ⑥ (growth, no wellbeing driver).
- **Combined verdict:** start with **① Budgeting** (best on both axes) and **② Alerts** (highest precision). These two cover the wellbeing mission; ③–⑥ layer growth and breadth on top.

---

## 3 · No double-counting — how the groups reconcile

The four T4 segments (351 + 302 + 258 + 88 = 999) are a **partition** — every consumer is in exactly one, so proposals ①③⑤⑥ target disjoint segments. The two rule-based groups are **overlays** used only where episodic precision matters:
- **② crossover (43)** and **④ distress tail (67)** are month-grain / cross-cutting rules that mostly fall *inside* segment ② (Stretched-Engaged); they are the sharp sub-targets, not new populations — so ② and ④ are subsets, not additions.
- **25 dormant good** overlaps the low-engagement customers and is a reactivation sub-target (via tool ③), not a fifth segment.

All sizes match T2 (43 / 49 / 52%), T3 (25, 67), and T4 (351/302/258/88) exactly — verified by assertion in `task5.py`.

---

## 4 · The credit-decision rule (absolute, non-negotiable)

> **`financial_health_score` and every segment/flag derived from it MUST NEVER be used to deny credit, reduce a credit limit, raise a rate, close or freeze an account, or otherwise disadvantage a customer.** FHS is a *wellbeing* measure of spending health, not a measure of creditworthiness. All six tools above are **supportive and opt-in**: they show information, send a dismissible nudge, or offer a product the customer can decline. A low health score triggers *help offered*, never *access removed*. Credit decisions must continue to run on the bank's existing, separately-governed credit-risk models — which this programme does not feed.

This is why every tool is phrased as "show / remind / suggest / alert," never "restrict / cut / block."

---

## 5 · Fairness note

Because the plan targets **behavioural ratios, not demographics**, it is structurally fair by construction — and T1/T2 confirmed age, province and occupation carry almost no health signal. Verified on the wellbeing-priority segment (Stretched-Engaged, n=302) in `task5.py`:

- **Age: neutral.** Mean age 50.6 vs 50.1 base — no age band is singled out. (Note: the 7 minors aged 15–17 are retained in the data; any pushed content to under-18s should be reviewed separately.)
- **Geography: noise only.** Province over/under-representation ranges 0.44×–2.02×, but every deviation sits on a **thin cell** (the 2.02× outlier, Thái Nguyên, is ~9 people on a base of 18). No province is systematically over- or under-served — consistent with T1's "no regional divide" finding. Interventions are delivered per-customer on ratios, so no region is advantaged or disadvantaged.
- **Gender: monitor.** The stretched segment skews mildly male (56.6% vs 49.4% base). This is a data observation, not a targeting criterion — the tools key on spend/income, not gender — but the split should be **monitored** so the wellbeing programme doesn't inadvertently under-serve women who become stretched. Do not add gender as a targeting field.

**Bottom line:** targeting on `spend_to_income_ratio` / `credit_utilization_ratio` / engagement behaviour means no protected demographic is used as a lever, and the ethical credit rule (§4) guarantees the downside is always "help offered," never "access denied."
