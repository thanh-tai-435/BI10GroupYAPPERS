// BI10 R01 — Group YAPPERS deck. Charts come from notebooks/full_pipeline.ipynb (outputs/figures/deck_*.png).
// Run: node draft/build_deck.js
const pptxgen = require("pptxgenjs");
const path = require("path");

const FIG = path.resolve(__dirname, "..", "outputs", "figures");
const OUT = process.env.OUT || path.resolve(__dirname, "YAPPERS_BI10_R01.pptx");

// ---- blue & white theme ----
const NAVY = "0B2545", BLUE = "1F5FA8", MID = "4A90D9", LIGHT = "A9C6EA", PALE = "EEF4FB";
const INK = "1A2433", MUTE = "5B6B7B", WHITE = "FFFFFF", ICE = "CFE0F5";
const FONT = "Arial";

const p = new pptxgen();
p.layout = "LAYOUT_WIDE";          // 13.33 x 7.5 in (16:9)
p.title = "ITB Consumer Wellbeing & Segmentation — Group YAPPERS";

const SRC_M = "consumer_financial_health_engagement_2025 (10,992 consumer-months, 999 customers)";
const SRC_T = "consumer_transactions_2025 (1,852,394 transactions)";
const SRC_J = "transactions joined to consumer-months";
const SRC_K = "team k-means (k = 4) on 8 z-scaled behavioural features, 999 customers";

// ---------- helpers ----------
const T = (s, text, o) => s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: FONT, color: INK }, o));
function header(s, section, title) {
  T(s, section.toUpperCase(), { x: 0.6, y: 0.35, w: 10, h: 0.3, fontSize: 11, bold: true, color: BLUE, charSpacing: 2 });
  T(s, title, { x: 0.6, y: 0.66, w: 12.1, h: 0.95, fontSize: 24, bold: true, color: NAVY, valign: "top" });
}
function footer(s, n, src) {
  if (src) T(s, "Source: " + src + ". Charts: notebooks/full_pipeline.ipynb.", { x: 0.6, y: 6.98, w: 10.6, h: 0.3, fontSize: 8.5, color: MUTE, italic: true });
  T(s, String(n), { x: 12.23, y: 6.98, w: 0.5, h: 0.3, fontSize: 9, color: MUTE, align: "right" });
}
function img(s, name, x, y, w, h) {
  s.addImage({ path: path.join(FIG, name + ".png"), x, y, w, h, sizing: { type: "contain", w, h } });
}
// right-hand insight panel: big number + takeaways
function panel(s, big, label, points, o = {}) {
  const x = 9.05, y = 1.75, w = 3.68, h = o.h || 4.95;
  s.addShape(p.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.1, fill: { color: PALE }, line: { color: PALE } });
  T(s, big, { x: x + 0.25, y: y + 0.2, w: w - 0.5, h: 0.85, fontSize: o.bigSize || 40, bold: true, color: BLUE });
  T(s, label, { x: x + 0.25, y: y + 1.05, w: w - 0.5, h: 0.6, fontSize: 11, color: MUTE, valign: "top" });
  T(s, points.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < points.length - 1, paraSpaceAfter: 8 } })),
    { x: x + 0.25, y: y + 1.75, w: w - 0.45, h: h - 1.9, fontSize: o.fs || 12, color: INK, valign: "top" });
}
// three insight cards along the bottom
function cards(s, items, y = 5.72) {
  const w = 3.9, gap = 0.2;
  items.forEach((it, i) => {
    const x = 0.6 + i * (w + gap);
    s.addShape(p.ShapeType.roundRect, { x, y, w, h: 1.1, rectRadius: 0.08, fill: { color: PALE }, line: { color: PALE } });
    T(s, it[0], { x: x + 0.2, y: y + 0.12, w: 1.55, h: 0.85, fontSize: 20, bold: true, color: BLUE, valign: "middle", fit: "shrink" });
    T(s, it[1], { x: x + 1.8, y: y + 0.1, w: w - 1.95, h: 0.9, fontSize: 10.5, color: INK, valign: "middle" });
  });
}
function slideOne(n, section, title, chartName, big, label, points, src, notes, o = {}) {
  const s = p.addSlide(); s.background = { color: WHITE };
  header(s, section, title);
  img(s, chartName, 0.6, 1.75, 8.2, 4.95);
  panel(s, big, label, points, o);
  footer(s, n, src); s.addNotes(notes);
  return s;
}
function slideTwo(n, section, title, c1, c2, items, src, notes) {
  const s = p.addSlide(); s.background = { color: WHITE };
  header(s, section, title);
  img(s, c1, 0.6, 1.7, 5.95, 3.85);
  img(s, c2, 6.78, 1.7, 5.95, 3.85);
  cards(s, items);
  footer(s, n, src); s.addNotes(notes);
}
function slideWide(n, section, title, chartName, items, src, notes) {
  const s = p.addSlide(); s.background = { color: WHITE };
  header(s, section, title);
  img(s, chartName, 0.6, 1.7, 12.13, 3.85);
  cards(s, items);
  footer(s, n, src); s.addNotes(notes);
}

