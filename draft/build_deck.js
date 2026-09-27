// BI10 R01 — Group YAPPERS deck generator. Run: node draft/build_deck.js
const pptxgen = require("pptxgenjs");
const path = require("path");

const FIG = path.resolve(__dirname, "..", "outputs", "figures");
const img = (n) => path.join(FIG, n);
const OUT = path.resolve(__dirname, "YAPPERS_BI10_R01.pptx");

// ---- palette (teal-trust / navy wellbeing) ----
const DARK = "0F2A43", NAVY = "12435E", TEAL = "058B8C", MINT = "1FC3A6";
const INK = "1B2A36", MUTE = "5F7180", ICE = "EAF3F4", WHITE = "FFFFFF";
const HFONT = "Cambria", BFONT = "Calibri";

const p = new pptxgen();
p.layout = "LAYOUT_WIDE";           // 13.33 x 7.5 in, 16:9
const H = 7.5;

// ---------- helpers ----------
function bulletList(items, fs = 14) {
  return items.map((t) => ({
    text: t,
    options: { bullet: { code: "2022", indent: 14 }, breakLine: true,
               paraSpaceAfter: 7, color: INK, fontFace: BFONT, fontSize: fs },
  }));
}
function tag(slide, txt) {
  slide.addText(txt.toUpperCase(), { x: 0.5, y: 0.42, w: 8, h: 0.32, isTextBox: true, margin: 0,
    fontFace: BFONT, fontSize: 11, bold: true, color: TEAL, charSpacing: 2 });
}
function heading(slide, txt) {
  slide.addText(txt, { x: 0.5, y: 0.72, w: 12.3, h: 0.8, isTextBox: true, margin: 0,
    fontFace: HFONT, fontSize: 25, bold: true, color: NAVY, valign: "top", lineSpacingMultiple: 0.95 });
}
function footer(slide, n) {
  slide.addText("Group YAPPERS · BI10 Round 01", { x: 0.5, y: 7.08, w: 6, h: 0.3,
    isTextBox: true, margin: 0, fontFace: BFONT, fontSize: 9, color: MUTE });
  slide.addText(String(n), { x: 12.5, y: 7.08, w: 0.5, h: 0.3, isTextBox: true, margin: 0,
    align: "right", fontFace: BFONT, fontSize: 9, color: MUTE });
}
function chart(slide, name, x, y, w, h) {
  slide.addImage({ path: img(name), x, y, w, h, sizing: { type: "contain", w, h } });
}
function cap(s, txt, x, y, w) {
  s.addText("Source: " + txt, { x, y, w, h: 0.28, isTextBox: true, margin: 0, fontFace: BFONT, fontSize: 8.5,
    italic: true, color: MUTE, valign: "top" });
}
function statBox(s, st, y = 5.55) {
  s.addShape(p.ShapeType.roundRect, { x: 0.5, y, w: 3.7, h: 1.15, rectRadius: 0.08, fill: { color: NAVY } });
  s.addText(st[0], { x: 0.5, y: y + 0.08, w: 3.7, h: 0.68, isTextBox: true, margin: 0, align: "center",
    fontFace: HFONT, fontSize: 26, bold: true, color: MINT });
  s.addText(st[1], { x: 0.5, y: y + 0.76, w: 3.7, h: 0.33, isTextBox: true, margin: 0, align: "center",
    fontFace: BFONT, fontSize: 11, color: WHITE });
}
function base(sec, title) {
  const s = p.addSlide();
  s.background = { color: WHITE };
  tag(s, sec); heading(s, title);
  return s;
}
// one chart right, bullets left
function contentOne(n, sec, title, bullets, chartName, o = {}) {
  const s = base(sec, title);
  s.addText(bulletList(bullets, o.fs || 13), { x: 0.5, y: 1.6, w: 6.3, h: o.stat ? 3.85 : 5.1, isTextBox: true, valign: "top" });
  chart(s, chartName, 7.05, 1.6, 5.8, 4.5);
  cap(s, o.src, 7.05, 6.15, 5.8);
  if (o.cav)
    s.addText("⚠  " + o.cav, { x: 7.05, y: 6.45, w: 5.8, h: 0.55, isTextBox: true, margin: 0,
      fontFace: BFONT, fontSize: 9.5, italic: true, color: MUTE, valign: "top" });
  if (o.stat) statBox(s, o.stat);
  footer(s, n);
  if (o.note) s.addNotes(o.note);
}
// bullets top band, two charts below (widths optional)
function contentTwo(n, sec, title, bullets, c1, c2, o = {}) {
  const s = base(sec, title);
  s.addText(bulletList(bullets, o.fs || 12), { x: 0.5, y: 1.5, w: 12.3, h: 1.85, isTextBox: true, valign: "top" });
  const [w1, w2] = o.widths || [6.05, 6.05];
  chart(s, c1, 0.5, 3.35, w1, 3.3);
  chart(s, c2, 0.5 + w1 + 0.2, 3.35, w2, 3.3);
  cap(s, o.src, 0.5, 6.72, 12.3);
  footer(s, n);
  if (o.note) s.addNotes(o.note);
}
// bullets top band, one full-width chart
function contentWide(n, sec, title, bullets, chartName, o = {}) {
  const s = base(sec, title);
  s.addText(bulletList(bullets, o.fs || 12), { x: 0.5, y: 1.5, w: 12.3, h: 1.75, isTextBox: true, valign: "top" });
  chart(s, chartName, 0.5, 3.3, 12.3, 3.35);
  cap(s, o.src, 0.5, 6.72, 12.3);
  footer(s, n);
  if (o.note) s.addNotes(o.note);
}

// source strings
const M = "consumer_financial_health_engagement_2025 (10,992 consumer-months, 999 consumers, 2025).";
const T = "consumer_transactions_2025 (1,852,394 transactions, 2025).";
const J = "transactions joined to consumer-months on consumer_id + month.";
const K = "team k-means (k = 4) on 8 z-scaled ratios, 999 consumers (task4_features.csv).";

// ============ SLIDE 1 — TITLE ============
(() => {
  const s = p.addSlide();
  s.background = { color: DARK };
  s.addShape(p.ShapeType.rect, { x: 0, y: 0, w: 0.22, h: H, fill: { color: MINT } });
  s.addText("ITB CONSUMER WELLBEING & SEGMENTATION", { x: 0.9, y: 2.0, w: 11.5, h: 1.3, isTextBox: true, margin: 0,
    fontFace: HFONT, fontSize: 40, bold: true, color: WHITE });
  s.addText("Overspending, not low income, drives financial stress, and help can be timed to reach it", {
    x: 0.9, y: 3.35, w: 11.5, h: 0.6, isTextBox: true, margin: 0, fontFace: BFONT, fontSize: 18, italic: true, color: MINT });
  s.addText([
    { text: "999 consumers · 10,992 consumer-months · 1.85M transactions · calendar year 2025", options: { color: "CFE3E6", fontSize: 14, breakLine: true, paraSpaceAfter: 10 } },
    { text: "Group YAPPERS  ·  BI10 Round 01  ·  September 2026", options: { color: "9FB6BD", fontSize: 13 } },
  ], { x: 0.9, y: 4.4, w: 11, h: 1.2, isTextBox: true, margin: 0, fontFace: BFONT });
  s.addNotes("This is a wellbeing study, not credit scoring. In one line: people slide into stress because they overspend on wants, usually in specific months, so ITB can offer help at the right time and never touch anyone's credit.");
})();

// ============ SLIDE 2 — EXECUTIVE SUMMARY ============
(() => {
  const s = p.addSlide();
  s.background = { color: DARK };
  s.addText("EXECUTIVE SUMMARY", { x: 0.6, y: 0.45, w: 8, h: 0.4, isTextBox: true, margin: 0,
    fontFace: BFONT, fontSize: 12, bold: true, color: MINT, charSpacing: 3 });
  s.addText("Overspending drives stress, and it is timed, reachable and fixable", { x: 0.6, y: 0.85, w: 12.2, h: 0.8,
    isTextBox: true, margin: 0, fontFace: HFONT, fontSize: 28, bold: true, color: WHITE });
  const rows = [
    ["T1 · The budget flips under stress", "Stressed months (FHS < 40) are 71.6% discretionary vs 40.5% in healthy months (FHS ≥ 80), a steady gradient across every band. The flip is in value: purchases ≥ 10M VND are 4% of stressed-month transactions but 54% of their spend."],
    ["T2 · Overspending, not low income", "Spend-to-income (r −0.90) and credit utilization (r −0.86), one overspending factor, explain ~82% of the health score. Nobody is stressed all year, yet 87% dip below 60 at least once; 43 active customers hold 52% of stress months."],
    ["T3 · Engagement is saturated", "91% of customers are High / Very-high engaged; the whole low tail is 91 customers seen on only 1–2 days in 2025. Among full-year customers, category breadth (r +0.81) and active days (r +0.80) drive engagement."],
    ["T4 · Four segments, 100% covered", "Healthy & Engaged 351 · Stretched & Engaged 302 · High-Activity 258 · Occasional Online-First 88; stable across random seeds (agreement 0.99 of 1). December lowers health ~13 points in every full-year segment."],
    ["T5 · Six opt-in tools, one rule", "Ranked by reach × driver strength: Budgeting (302) → November Reminders (258) → Spend Alerts (43, launched first). A 10% spend trim could cut stress months 28–32% (what-if). FHS never denies, cuts, prices or blocks credit."],
  ];
  let y = 1.85;
  rows.forEach((r) => {
    s.addText(r[0], { x: 0.6, y, w: 3.7, h: 0.95, isTextBox: true, margin: 0, valign: "top",
      fontFace: BFONT, fontSize: 14.5, bold: true, color: MINT });
    s.addText(r[1], { x: 4.45, y, w: 8.35, h: 0.95, isTextBox: true, margin: 0, valign: "top",
      fontFace: BFONT, fontSize: 12.5, color: "DCEAEC" });
    y += 1.03;
  });
  s.addNotes("One row per task: the signal, the driver and timing, engagement, the segments, then the plan and the ethical rule. The 82% is the share of FHS variance explained by the two ratios (R² 0.82). The 28–32% is a what-if scenario, tested with holdouts on slide 21.");
})();

// ============ SLIDE 3 — TABLE OF CONTENTS ============
(() => {
  const s = base("Contents", "What this deck covers");
  const items = [
    ["01", "Introduction to the Case & data quality", "slide 4"],
    ["02", "Task 1 — Exploratory Data Analysis", "slides 5–8"],
    ["03", "Task 2 — Financial Health Analysis", "slides 9–12"],
    ["04", "Task 3 — Customer Engagement Analysis", "slides 13–15"],
    ["05", "Task 4 — Customer Segmentation", "slides 16–18"],
    ["06", "Task 5 — Recommendations & Impact", "slides 19–22"],
  ];
  items.forEach((it, i) => {
    const col = Math.floor(i / 3), row = i % 3;
    const x = 0.7 + col * 6.3, y = 2.0 + row * 1.5;
    s.addShape(p.ShapeType.roundRect, { x, y, w: 0.85, h: 0.85, rectRadius: 0.42,
      fill: { color: ICE }, line: { color: MINT, width: 1.5 } });
    s.addText(it[0], { x, y, w: 0.85, h: 0.85, isTextBox: true, margin: 0, align: "center",
      valign: "middle", fontFace: HFONT, fontSize: 22, bold: true, color: TEAL });
    s.addText([{ text: it[1], options: { bold: true, color: INK, fontSize: 15, breakLine: true } },
               { text: it[2], options: { color: MUTE, fontSize: 12 } }],
      { x: x + 1.05, y, w: 4.9, h: 0.85, isTextBox: true, margin: 0, valign: "middle", fontFace: BFONT });
  });
  footer(s, 3);
  s.addNotes("Four required sections: Executive Summary (2), Contents (3), Introduction (4), Task results (5–21). Each task follows the brief's question order.");
})();