// ============ 1 · TITLE ============
(() => {
  const s = p.addSlide(); s.background = { color: NAVY };
  T(s, "BI10 ROUND 01  ·  GROUP YAPPERS", { x: 0.8, y: 1.2, w: 11, h: 0.4, fontSize: 13, bold: true, color: LIGHT, charSpacing: 3 });
  T(s, "ITB Consumer Wellbeing\n& Segmentation", { x: 0.8, y: 1.8, w: 11.5, h: 1.9, fontSize: 44, bold: true, color: WHITE });
  T(s, "Overspending, not low income, drives financial stress — and help can be timed to reach it", { x: 0.8, y: 3.8, w: 11.5, h: 0.6, fontSize: 18, color: ICE });
  [["999", "customers"], ["10,992", "customer-months"], ["1.85M", "transactions"], ["2025", "full year"]].forEach((k, i) => {
    const x = 0.8 + i * 2.55;
    s.addShape(p.ShapeType.roundRect, { x, y: 5.0, w: 2.35, h: 1.2, rectRadius: 0.08, fill: { color: "13345E" }, line: { color: "13345E" } });
    T(s, k[0], { x, y: 5.08, w: 2.35, h: 0.65, fontSize: 26, bold: true, color: WHITE, align: "center" });
    T(s, k[1], { x, y: 5.72, w: 2.35, h: 0.35, fontSize: 11, color: LIGHT, align: "center" });
  });
  T(s, "September 2026", { x: 0.8, y: 6.6, w: 5, h: 0.35, fontSize: 11, color: LIGHT });
  s.addNotes("A wellbeing study, not credit scoring. In one line: people slide into stress because they overspend on wants, usually in specific months, so ITB can offer help at the right time and never touch anyone's credit.");
})();

// ============ 2 · EXECUTIVE SUMMARY ============
(() => {
  const s = p.addSlide(); s.background = { color: WHITE };
  header(s, "Executive summary", "Overspending drives stress — and it is timed, reachable and fixable");
  const rows = [
    ["T1", "71.6% vs 40.5%", "Stress flips the budget to wants", "Discretionary share in stressed vs healthy months; purchases ≥ 10M VND are 4% of stressed transactions but 54% of the value."],
    ["T2", "52%", "Stress is episodic and concentrated", "Spend-to-income (r −0.90) drives health. Nobody is stressed all year, yet 87% dip below 60; 43 active customers hold 52% of stress months."],
    ["T3", "91", "Engagement is saturated", "91% of customers are High / Very high; the entire low tail is 91 customers seen on only 1–2 days. Breadth and regular use drive engagement."],
    ["T4", "4", "Four stable segments, 100% covered", "Healthy 351 · Stretched 302 · High-Activity 258 · Occasional 88; stable across seeds (ARI 0.99). December cuts health ~13 pts in every segment."],
    ["T5", "−28–32%", "Six opt-in tools, one rule", "Budgeting → November reminders → evening alerts lead. In a what-if, a 10% spend trim cuts stress months 28–32% (to be tested). FHS never touches credit."],
  ];
  rows.forEach((r, i) => {
    const y = 1.75 + i * 1.02;
    s.addShape(p.ShapeType.ellipse, { x: 0.6, y: y + 0.1, w: 0.62, h: 0.62, fill: { color: NAVY }, line: { color: NAVY } });
    T(s, r[0], { x: 0.6, y: y + 0.1, w: 0.62, h: 0.62, fontSize: 13, bold: true, color: WHITE, align: "center", valign: "middle" });
    T(s, r[1], { x: 1.45, y, w: 2.9, h: 0.82, fontSize: 26, bold: true, color: BLUE, valign: "middle", fit: "shrink" });
    T(s, r[2], { x: 4.45, y: y + 0.02, w: 8.3, h: 0.35, fontSize: 14, bold: true, color: NAVY });
    T(s, r[3], { x: 4.45, y: y + 0.38, w: 8.3, h: 0.5, fontSize: 11.5, color: INK, valign: "top" });
  });
  footer(s, 2);
  s.addNotes("One row per task: signal, driver, engagement, segments, plan. The 52% (T2) is the share of the 95 stress months held by the 43 crossover customers; spend-to-income and utilization explain 82% of FHS; the 28–32% is a simulated what-if, to be tested against holdouts (slide 21).");
})();