// ============ SLIDE 4 — INTRODUCTION + DATA QUALITY ============
(() => {
  const s = base("Introduction", "The case: understand wellbeing, never score credit");
  s.addText(bulletList([
    "ITB, a Vietnamese consumer-finance company, wants to understand customers' financial wellbeing, spending and channel engagement, and to segment them. It does not want credit-risk decisions.",
    "We compare ratios and shares, never absolute VND: synthetic income, credit and balance amounts are inflated (case §12).",
    "Stress is measured per customer-month, because it comes and goes. Segments are measured per customer, as a yearly average profile.",
    "Process: data-quality checks → EDA → financial health → engagement → segmentation → recommendations. Every number reproduces from notebooks/full_pipeline.ipynb.",
  ], 12.5), { x: 0.5, y: 1.6, w: 6.3, h: 3.6, isTextBox: true, valign: "top" });
  s.addShape(p.ShapeType.roundRect, { x: 0.5, y: 5.3, w: 6.3, h: 1.3, rectRadius: 0.08, fill: { color: NAVY } });
  s.addText([
    { text: "Ethical rule  ", options: { bold: true, color: MINT, fontSize: 13 } },
    { text: "financial_health_score is a wellbeing indicator. It is never used to approve or deny credit, cut a limit, raise a rate or block an account. A low score only triggers help the customer can accept or ignore.", options: { color: WHITE, fontSize: 12 } },
  ], { x: 0.7, y: 5.36, w: 5.9, h: 1.18, isTextBox: true, margin: 0, valign: "middle", fontFace: BFONT });

  [["999", "consumers"], ["10,992", "consumer-months"], ["1.85M", "transactions"], ["34", "provinces"]].forEach((st, i) => {
    const x = 7.05 + i * 1.47;
    s.addShape(p.ShapeType.roundRect, { x, y: 1.6, w: 1.35, h: 1.05, rectRadius: 0.08, fill: { color: ICE } });
    s.addText(st[0], { x, y: 1.66, w: 1.35, h: 0.55, isTextBox: true, margin: 0, align: "center",
      fontFace: HFONT, fontSize: 19, bold: true, color: NAVY });
    s.addText(st[1], { x, y: 2.2, w: 1.35, h: 0.35, isTextBox: true, margin: 0, align: "center",
      fontFace: BFONT, fontSize: 10, color: MUTE });
  });
  s.addShape(p.ShapeType.roundRect, { x: 7.05, y: 2.85, w: 5.8, h: 3.75, rectRadius: 0.06,
    fill: { color: WHITE }, line: { color: MINT, width: 1.2 } });
  const dq = [
    ["✓", "0 missing cells · 0 duplicate transaction IDs or consumer-months · 0 negative amounts"],
    ["✓", "Every timestamp in 2025; 1 name + birth date per consumer, 1 name per merchant (693)"],
    ["✓", "Transactions reconcile 100% to monthly total_spend (10,992 / 10,992 months)"],
    ["⚠", "Coverage: 908 customers have all 12 months; 91 appear in only 1–2 months (1–2 active days)"],
    ["✓", "5 over-limit months (utilization 1.03–1.5, all FHS < 35) kept as real behaviour"],
    ["✓", "7 minors (aged 15–17) kept and binned, not dropped"],
    ["⚠", "Case §12: two source years folded onto 2025 inflate volumes; engagement skews high → ratios are the signal"],
  ];
  s.addText([{ text: "Data-quality checks — both files", options: { bold: true, color: TEAL, fontSize: 13, breakLine: true, paraSpaceAfter: 6 } },
    ...dq.map((d, i) => ({ text: d[0] + "  " + d[1], options: { color: INK, fontSize: 10.5, breakLine: i < dq.length - 1, paraSpaceAfter: 5 } }))],
    { x: 7.25, y: 2.95, w: 5.45, h: 3.6, isTextBox: true, margin: 0, valign: "top", fontFace: BFONT });
  footer(s, 4);
  s.addNotes("Two rules govern the deck: ratios over magnitudes, wellbeing over credit. The data is clean; the caveats are the synthetic ones the case documents plus 91 customers seen only once, and we flag them wherever they touch a number.");
})();

// ============ SLIDES 5–21 (auto-numbered) ============
let N = 4;

// ---- Task 1 ----
contentOne(++N, "Task 1 · EDA · Q1", "December = 15% of annual spend, driven by trip frequency, not tickets",
  ["Peak: December 488.0B VND = 15.04% of the 3.24T annual spend. Trough: February 174.4B = 5.37%. Gap +313.7B VND (+9.7pp): December is 2.8× February.",
   "Driver is count: transactions +187% (97,657 → 280,598) while the average ticket slips 2.6% (1.79M → 1.74M VND). Count explains the entire lift.",
   "Same customers, more trips: active consumers flat (919 → 918), transactions per consumer 106 → 306. All 14 categories grow +181% to +193% in transactions.",
   "Reveals: the peak is a burst of everyday frequency, and December is the weakest-health month (avg FHS 54.2 vs 73.6 in Feb) → plan support before December."],
  "v2_t1_q1_decomposition.png",
  { src: T, stat: ["2.9×", "transactions per customer, Dec vs Feb"],
    cav: "Case §12: two source years folded onto 2025 inflate absolute VND in every month; shares and ratios (15.04%, 2.8×) are the reliable signal.",
    note: "December is not new customers or pricier baskets: the same ~918 customers transact almost three times as often, even per day. That burst coincides with the year's lowest average health score (54.2), so the peak is also the pressure point we return to in Task 2 and Task 5." });

contentTwo(++N, "Task 1 · EDA · Q2 — the spine", "Stress flips the budget: 71.6% discretionary vs 40.5% when healthy",
  ["Stressed months (FHS < 40; 95 consumer-months, 70 consumers): 28.4% essential / 71.6% discretionary. Healthy months (FHS ≥ 80; 475 months, 303 consumers): 59.5% / 40.5%. A steady gradient across FHS bands: 71.6 → 64.2 → 57.3 → 54.4 → 49.2 → 40.5%.",
   "The flip is in value, not habits: essentials are ~47% of transactions in both groups, but the discretionary ticket is 3.9M vs 1.1M VND. Purchases ≥ 10M VND are 4.3% of stressed-month transactions yet 54% of their value (healthy: 0.4% → 3%).",
   "Travel alone adds +22pp of value share, online shopping +11pp; the mix stays inverted without travel (37% vs 60% essential). Stress = a few large discretionary purchases → pre-purchase alerts, not credit restriction."],
  "t1_essential_discretionary.png", "v2_t1_q2_category_shift.png",
  { src: M + " Category shift: " + J,
    note: "Stressed customers do not buy wants more often: essentials are about 47% of their transactions, like healthy customers. The inversion comes from a few very large discretionary tickets, above all travel. FHS partly reflects spend-to-income, so read this as co-occurrence, not cause." });

contentOne(++N, "Task 1 · EDA · Q3", "High-spend hubs trail digital by ≤ 0.46pp; geography is not the lever",
  ["6 provinces combine above-median spend (> 82.7B VND) with below-average digital share (non-POS; national 41.2%): Ha Noi, Dong Nai, Lam Dong, Hung Yen, Hai Phong, Nghe An.",
   "Breakdown: POS 58.9–59.3% vs 58.8% nationally; QR at par (19.7–20.3% vs 19.9%). All 6 trail on both E-commerce (to −0.31pp) and Mobile App (to −0.32pp).",
   "Size: largest gap −0.46pp (Dong Nai); only 3 of 6 significant (p < 0.05). Leaders: HCMC 13.6% of spend at 41.3%; range Cao Bang 43.1% → Quang Ngai 39.2%.",
   "Customers differ 8.7pp (p10–p90 digital share 37.2–45.9%) vs 3.9pp across all 34 provinces → drive digital adoption per customer, not per region."],
  "v2_t1_q3_channel_gap.png",
  { fs: 12, src: T, stat: ["−0.46pp", "largest digital gap among high-spend hubs"],
    cav: "Digital = non-POS incl. QR. On online_transaction_flag (excl. QR, national 21.3%) Lam Dong drops out; other gaps stay ≤ 0.6pp.",
    note: "Six high-spend provinces technically qualify, but they lag only in app and e-commerce use, and by fractions of a point. Customers within any province differ far more than provinces do, so a regional digital campaign would miss the real variation." });

contentTwo(++N, "Task 1 · EDA · Q4 & Q5", "Fuel is the habit, groceries the wallet; 25–34 is weakest, barely",
  ["Q4 — Top by count: Fuel & Transport, 188,029 transactions (10.2%), avg ticket 1.59M VND, 17.3 buys per buyer-month. Top by spend: in-store Groceries, 513.8B VND (15.8% of value), avg ticket 2.92M (1.8× fuel). Fuel = frequent top-ups; groceries = stock-up baskets.",
   "Q5 — 25–34 has the lowest mean FHS (65.8 vs best 67.0) while staying active (178.7 transactions/month vs cohort median 177.8). It is the only cohort above national spend-to-income (0.716 vs 0.700) AND below the national essential ratio (0.468 vs 0.481).",
   "Honest limit: the cohort spread is 1.2 pts, 95% CIs overlap and ANOVA p = 0.13; counting each consumer once, 15–24 ties (65.75 vs 65.79). Age is a weak lever: target spend-to-income, not birth year."],
  "v2_t1_q4_category.png", "v2_t1_q5_age.png",
  { src: T + " Age cohorts: consumer-month file; 95% CIs from consumer-level bootstrap.",
    note: "Fuel and groceries are both near-universal essentials but serve different jobs. On age, 25–34 answers Q5 as asked (active, lowest score, highest spend-to-income), but the spread is 1.2 points and not significant, so the actionable variable is spend-to-income." });