// ============ 3 · AGENDA ============
(() => {
  const s = p.addSlide(); s.background = { color: WHITE };
  header(s, "Contents", "What this deck covers");
  const items = [["01", "Introduction & data quality", "slide 4"], ["02", "Task 1 — Exploratory data analysis", "slides 5–8"],
    ["03", "Task 2 — Financial health", "slides 9–12"], ["04", "Task 3 — Customer engagement", "slides 13–15"],
    ["05", "Task 4 — Customer segmentation", "slides 16–18"], ["06", "Task 5 — Recommendations & impact", "slides 19–21 · closing 22"]];
  items.forEach((it, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.6 + col * 6.15, y = 1.9 + row * 1.55;
    s.addShape(p.ShapeType.roundRect, { x, y, w: 5.95, h: 1.3, rectRadius: 0.08, fill: { color: PALE }, line: { color: PALE } });
    T(s, it[0], { x: x + 0.3, y, w: 1.1, h: 1.3, fontSize: 30, bold: true, color: BLUE, valign: "middle" });
    T(s, it[1], { x: x + 1.45, y: y + 0.28, w: 4.3, h: 0.45, fontSize: 16, bold: true, color: NAVY });
    T(s, it[2], { x: x + 1.45, y: y + 0.72, w: 4.3, h: 0.35, fontSize: 12, color: MUTE });
  });
  footer(s, 3);
  s.addNotes("Four required sections: Executive Summary (2), Contents (3), Introduction (4), Task results (5–21). Each task follows the brief's question order.");
})();

// ============ 4 · INTRODUCTION + DATA QUALITY ============
(() => {
  const s = p.addSlide(); s.background = { color: WHITE };
  header(s, "Introduction", "A wellbeing lens on 999 customers — built on clean, reconciled data");
  T(s, [
    { text: "ITB wants to understand customers' financial wellbeing, spending and channel engagement — not to score credit risk.", options: { bullet: true, breakLine: true, paraSpaceAfter: 10 } },
    { text: "We compare ratios and shares, never absolute VND: synthetic income, credit and balances are inflated.", options: { bullet: true, breakLine: true, paraSpaceAfter: 10 } },
    { text: "Stress is measured per customer-month (it comes and goes); segments per customer (yearly profile).", options: { bullet: true, breakLine: true, paraSpaceAfter: 10 } },
    { text: "Process: data checks → EDA → health → engagement → segmentation → recommendations.", options: { bullet: true } },
  ], { x: 0.6, y: 1.85, w: 5.9, h: 3.2, fontSize: 13.5, valign: "top" });
  s.addShape(p.ShapeType.roundRect, { x: 0.6, y: 5.25, w: 5.9, h: 1.45, rectRadius: 0.08, fill: { color: NAVY }, line: { color: NAVY } });
  T(s, [{ text: "Ethical rule   ", options: { bold: true, color: LIGHT } },
        { text: "financial_health_score is a wellbeing indicator — never used to approve or deny credit, cut a limit, raise a rate or block an account.", options: { color: WHITE } }],
    { x: 0.85, y: 5.35, w: 5.4, h: 1.25, fontSize: 12.5, valign: "middle" });
  s.addShape(p.ShapeType.roundRect, { x: 6.85, y: 1.85, w: 5.88, h: 4.85, rectRadius: 0.08, fill: { color: PALE }, line: { color: PALE } });
  T(s, "Data-quality checks (both files)", { x: 7.1, y: 2.0, w: 5.4, h: 0.4, fontSize: 14, bold: true, color: NAVY });
  const dq = [["✓", "0 missing cells, 0 duplicate IDs, 0 negative amounts"], ["✓", "All timestamps in 2025; 1 name per customer and merchant"],
    ["✓", "Transactions reconcile 100% to monthly spend (10,992 months)"], ["✓", "7 minors kept; 5 over-limit months kept as real behaviour"],
    ["!", "908 customers have 12 months; 91 appear on only 1–2 days"], ["!", "Two source years folded onto 2025 (case study §12) → ratios are the signal"]];
  dq.forEach((d, i) => {
    const y = 2.55 + i * 0.66;
    s.addShape(p.ShapeType.ellipse, { x: 7.1, y: y + 0.05, w: 0.36, h: 0.36, fill: { color: d[0] === "✓" ? BLUE : WHITE }, line: { color: BLUE, width: 1.2 } });
    T(s, d[0], { x: 7.1, y: y + 0.05, w: 0.36, h: 0.36, fontSize: 11, bold: true, color: d[0] === "✓" ? WHITE : BLUE, align: "center", valign: "middle" });
    T(s, d[1], { x: 7.6, y, w: 4.95, h: 0.5, fontSize: 12, valign: "middle" });
  });
  footer(s, 4, SRC_M + "; " + SRC_T);
  s.addNotes("Two rules govern the deck: ratios over magnitudes, wellbeing over credit. The data is clean; the caveats are the synthetic ones the case documents, plus 91 customers seen only once, which we flag wherever they touch a number. 693 merchants, 34 provinces.");
})();