// ---- Task 2 ----
contentOne(++N, "Task 2 · Financial Health · D1", "Nobody is stressed on average, yet 87% dip below 60 at some point",
  ["Consumer level (average of each consumer's months, n = 999): mean 66.3, median 66.2, std 4.7, IQR 63.4–69.3, range 42.3–80.8 — a tight band.",
   "Month level (n = 10,992): std 9.5, 2× wider. Stable 72.5% · Watch 22.4% · Healthy (≥ 80) 4.3% · Stressed (< 40) 0.9% = 95 months across 70 consumers.",
   "0 of 999 average below 40, but 869 (87%) fall below 60 in at least one month; who the customer is explains only 22% of monthly variance, the calendar month 25%.",
   "Stress peaks at year-ends: January + December hold 46 of 95 stressed months (mean FHS Feb 73.6 → Dec 54.2) → trigger support on the month, not a static list."],
  "v2_t2_distribution.png",
  { fs: 12.5, src: M + " Consumer level = mean of available months (908 consumers have 12, 91 have 1–2).",
    stat: ["87%", "dip below 60 at least once"],
    note: "Averaging each person makes everyone look fine: the lowest consumer average is 42. Month by month almost everyone has a bad month, and stress spikes in December and January. So the right unit for help is the customer-month." });

contentTwo(++N, "Task 2 · Financial Health · D2", "Low health is overspending: it breaks once spend passes income",
  ["One factor dominates (month grain, n = 10,992): spend-to-income r −0.90 and credit utilization r −0.86 move together (r 0.90) and jointly explain 82% of FHS variance; the link also holds within each consumer (r −0.90).",
   "Threshold: 98% of stressed months spend more than income; in the top spend-to-income quintile (avg 1.21) 93% of months fall below 60, and none do in the bottom two quintiles.",
   "What they buy (transactions): stressed months are 72% discretionary by value vs 40% in healthy months, with 2× the e-commerce + app share (23% vs 12%). They are also MORE engaged (81.1 vs 72.7). Shared inputs → directional, not causal."],
  "v2_t2_sti_threshold.png", "t2_low_health_drivers.png",
  { src: M + " Category mix: " + J,
    note: "The two headline ratios are one story: spending relative to capacity. The practical line is spend-to-income above 1, which almost every stressed month crosses. The transaction file shows the extra spend is discretionary and online, which tells a budgeting tool what to watch." });

contentWide(++N, "Task 2 · Financial Health · D3", "Occupation and province gaps are really spending gaps; age is flat",
  ["Occupation (396 titles → 8 keyword groups + Other; consumer level): Eng/science/IT 69.1 (n = 229) and Business/finance 68.7 (126) vs Office/public 64.5 (443) and Manual/trades 62.9 (23), a 6.2-pt spread mirroring spend-to-income 0.61 vs 0.76–0.79.",
   "Province (27 with ≥ 15 consumers): Thai Nguyen 63.0 to Ha Noi 67.8; real but small (ANOVA p = 0.009, 5% of variance). Age: six cohorts within 65.8–67.0, not significant (p = 0.13).",
   "Hold spend-to-income constant and the occupation spread falls to 1.3 pts and province to 1.6 pts (p = 0.62). Target the ratio, never the group — the fairer and more effective lever."],
  "v2_t2_demog_adjusted.png",
  { src: M + " Consumer level, n = 999; adjustment = residual of FHS on spend-to-income (linear).",
    note: "All three cuts the brief asks for are here. Occupation shows the biggest gap, but it almost disappears once we account for spending relative to income; the same holds for province. That is why the recommendations target behaviour, not demographics." });

contentTwo(++N, "Task 2 · Financial Health · D4", "43 active customers carry 52% of stress months — reach them before 22:00",
  ["Rule (consumer-month): financial_health_score < 40 AND engagement_score ≥ 81.4 (the top 25% of all 10,992 consumer-months, a fixed constant). It flags 49 months / 43 consumers = 52% of stressed months vs 25% by chance (p < 0.001); top 30% / 20% give 44 / 41 consumers.",
   "Profile: spend/income 1.89, utilization 0.55, discretionary 71%, online share 0.49 (2.3× the 0.21 average). All 43 are full-year customers averaging FHS 62 in other months; 39 of them sit in the Stretched & Engaged segment.",
   "When (transactions): 22:00–23:59 carries 23.5% of stressed-month spend value vs 8.3% in healthy months (count only 11.6% vs 9.7%), led by online shopping 39% and travel 14% → opt-in spend alerts before 22:00. Wellbeing use only."],
  "t2_crossover.png", "v2_t2_latenight.png",
  { src: M + " Timing: " + J,
    note: "The rule has two fixed thresholds on monthly fields, so anyone can rerun it. More than half of all stress happens to customers already very active in our channels, and the transaction file tells us when: late evening, big online baskets." });

// ---- Task 3 ----
contentTwo(++N, "Task 3 · Engagement · D1–D2", "Engagement is saturated; digital share is what varies",
  ["D1: engagement_score mean 77.8, median 78.1, IQR 74.8–81.4. Official bands (40/60/80) per month: Low 0.1% · Medium 0.9% · High 64.2% · Very high 34.8%. Per consumer (average score): 1.0% · 8.0% · 66.9% · 24.1% — 91% High or Very high.",
   "All 91 consumers below 'High' used the card on only 1–2 days all year; every one of the 908 full-year consumers averages ≥ 69.8. The score separates one-off users from the base, not good customers from great ones.",
   "D2: POS 58.8% · QR 19.8% · E-commerce 8.7% · Mobile App 7.7% · Recurring 4.9% of transactions; 925 of 999 use all 5. Average online spend share 21.0% of spend (consumer median 20.4%, full-year range 12–36%); it tracks engagement (r +0.86)."],
  "v2_t3_engagement_segments.png", "v2_t3_channel_mix.png",
  { src: M + " Channels: " + T,
    note: "The histogram shows the continuous score; shading the official 40/60/80 bands answers the share-per-segment question on the same axis, at month and consumer grain, so the 1% tail stays visible where a pie would hide it. Channels are nominal, so a sorted bar labelled with trip share, value share and adoption fits." });

contentTwo(++N, "Task 3 · Engagement · D3–D4", "Breadth and regular use track engagement; recency only flags one-offs",
  ["D3: category diversity ranges 2–14 per month; the 908 full-year consumers average 12.5–14, the 91 one-off users 2–7. r = +0.94 across all consumers and still +0.81 within the full-year base (Spearman +0.79): breadth matters beyond the tail.",
   "D4: recency 0–30 days (median 0), active days 1–31 (median 30), 2–713 transactions per month (median 150). Full-year consumers: recency ≤ 4 days, active days 15–31. Links (consumer, full-year): active days r +0.80, count +0.76, recency −0.58.",
   "Heatmap: 30–31 active days & recency 0 → engagement 79.8 (n = 6,614 months); every 1–5-active-day cell stays ≤ 55 → watch falling breadth and active days, not recency."],
  "v2_t3_diversity_engagement.png", "t3_recency_frequency.png",
  { src: M,
    note: "Diversity and engagement are both continuous, so a scatter fits; colouring the one-off users shows the r = 0.94 is partly two clusters, and the within-base r = 0.81 shows the link holds anyway. Recency × frequency is an interaction of two binned variables, so a heatmap with cell counts fits." });

contentOne(++N, "Task 3 · Engagement · D5", "25 healthy customers used the card on only 1–2 days all year",
  ["Cutoff: FHS ≥ 70 (top 21%, p79) AND engagement < 70 (below the consumer p10 = 71.1) → 25 consumers = 2.5% of the base, 11.8% of the 211 healthy.",
   "Why 70: one-off users score ≤ 61.6 and full-year consumers ≥ 69.8, so cutoffs 60–70 all give 25; < 72 / 75 pull in active users (36 / 63). FHS ≥ 65 → 48 (not clearly healthy); ≥ 75 → 9.",
   "Profile vs rest: 2.0 vs 27.0 active days · 9.9 vs 159 transactions/month · diversity 4.7 vs 13.1 · online 0.61 vs 0.24 · age 61 vs 50 · spend/income 0.46 vs 0.70.",
   "19 of 25 were last seen in Jan–Jul (silent 5+ months); 24 of 25 are Occasional Online-First → play = win back everyday use, not budgeting."],
  "v2_t3_quadrant.png",
  { fs: 12, src: M, cav: "n = 25, one month of data each: FHS is a single reading. A watch-list, not a sized forecast; never used to limit credit.",
    note: "Health and engagement are two continuous scores, so a quadrant scatter with both cutoffs fits. The shaded empty band between 61.6 and 69.8 and the inset curve show the 70 cutoff sits in a real gap in the data. These are healthy, older, low-spend users whose single burst was mostly digital: the play is reactivation." });

// ---- Task 4 ----
contentOne(++N, "Task 4 · Segmentation · Method", "Three business axes, one model: coverage, health and activity",
  ["Preprocessing: 10,992 consumer-months → 999 consumers (yearly mean per ratio), 0 nulls, raw VND excluded. The preprocessed dataset + dictionary are in the ZIP (task4_features.csv).",
   "8 z-scaled inputs: health (FHS, spend/income, utilization, volatility) · activity (engagement, transactions) · mix (discretionary, online share).",
   "Excluded with reason: essential ratio (= 1 − discretionary); diversity, active days, recency (p75 already at the best value). Demographics used for profiling only, never as inputs.",
   "Why k = 4 (k-means): k = 2 splits off part-year customers, k = 3 adds health, k = 4 adds activity; k ≥ 5 only subdivides. Silhouette 0.25 (separation, 0–1); coverage 999 / 999 incl. 7 minors."],
  "v2_t4_k_selection.png",
  { fs: 12.5, src: K,
    note: "We cluster on ratios only, one row per customer, and keep demographics out so segments describe behaviour, not who people are. k = 4 is not a matter of taste: each added cluster separates a new business axis, and beyond four the model only subdivides." });

contentTwo(++N, "Task 4 · Segmentation · Profiles", "Four segments, four different jobs for the product team",
  ["Healthy & Engaged 351 (35.1%): best FHS 70.5, lowest spend/income 0.57, utilization 0.15 → savings & opt-in product offers.  ·  Stretched & Engaged 302 (30.2%): spend/income 0.84, utilization 0.25, 20% had a stress month → budgeting tool + spend alerts.",
   "High-Activity Users 258 (25.8%): 251 transactions/month (1.6× average), 30 active days, highest volatility 1.91; not more online (21% vs 25% average); youngest (43), 60% female → volatility smoothing, year-end planning reminders.",
   "Occasional Online-First 88 (8.8%) ≈ the brief's Emerging Digital: seen 1.1 of 12 months, 1.9 active days, 67% online, 75% of value non-POS → digital nudges to build a habit; scores rest on ~1 month (low confidence)."],
  "v2_t4_sizes.png", "v2_t4_profile_heatmap.png",
  { widths: [4.6, 7.5], src: K + " Non-POS share from " + T,
    note: "The heatmap is the side-by-side comparison: top rows are model inputs, bottom rows profile-only checks. Health splits Healthy from Stretched, activity isolates High-Activity, and the Occasional group is defined by how rarely we see them. Each segment maps to one tool in Task 5; none touches credit decisions." });