// ============ TASK 1 ============
slideOne(5, "Task 1 · EDA · Q1", "December is 15% of annual spend — driven by more trips, not bigger baskets",
  "deck_q1_index", "2.9×", "transactions per customer, December vs February",
  ["Dec 488B VND = 15.04% of the year vs Feb 174B = 5.37% (2.8×)",
   "Transactions +187%, average ticket −2.6%; active customers flat (919 → 918)",
   "December is also the weakest-health month (FHS 54.2) → plan support before it"],
  SRC_T, "Peak = December 488.0B VND (15.04% of 3.24T), trough = February 174.4B (5.37%); gap +313.7B (+9.7pp). All 14 categories grow +181% to +193% in transactions. Case §12: two source years folded onto 2025 inflate absolute VND, so the share and the 2.8× ratio are the reliable signal.");

slideTwo(6, "Task 1 · EDA · Q2", "Under stress the budget flips: 71.6% discretionary vs 40.5% when healthy",
  "deck_q2_gradient", "deck_q2_shift",
  [["71.6%", "discretionary share in stressed months (FHS < 40) vs 40.5% in healthy months (FHS ≥ 80)"],
   ["54%", "of stressed-month value comes from purchases ≥ 10M VND — only 4.3% of transactions"],
   ["+22pp", "travel's share gain; the mix stays inverted even without travel (37% vs 60% essential)"]],
  SRC_M + "; category shift: " + SRC_J,
  "95 stressed months (70 customers): 28.4% essential / 71.6% discretionary; 475 healthy months (303 customers): 59.5% / 40.5%. The share falls steadily across every band, so it is not a cutoff artefact (FHS<35 vs ≥85: 73.5% vs 30.2%). Essentials are ~47% of transactions in both groups: the flip is in value (discretionary ticket 3.9M vs 1.1M VND). Implication: pre-purchase visibility, never credit restriction.");

slideOne(7, "Task 1 · EDA · Q3", "High-spend provinces trail the national digital share by at most 0.46pp",
  "deck_q3_gap", "≤ 0.46pp", "largest digital gap among high-spend provinces",
  ["6 qualify (spend > median, digital < 41.2%): Dong Nai 40.7%, Hung Yen 40.8%, Hai Phong 40.8%, Ha Noi 40.9%, Lam Dong 41.1%, Nghe An 41.2%",
   "Channel mix: POS 58.9–59.3% vs 58.8% nationally; QR at par; the gap sits in e-commerce and app",
   "Customers differ 8.6pp within provinces vs 3.9pp across all 34 → target the customer, not the region",
   "Top market HCMC: 13.6% of spend at 41.3% digital; lagging: Quang Ngai 39.2% digital"],
  SRC_T, "Qualifying = spend above the provincial median (> 82.7B VND) and digital (non-POS) share below the national 41.2%. Only 3 of 6 gaps are significant (p < 0.05). HCMC leads spend (13.6%) at 41.3% digital; range Cao Bang 43.1% to Quang Ngai 39.2%.");

slideTwo(8, "Task 1 · EDA · Q4 & Q5", "Fuel is the everyday habit, groceries the biggest basket; age barely moves health",
  "deck_q4_categories", "deck_q5_cohorts",
  [["188,029", "Fuel & transport transactions — top by count, 1.59M VND ticket, 17 buys per buyer-month"],
   ["2.92M", "VND grocery ticket — top by spend (513.8B), 1.8× fuel. Lagging: travel (57,956 txns), online groceries (87.1B)"],
   ["65.8", "lowest FHS: 25–34, active (178.7 txns/mo); spend/income 0.716 vs 0.700, essential 0.468 vs 0.481"]],
  SRC_T + "; cohorts: " + SRC_M,
  "Q4: fuel is a frequent top-up (96.8% of customers buy it), groceries a stock-up basket (99.3%). Q5: 25–34 is the only cohort above national spend-to-income (0.716 vs 0.700) and below the national essential ratio (0.468 vs 0.481) — overspending on wants. But the spread is 1.2 points, 95% CIs overlap and ANOVA p = 0.13: age is a weak lever.");