(() => {   // validation + limitations & future work
  const n = ++N;
  const s = base("Task 4 · Segmentation · Validation & limits", "Stable where it matters, honest where it is thin");
  s.addText(bulletList([
    "Stability (ARI, 1 = identical groups): 20 random seeds 0.988; 80% bootstrap × 50 0.911; dropping December 0.873. Changing features or aggregation moves ~⅓ of labels (0.62–0.63).",
    "Structure: Occasional is distinct (silhouette 0.47; = \"seen < 12 months\", ARI 0.98); the 3 full-year segments form a continuum (0.19–0.27; GMM ARI 0.26) → zones, not types.",
    "2×2 cross-check: the health axis agrees (344/351 Healthy above the FHS median, 273/302 Stretched below); the engagement median (78.2) does not separate them → activity axis added.",
    "December cuts FHS 12.8 / 14.2 / 13.4 pts in all 3 full-year segments alike → a calendar effect: reminders go to everyone. Age / gender differ (Cramér's V 0.19 / 0.13) → act on behaviour.",
  ], 11.5), { x: 0.5, y: 1.5, w: 6.4, h: 3.4, isTextBox: true, valign: "top" });
  chart(s, "v2_t4_pca.png", 7.05, 1.5, 5.8, 3.05);
  cap(s, K + " PCA of 8 z-scaled features = 73% of variance.", 7.05, 4.58, 5.8);
  const box = (x, title, lines) => {
    s.addShape(p.ShapeType.roundRect, { x, y: 4.95, w: 6.05, h: 2.0, rectRadius: 0.06, fill: { color: ICE } });
    s.addText([{ text: title, options: { bold: true, color: TEAL, fontSize: 12.5, breakLine: true, paraSpaceAfter: 4 } },
      ...lines.map((t, i) => ({ text: "•  " + t, options: { color: INK, fontSize: 10.5, breakLine: i < lines.length - 1, paraSpaceAfter: 3 } }))],
      { x: x + 0.18, y: 5.03, w: 5.7, h: 1.86, isTextBox: true, margin: 0, valign: "top", fontFace: BFONT });
  };
  box(0.5, "Limitations", [
    "Moderate separation (silhouette 0.25); full-year segments are a continuum sensitive to feature choice.",
    "Yearly means hide trajectory; 91 customers seen < 12 months carry ~1-month scores (low confidence).",
    "Synthetic data, two source years folded onto 2025, engagement saturated. Wellbeing groups only: never lending, limits or pricing.",
  ]);
  box(6.8, "Future work", [
    "Hybrid model: a rule for part-year customers + k-means k = 3 on full-year customers (ARI 0.86 vs today).",
    "Trajectory features (within-year FHS SD: 17.1 Occasional vs 7.7 Healthy) and GMM soft membership.",
    "Chronological early-warning on next_month_low_health_flag (train Jan–Aug, test Nov), to offer help only.",
  ]);
  footer(s, n);
  s.addNotes("The segments survive re-seeding, resampling and removing December, so they are safe to act on. We are explicit that the three full-year groups are zones on a continuum and that the smallest group is defined by how rarely we see them. ARI measures agreement between two groupings (1 = identical); silhouette measures separation (0–1).");
})();

// ---- Task 5 ----
(() => {   // six tools as a table
  const n = ++N;
  const s = base("Task 5 · Recommendations", "Six non-punitive tools, each tied to a measured data finding");
  const Hd = (t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: NAVY }, fontSize: 10.5 } });
  const rows = [[Hd("Tool"), Hd("Target group (n, % of 999)"), Hd("Data evidence"), Hd("Action"), Hd("KPI")],
    ["① Budgeting tool", "Stretched & Engaged: 302 (30.2%)", "spend/income 0.84 vs 0.57 Healthy; r(spend/income, FHS) −0.90", "Spend-vs-income dashboard + self-set discretionary budget", "spend/income; % months FHS < 40"],
    ["② Spend alerts", "Crossover: 43 (4.3%) — 39 Stretched + 4 Healthy", "49 of 95 stress months (52%); 23.5% of stressed spend at 22–23h", "Opt-in, dismissible pacing alert in the evening, before 22:00", "stress months per consumer"],
    ["③ Planning reminders", "High-Activity Users: 258 (25.8%)", "highest volatility 1.91 (r −0.50); December cuts FHS ~13 pts in every segment", "Monthly set-aside prompt; year-end plan sent in November", "December FHS drop vs holdout"],
    ["④ Financial education", "Low-health & low-engagement: 67 (6.7%)", "86% discretionary vs 55% base; 64 of 67 are occasional users", "Needs-vs-wants micro-modules built on their own spend mix", "essential share next active month"],
    ["⑤ Digital nudges", "Occasional Online-First: 88 (8.8%)", "seen on 1–2 days only; 60.5% of spend via E-com + Mobile", "Onboarding + category-broadening nudges in the app they use", "active days; categories / month"],
    ["⑥ Product suggestions", "Healthy & Engaged: 351 (35.1%), adults only", "lowest utilization 0.148, highest FHS 70.5", "Opt-in savings / loyalty; never a credit-line increase", "opt-in uptake; FHS stable"]];
  s.addTable(rows, { x: 0.5, y: 1.55, w: 12.3, colW: [1.75, 2.55, 3.35, 3.0, 1.65], fontFace: BFONT, fontSize: 10, color: INK,
    border: { type: "solid", pt: 0.5, color: "C9D6DB" }, fill: { color: WHITE }, valign: "middle", rowH: 0.62 });
  cap(s, K + " Crossover, low-health group and r: consumer-month file; timing and channels: transactions file.", 0.5, 6.05, 12.3);
  s.addText("Segments ① ③ ⑤ ⑥ partition all 999 customers. Overlays: Alerts 43 = 39 Stretched + 4 Healthy; Education 67 = 64 Occasional + 3 Stretched, so those 64 receive ④ and ⑤ in sequence, never in the same week.", {
    x: 0.5, y: 6.35, w: 12.3, h: 0.6, isTextBox: true, margin: 0, fontFace: BFONT, fontSize: 11, italic: true, color: TEAL });
  footer(s, n);
  s.addNotes("One tool per required type, each with an exact size, the column it rests on and a KPI. The only double contact is 64 occasional customers who get education and nudges, staggered.");
})();

contentOne(++N, "Task 5 · Recommendations", "Prioritisation by reach × driver strength — and the credit rule",
  ["Score = reach (consumers) × driver strength (|r| of the tool's trigger column with the outcome it should move, month level). Wellbeing tools (outcome FHS) rank before growth tools (outcome engagement).",
   "Wellbeing: ① Budgeting 271 → ③ Reminders 128 → ② Alerts 37 → ④ Education 32. Growth: ⑥ Products 74 → ⑤ Nudges 52. Alerts still ships first: its 43 customers hold 71% of stress months.",
   "Fairness audit: triggers are behaviour only, but targets skew — Reminders 60.5% female (base 50.6%); Education / Nudges mean age ~58 (base 50). We track uptake by age and gender; minors get no offers.",
   "RULE: financial_health_score is never used to deny credit, cut a credit limit, raise a rate or block an account. A low score only triggers help that is offered."],
  "v2_t5_priority_score.png",
  { fs: 12, src: "team analysis on the consumer-month file (10,992 months) + task4_features.csv; |r| = Pearson, month level.",
    stat: ["NEVER", "FHS → credit decision"],
    note: "The chart's axes are the two ranking inputs, so the order is reproducible. Budgeting wins on both. Alerts is small but precise, so it launches in wave 1. The rule is the contract: help offered, never access removed." });

contentOne(++N, "Task 5 · Impact", "A 10% spend trim could cut stress months 28–32%, tested in 90 days",
  ["What-if: FHS = 84.1 − 25.3 × spend-to-income (r −0.90). If the Stretched 302 cut spend-to-income by 10%, stress months fall 95 → 65–68 (−28% to −32%).",
   "Directional only: spend-to-income + utilization explain 82% of FHS, so part of the gain is mechanical; 9 of the 95 stress months sit outside the 302.",
   "Measurement: each tool has one KPI against a random 10% holdout for 3 months; Reminders are judged on the December FHS drop vs holdout.",
   "Days 0–30: Budgeting + Alerts · 31–60: November Reminders + Digital Nudges · 61–90: Education + opt-in Products. Scale only what beats its holdout."],
  "v2_t5_impact_scenario.png",
  { src: "team what-if on the consumer-month file (10,992 months); OLS slopes, all customers vs Stretched only.",
    stat: ["65–68", "stress months (from 95) at a 10% trim"],
    cav: "Illustrative: the slope is partly built into the FHS formula, so only the holdout test can show real behaviour change.",
    note: "This is a hypothesis we will measure, not a promise. Even the conservative slope removes about a quarter of stress months, and the holdout tells us which tools earn scale." });

// ============ SLIDE 22 — CLOSING ============
(() => {
  const s = p.addSlide();
  s.background = { color: DARK };
  s.addShape(p.ShapeType.rect, { x: 0, y: 0, w: 0.22, h: H, fill: { color: MINT } });
  s.addText("THE CONTRACT", { x: 0.9, y: 0.8, w: 8, h: 0.4, isTextBox: true, margin: 0,
    fontFace: BFONT, fontSize: 12, bold: true, color: MINT, charSpacing: 3 });
  s.addText("Protect the stretched, plan with the active, re-engage the occasional, grow the healthy — without ever touching their credit.", {
    x: 0.9, y: 1.25, w: 11.6, h: 1.7, isTextBox: true, margin: 0, fontFace: HFONT, fontSize: 26, bold: true, color: WHITE, lineSpacingMultiple: 1.05 });
  const pts = [
    ["The spine", "Overspending drives poor health (r −0.90). Under stress the budget flips to 71.6% discretionary. Stress comes in episodes and peaks in December."],
    ["The segments", "4 segments (351 / 302 / 258 / 88) covering all 999 customers, stable across seeds, each with its own opt-in tool."],
    ["Lead action", "Budgeting for the Stretched 302, plus evening Spend Alerts for the 43 customers behind 52% of stress months, each measured against a random holdout within 90 days."],
    ["Honest limits", "Synthetic data (two source years folded onto 2025, engagement skewed high), 91 customers seen only once, segments on a continuum. Sizes are directional; conclusions rest on ratios."],
  ];
  let y = 3.25;
  pts.forEach((r) => {
    s.addText(r[0], { x: 0.9, y, w: 2.7, h: 0.8, isTextBox: true, margin: 0, valign: "top",
      fontFace: BFONT, fontSize: 14, bold: true, color: MINT });
    s.addText(r[1], { x: 3.7, y, w: 8.9, h: 0.8, isTextBox: true, margin: 0, valign: "top",
      fontFace: BFONT, fontSize: 13, color: "DCEAEC" });
    y += 0.86;
  });
  s.addText("One guarantee: wellbeing help, never a credit decision.", {
    x: 0.9, y: 6.8, w: 11.6, h: 0.4, isTextBox: true, margin: 0, fontFace: BFONT, fontSize: 13, italic: true, bold: true, color: MINT });
  s.addNotes("If a judge remembers three things: overspending, not income; timing, not a blacklist; help offered, never credit taken away.");
})();

p.writeFile({ fileName: OUT }).then((f) => console.log("WROTE", f)).catch((e) => { console.error(e); process.exit(1); });