// ============ TASK 2 ============
slideOne(9, "Task 2 · Financial health · D1", "No one is stressed on average, yet 87% of customers dip below 60 at least once",
  "deck_d1_distribution", "87%", "of customers fall below 60 in at least one month",
  ["Customer averages: mean 66.3, IQR 63.4–69.3 — a tight band",
   "Months are 2× more spread: 95 stressed months (0.9%) across 70 customers",
   "January + December hold 46 of 95 stressed months → trigger help on the month"],
  SRC_M, "Consumer level: mean 66.3, median 66.2, std 4.7, range 42.3–80.8, skew −0.32. Month level: std 9.5; Stable 72.5% · Watch 22.4% · Healthy 4.3% · Stressed 0.9%. Who the customer is explains only 22% of monthly variance, the calendar month 25%.");

slideTwo(10, "Task 2 · Financial health · D2", "Low health is an overspending story: it breaks once spend passes income",
  "deck_d2_threshold", "deck_d2_drivers",
  [["r −0.90", "spend-to-income; with utilization (−0.86) it explains 82% of the health score"],
   ["98%", "of stressed months spend more than income"],
   ["93%", "of top-quintile months fall below 60 — none in the bottom two quintiles"]],
  SRC_M + "; category mix: " + SRC_J,
  "Spend-to-income and utilization move together (r 0.90): one overspending factor, which also holds within each customer (r −0.90). Stressed months are 71.6% discretionary by value and have 2× the e-commerce + app share (23% vs 12%). They are also more engaged (81.1 vs 72.7). FHS and the ratios share spend fields — directional, not causal.");

slideWide(11, "Task 2 · Financial health · D3", "Occupation and province gaps are really spending gaps; age is flat",
  "deck_d3_spread",
  [["6.2 → 1.3", "points: occupation gap once spend-to-income is held constant"],
   ["4.8 → 1.6", "points: province gap (Ha Noi 67.8 top, Thai Nguyen 63.0 bottom)"],
   ["1.2", "points across six age cohorts — not significant (p = 0.13)"]],
  SRC_M + " (customer level)",
  "Occupation: 396 titles grouped into 8 keyword groups; Eng/science/IT 69.1 and Business/finance 68.7 vs Office/public 64.5 and Manual 62.9, mirroring spend-to-income 0.61 vs 0.76–0.79. Province ANOVA p = 0.009 but only 5% of variance. Target the ratio, never the group — fairer and more effective.");

slideOne(12, "Task 2 · Financial health · D4", "43 active customers carry 52% of stress months — with big late-night purchases",
  "deck_d4_latenight", "52%", "of all stress months belong to 43 highly engaged customers",
  ["Rule: FHS < 40 AND engagement ≥ 81.4 (top 25% of months); stable at top 30% / 20%",
   "Profile: spend 1.89× income, utilization 0.55, online share 2.3× average",
   "23.5% of stressed spend value lands at 22–23h (vs 8.3%) → opt-in alert before 22:00"],
  SRC_M + "; timing: " + SRC_J,
  "Rule applied per customer-month; a customer belongs if any month qualifies. 49 months / 43 customers = 51.6% of stressed months vs 25% by chance (p < 0.001); top 30% / 20% give 44 / 41 customers. All 43 are full-year customers averaging FHS 62 in other months; 39 sit in the Stretched segment. Late-night count differs little (11.6% vs 9.7%): bigger tickets, led by online shopping (39%) and travel (14%). Wellbeing use only.");

// ============ TASK 3 ============
slideTwo(13, "Task 3 · Engagement · D1–D2", "Engagement is saturated; the whole low tail is 91 one-off customers",
  "deck_t3_engagement", "deck_t3_channels",
  [["91%", "of customers are High or Very high (1.0 / 8.0 / 66.9 / 24.1% by band)"],
   ["91", "customers seen on only 1–2 days are the entire below-High tail"],
   ["21.0%", "average online spend share; 925 of 999 customers use all five channels"]],
  SRC_M + "; channels: " + SRC_T,
  "Engagement score mean 77.8, median 78.1, IQR 74.8–81.4. Every full-year customer averages ≥ 69.8, so the score separates one-off users from the base, not good customers from great ones. Channels: POS 58.8% · QR 19.8% · E-commerce 8.7% · Mobile 7.7% · Recurring 4.9%; non-POS = 41% of trips and 41.5% of value. Chart choice: histogram for a continuous score (bands shaded so the 1% tail stays visible), sorted bars for nominal channels.");

slideTwo(14, "Task 3 · Engagement · D3–D4", "Breadth and regular activity — not recency — separate engaged customers",
  "deck_t3_diversity", "deck_t3_heatmap",
  [["2–14", "categories per month; r +0.81 with engagement even within full-year customers"],
   ["r +0.80", "active days (range 1–31, median 30) — ahead of count (+0.76) and recency (−0.58; range 0 to 30 days)"],
   ["≤ 55", "engagement whenever a customer is active on only 1–5 days, whatever the recency"]],
  SRC_M,
  "Ranges: recency 0–30 days (median 0), active days 1–31 (median 30), 2–713 transactions a month (median 150). r = +0.94 across all customers is partly two clusters; +0.81 within the 908 full-year base shows the link holds. Scatter for two continuous variables; heatmap for the recency × frequency interaction.");

slideOne(15, "Task 3 · Engagement · D5", "25 healthy customers used their card on only 1–2 days all year",
  "deck_t3_cutoff", "25", "customers (2.5%): FHS ≥ 70 and engagement < 70",
  ["Cutoff 70 sits in an empty gap: 25 at any cutoff 60–70; looser (72.5 / 75) pulls in active users (39 / 63); stricter FHS ≥ 75 leaves 9",
   "Profile: 2 vs 27 active days, 10 vs 159 transactions a month, 61% vs 24% online",
   "19 silent since Jan–Jul → win back everyday use, not budgeting"],
  SRC_M, "FHS ≥ 70 = top 21% (p79); engagement < 70 is below the customer p10 (71.1). Looser cutoffs pull in active users (39 at 72.5, 63 at 75); FHS ≥ 65 gives 48, ≥ 75 gives 9. Also: age 61 vs 50, diversity 4.7 vs 13.1, spend/income 0.46 vs 0.70; 24 of 25 are Occasional Online-First. One month of data each: a watch-list, never used to limit credit.");

// ============ TASK 4 ============
slideOne(16, "Task 4 · Segmentation · Method", "Clustering 8 behavioural features yields four segments along three business axes",
  "deck_t4_k", "k = 4", "k-means on 8 z-scaled behavioural features, 999 customers",
  ["Inputs: 4 ratios (spend/income, utilization, discretionary, online), spending volatility, FHS, engagement score, transactions/month; no raw VND, no demographics",
   "k = 2 splits one-off users, k = 3 adds health, k = 4 adds activity; k ≥ 5 only subdivides",
   "Coverage 999 / 999 incl. 7 minors; preprocessed dataset task4_features.csv + dictionary in the ZIP"],
  SRC_K, "Preprocessing: 10,992 customer-months → 999 customers (yearly mean per ratio), 0 nulls. Features: FHS, spend/income, utilization, volatility, engagement, transactions, discretionary share, online share (z-scaled). Excluded: essential ratio (= 1 − discretionary); diversity, active days, recency (near-constant). Silhouette 0.25 = moderate separation, expected for behaviour.");

(() => {
  const s = p.addSlide(); s.background = { color: WHITE };
  header(s, "Task 4 · Segmentation · Profiles", "Four segments, four different jobs for the product team");
  img(s, "deck_t4_profile", 0.6, 1.7, 7.9, 5.1);
  const segs = [["Healthy & Engaged", "351 · 35.1%", "Best health, lowest spend/income → savings & opt-in offers"],
    ["Stretched & Engaged", "302 · 30.2%", "Spend/income 0.84, 20% had a stress month → budgeting + alerts"],
    ["High-Activity Users", "258 · 25.8%", "251 transactions/month, most volatile → planning reminders"],
    ["Occasional Online-First", "88 · 8.8%", "Seen ~1 month, 67% online (≈ brief's Emerging Digital) → habit nudges"]];
  segs.forEach((g, i) => {
    const y = 1.7 + i * 1.28;
    s.addShape(p.ShapeType.roundRect, { x: 8.8, y, w: 3.93, h: 1.13, rectRadius: 0.08, fill: { color: i === 1 ? NAVY : PALE }, line: { color: i === 1 ? NAVY : PALE } });
    T(s, g[0], { x: 9.0, y: y + 0.08, w: 2.4, h: 0.35, fontSize: 12.5, bold: true, color: i === 1 ? WHITE : NAVY });
    T(s, g[1], { x: 11.3, y: y + 0.08, w: 1.3, h: 0.35, fontSize: 11, bold: true, color: i === 1 ? LIGHT : BLUE, align: "right" });
    T(s, g[2], { x: 9.0, y: y + 0.45, w: 3.6, h: 0.62, fontSize: 10.5, color: i === 1 ? WHITE : INK, valign: "top" });
  });
  footer(s, 17, SRC_K);
  s.addNotes("The heatmap is the side-by-side comparison the brief asks for. Health splits Healthy from Stretched, activity isolates High-Activity (not more online: 21% vs 25% average; youngest, 60% female), and the Occasional group is defined by how rarely we see them (1.1 of 12 months). Suggested personas not formed: Essential-Spend-Focused = 4 customers; Healthy-but-Disengaged = 25, 24 of them Occasional.");
})();

slideOne(18, "Task 4 · Validation, limits & future work", "Segments are stable — and December hits every segment by ~13 points",
  "deck_t4_december", "0.99", "agreement across 20 random seeds (ARI, 1 = identical)",
  ["Bootstrap ARI 0.91; December cuts health 12.8–14.2 pts in every segment → reminders for all",
   "Limits: synthetic folded data; 88 occasional users rest on ~1 month; full-year segments form a continuum (silhouette 0.25); segments lean on age / gender (Cramér's V 0.23 / 0.13) → act on behaviour only",
   "Future work: hybrid rules + k-means, month-to-month trajectory features, chronological early-warning on next_month_low_health_flag (support only)"],
  SRC_K, "Stability: 20 seeds ARI 0.988; 80% bootstrap × 50 ARI 0.911; dropping December 0.873. GMM agrees 0.26 (Occasional identical). 2×2 median cross-check agrees on health (344/351, 273/302). Future work detail: hybrid model (rule for part-year customers + k = 3 on the full-year base), trajectory features (slope, December dip), chronological early-warning on next_month_low_health_flag trained Jan–Aug, validated Sep–Oct, tested Nov (support only).", { bigSize: 36, fs: 10.5 });

// ============ TASK 5 ============
(() => {
  const s = p.addSlide(); s.background = { color: WHITE };
  header(s, "Task 5 · Recommendations", "Six non-punitive tools, each tied to a measured finding");
  const H = (t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: NAVY }, fontSize: 11 } });
  const rows = [[H("Tool"), H("Target (n, % of 999)"), H("Evidence"), H("Action"), H("KPI")],
    ["① Budgeting", "Stretched & Engaged · 302 (30.2%)", "spend/income 0.84; r −0.90 with FHS", "Spend-vs-income view, self-set budget", "spend/income; stress months"],
    ["② Spend alerts", "Crossover · 43 (4.3%)", "52% of stress months; late-night spend", "Opt-in pacing alert before 22:00", "stress months / customer"],
    ["③ Planning reminders", "High-Activity · 258 (25.8%)", "volatility 1.91; December −13 pts", "Year-end plan sent in November", "Dec drop vs holdout"],
    ["④ Education", "FHS < 70 & engagement < 70 (yearly means) · 67 (6.7%)", "86% discretionary vs 55% base", "Needs-vs-wants micro-modules", "essential share"],
    ["⑤ Digital nudges", "Occasional Online-First · 88 (8.8%)", "1–2 active days; 60.6% via app/e-com", "Habit nudges in their app", "active days"],
    ["⑥ Product suggestions", "Healthy & Engaged, adults 18+ · 350 (35.0%)", "lowest utilization 0.15; FHS 70.5", "Opt-in savings/loyalty, no credit increase", "opt-in uptake"]];
  const body = rows.map((r, i) => i === 0 ? r : r.map((c) => ({ text: c, options: { fill: { color: i % 2 ? WHITE : PALE } } })));
  s.addTable(body, { x: 0.6, y: 1.75, w: 12.13, colW: [1.95, 2.85, 2.85, 2.7, 1.78], fontFace: FONT, fontSize: 11, color: INK,
    border: { type: "solid", pt: 0.5, color: "D5E2F2" }, valign: "middle", rowH: 0.62, margin: 0.06 });
  T(s, "Segments ① ③ ⑤ ⑥ cover all 999 customers (1 minor in Healthy & Engaged gets no product offer). Overlays: alerts 43 = 39 Stretched + 4 Healthy; education 67 = 64 Occasional + 3 Stretched (sequenced, never in the same week).",
    { x: 0.6, y: 6.25, w: 12.13, h: 0.55, fontSize: 11, italic: true, color: BLUE });
  footer(s, 19, SRC_K + "; " + SRC_M + "; " + SRC_T);
  s.addNotes("One tool per required type, each with an exact size, the column it rests on and a KPI. Every tool is opt-in and behaviour-triggered.");
})();

(() => {
  const s = slideOne(20, "Task 5 · Prioritisation", "Budgeting leads on reach × driver strength; alerts launch first for precision",
    "deck_t5_priority", "271", "priority score of the budgeting tool (302 × 0.90)",
    ["Reach × |r|: a ranking heuristic, not an impact estimate; wellbeing first",
     "Alerts reach only 43 customers but 71% of stress months → wave 1",
     "Fairness: behaviour-only triggers; uptake tracked by age & gender; no offers to minors"],
    SRC_M + "; " + SRC_K, "Wellbeing: Budgeting 271 → Reminders 128 → Alerts 37 → Education 32. Growth: Products 74 → Nudges 52. Targets skew (Reminders 60.5% female; Education/Nudges mean age ~58), so we monitor uptake by group rather than target by it.",
    { h: 3.55, fs: 11 });
  s.addShape(p.ShapeType.roundRect, { x: 9.05, y: 5.45, w: 3.68, h: 1.25, rectRadius: 0.1, fill: { color: NAVY }, line: { color: NAVY } });
  T(s, "NEVER", { x: 9.3, y: 5.5, w: 3.2, h: 0.5, fontSize: 22, bold: true, color: WHITE });
  T(s, "financial_health_score → deny credit, cut a limit, raise a rate or block an account", { x: 9.3, y: 5.98, w: 3.25, h: 0.65, fontSize: 10.5, color: ICE, valign: "top" });
})();

slideOne(21, "Task 5 · Impact", "What-if: a 10% spend trim would cut stress months by 28–32% — to be tested in a 90-day pilot",
  "deck_t5_scenario", "−28–32%", "stress months if the Stretched 302 trim spend-to-income by 10% (simulated, not measured)",
  ["What-if on FHS = 84.1 − 25.3 × spend/income; part of the gain is mechanical",
   "Roadmap: 0–30 d budgeting + alerts · 31–60 d November reminders + nudges · 61–90 d education + products",
   "Every tool vs a random 10% holdout for 3 months; scale only what wins"],
  SRC_M, "95 → 65 stress months with the all-customer slope, 68 with the slope inside the segment (−22.2); 9 of the 95 stress months sit outside the 302. Spend-to-income and utilization explain 82% of FHS, so only the holdout test can show real behaviour change. A hypothesis to measure, not a promise.",
  { bigSize: 34 });

// ============ 22 · CLOSING ============
(() => {
  const s = p.addSlide(); s.background = { color: NAVY };
  T(s, "THE CONTRACT", { x: 0.8, y: 0.8, w: 8, h: 0.4, fontSize: 13, bold: true, color: LIGHT, charSpacing: 3 });
  T(s, "Protect the stretched, plan with the active, re-engage the occasional, grow the healthy — without ever touching their credit.",
    { x: 0.8, y: 1.3, w: 11.7, h: 1.6, fontSize: 28, bold: true, color: WHITE });
  const cols = [["Why", "Overspending drives poor health (r −0.90); under stress 71.6% of spend is discretionary, and stress peaks in December."],
    ["Who", "4 stable segments cover all 999 customers; 43 active customers hold 52% of stress months."],
    ["What", "Budgeting for 302 and opt-in evening alerts first, each to be measured against a random holdout in a 90-day pilot."]];
  cols.forEach((c, i) => {
    const x = 0.8 + i * 3.97;
    s.addShape(p.ShapeType.roundRect, { x, y: 3.35, w: 3.75, h: 2.45, rectRadius: 0.08, fill: { color: "13345E" }, line: { color: "13345E" } });
    T(s, c[0], { x: x + 0.3, y: 3.5, w: 3.2, h: 0.5, fontSize: 18, bold: true, color: LIGHT });
    T(s, c[1], { x: x + 0.3, y: 4.05, w: 3.2, h: 1.6, fontSize: 13, color: WHITE, valign: "top" });
  });
  T(s, "Honest limits: synthetic data (two source years folded onto 2025), 91 customers seen only once, segments on a continuum — sizes are directional; conclusions rest on ratios.",
    { x: 0.8, y: 6.1, w: 11.7, h: 0.5, fontSize: 11, italic: true, color: ICE });
  T(s, "One guarantee: wellbeing help, never a credit decision.", { x: 0.8, y: 6.65, w: 11.7, h: 0.4, fontSize: 13, bold: true, color: WHITE });
  s.addNotes("If a judge remembers three things: overspending, not income; timing, not a blacklist; help offered, never credit taken away.");
})();

p.writeFile({ fileName: OUT }).then((f) => console.log("WROTE", f)).catch((e) => { console.error(e); process.exit(1); });
