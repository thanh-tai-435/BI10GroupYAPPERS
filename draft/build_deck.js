// BI10 R01 — Group YAPPERS deck generator. Run: node draft/build_deck.js
const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

const FIG = path.resolve(__dirname, "..", "outputs", "figures");
const img = (n) => path.join(FIG, n);
const OUT = path.resolve(__dirname, "YAPPERS_BI10_R01.pptx");

// ---- palette (teal-trust / navy wellbeing) ----
const DARK = "0F2A43";   // deep navy  (title/closing bg)
const NAVY = "12435E";   // primary
const TEAL = "058B8C";   // secondary
const MINT = "1FC3A6";   // accent
const INK = "1B2A36";    // body text on light
const MUTE = "5F7180";   // muted
const ICE = "EAF3F4";    // light tint
const WHITE = "FFFFFF";

const HFONT = "Cambria";
const BFONT = "Calibri";

const p = new pptxgen();
p.layout = "LAYOUT_WIDE";           // 13.33 x 7.5
const W = 13.33, H = 7.5;
p.defineSlideMaster({ title: "L", background: { color: WHITE } });

// ---------- helpers ----------
function bulletList(items, fs = 14) {
  return items.map((t, i) => ({
    text: t,
    options: { bullet: { code: "2022", indent: 14 }, breakLine: true,
               paraSpaceAfter: 7, color: INK, fontFace: BFONT, fontSize: fs },
  }));
}
function tag(slide, txt) {                     // mint section pill
  slide.addText(txt.toUpperCase(), {
    x: 0.5, y: 0.42, w: 4.5, h: 0.32, isTextBox: true, margin: 0,
    fontFace: BFONT, fontSize: 11, bold: true, color: TEAL, charSpacing: 2 });
}
function heading(slide, txt) {
  slide.addText(txt, { x: 0.5, y: 0.72, w: 12.3, h: 0.95, isTextBox: true, margin: 0,
    fontFace: HFONT, fontSize: 27, bold: true, color: NAVY, valign: "top", lineSpacingMultiple: 0.95 });
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
function caveat(slide, txt, y) {
  slide.addText("⚠  " + txt, { x: 0.5, y, w: 6.3, h: 0.7, isTextBox: true, margin: 0,
    fontFace: BFONT, fontSize: 10.5, italic: true, color: MUTE, valign: "top" });
}

// ============ SLIDE 1 — TITLE ============
(() => {
  const s = p.addSlide();
  s.background = { color: DARK };
  s.addShape(p.ShapeType.rect, { x: 0, y: 0, w: 0.22, h: H, fill: { color: MINT } });
  s.addText("ITB CONSUMER WELLBEING & SEGMENTATION", {
    x: 0.9, y: 2.0, w: 11.5, h: 1.3, isTextBox: true, margin: 0,
    fontFace: HFONT, fontSize: 40, bold: true, color: WHITE, lineSpacingMultiple: 1.0 });
  s.addText("A non-punitive plan built on spending behaviour, not credit risk", {
    x: 0.9, y: 3.35, w: 11, h: 0.6, isTextBox: true, margin: 0,
    fontFace: BFONT, fontSize: 18, italic: true, color: MINT });
  s.addText([
    { text: "999 consumers · 1.85M transactions — and one finding that reframes everything.", options: { color: "CFE3E6", fontSize: 14, breakLine: true, paraSpaceAfter: 10 } },
    { text: "Group YAPPERS  ·  BI10 Round 01  ·  September 2026", options: { color: "9FB6BD", fontSize: 13 } },
  ], { x: 0.9, y: 4.4, w: 11, h: 1.2, isTextBox: true, margin: 0, fontFace: BFONT });
  s.addNotes("Set the wellbeing frame from second one — customer understanding, never credit scoring.");
})();

// ============ SLIDE 2 — EXECUTIVE SUMMARY ============
(() => {
  const s = p.addSlide();
  s.background = { color: DARK };
  s.addText("EXECUTIVE SUMMARY", { x: 0.6, y: 0.5, w: 8, h: 0.4, isTextBox: true, margin: 0,
    fontFace: BFONT, fontSize: 12, bold: true, color: MINT, charSpacing: 3 });
  s.addText("One inversion drives the whole story", { x: 0.6, y: 0.9, w: 12, h: 0.8, isTextBox: true,
    margin: 0, fontFace: HFONT, fontSize: 30, bold: true, color: WHITE });
  const rows = [
    ["Overspend, not low income", "spend-to-income (r −0.90) and credit-utilization (r −0.86) explain almost all of financial health."],
    ["The budget inverts under stress", "stressed customers spend 71.6% discretionary vs healthy customers' 40.5% — the strongest signal in the data."],
    ["Stress is episodic & hits the engaged", "0 of 999 chronically stressed; the crossover = 43 consumers = 52% of ALL stress episodes; 72% of Healthy→Stretched slides happen Nov→Dec."],
    ["Four stable segments", "k-means (k=4), 999/999 covered — sizes 351 / 302 / 258 / 88; stable across seeds (ARI 0.99)."],
    ["A 6-tool wellbeing plan", "lead with Budgeting (302) + Spend Alerts (43, Sun–Mon evenings); a 10% spend trim cuts stress months ~32%. FHS never denies, cuts, or blocks credit."],
  ];
  let y = 2.0;
  rows.forEach((r) => {
    s.addText(r[0], { x: 0.6, y, w: 4.1, h: 0.9, isTextBox: true, margin: 0, valign: "top",
      fontFace: BFONT, fontSize: 15, bold: true, color: MINT });
    s.addText(r[1], { x: 4.9, y, w: 7.8, h: 0.9, isTextBox: true, margin: 0, valign: "top",
      fontFace: BFONT, fontSize: 13.5, color: "DCEAEC" });
    y += 1.02;
  });
  s.addNotes("If a judge reads only this slide, they get the whole story.");
})();

// ============ SLIDE 3 — TABLE OF CONTENTS ============
(() => {
  const s = p.addSlide();
  s.background = { color: WHITE };
  tag(s, "Contents"); heading(s, "What this deck covers");
  const items = [
    ["01", "Introduction to the Case"],
    ["02", "Task 1 — Exploratory Data Analysis"],
    ["03", "Task 2 — Financial Health Analysis"],
    ["04", "Task 3 — Customer Engagement Analysis"],
    ["05", "Task 4 — Customer Segmentation"],
    ["06", "Task 5 — Recommendations & Impact"],
  ];
  items.forEach((it, i) => {
    const col = Math.floor(i / 3), row = i % 3;
    const x = 0.7 + col * 6.3, y = 2.1 + row * 1.5;
    s.addShape(p.ShapeType.roundRect, { x, y, w: 0.85, h: 0.85, rectRadius: 0.42,
      fill: { color: ICE }, line: { color: MINT, width: 1.5 } });
    s.addText(it[0], { x, y, w: 0.85, h: 0.85, isTextBox: true, margin: 0, align: "center",
      valign: "middle", fontFace: HFONT, fontSize: 22, bold: true, color: TEAL });
    s.addText(it[1], { x: x + 1.05, y, w: 4.9, h: 0.85, isTextBox: true, margin: 0, valign: "middle",
      fontFace: BFONT, fontSize: 15, bold: true, color: INK });
  });
  footer(s, 3);
  s.addNotes("Show the arc — EDA and segmentation carry the most weight.");
})();

// ============ SLIDE 4 — INTRODUCTION + DATA QUALITY ============
(() => {
  const s = p.addSlide();
  s.background = { color: WHITE };
  tag(s, "Introduction"); heading(s, "The case: understand wellbeing, not score credit");
  s.addText(bulletList([
    "ITB, a Vietnamese consumer-finance company, wants to understand customer wellbeing, spending and engagement — customer understanding & segmentation, NOT credit-risk decisions.",
    "We read ratios and shares, never absolute VND: synthetic income / credit / balance magnitudes are inflated.",
    "Distress analysed at consumer-MONTH grain (it is episodic); \"what kind of customer\" at consumer level.",
    "Process: data-quality checks → EDA → financial health → engagement → segmentation → recommendations. Every number reproduces in notebooks/full_pipeline.ipynb.",
  ], 13), { x: 0.5, y: 1.7, w: 6.3, h: 3.4, isTextBox: true, valign: "top" });
  s.addShape(p.ShapeType.roundRect, { x: 0.5, y: 5.3, w: 6.3, h: 1.2, rectRadius: 0.08, fill: { color: NAVY } });
  s.addText([
    { text: "Ethical rule  ", options: { bold: true, color: MINT, fontSize: 13 } },
    { text: "financial_health_score is a wellbeing measure — never used to deny credit, cut a limit, raise a rate, or block an account.", options: { color: WHITE, fontSize: 12.5 } },
  ], { x: 0.7, y: 5.38, w: 5.9, h: 1.05, isTextBox: true, margin: 0, valign: "middle", fontFace: BFONT });

  const stats = [["999", "consumers"], ["1.85M", "transactions"], ["693", "merchants"], ["34", "provinces"]];
  stats.forEach((st, i) => {
    const x = 7.05 + i * 1.47;
    s.addShape(p.ShapeType.roundRect, { x, y: 1.7, w: 1.35, h: 1.05, rectRadius: 0.08, fill: { color: ICE } });
    s.addText(st[0], { x, y: 1.76, w: 1.35, h: 0.55, isTextBox: true, margin: 0, align: "center",
      fontFace: HFONT, fontSize: 20, bold: true, color: NAVY });
    s.addText(st[1], { x, y: 2.3, w: 1.35, h: 0.35, isTextBox: true, margin: 0, align: "center",
      fontFace: BFONT, fontSize: 10.5, color: MUTE });
  });
  s.addShape(p.ShapeType.roundRect, { x: 7.05, y: 2.95, w: 5.8, h: 3.55, rectRadius: 0.06,
    fill: { color: WHITE }, line: { color: MINT, width: 1.2 } });
  const dq = [
    "0 missing cells · 0 duplicate transaction IDs · 0 duplicate consumer-months",
    "0 negative amounts · every timestamp inside 2025",
    "1 name + birth date per consumer; 1 name per merchant",
    "Transactions reconcile 100% to monthly total_spend (10,992 / 10,992)",
    "10,992 of 11,988 possible consumer-months present (1–12 each)",
    "5 over-limit months (utilization 1.03–1.5, all FHS < 35) kept as real behaviour",
    "Caveat (case §12): two source years folded onto 2025 → volumes inflated; ratios are the signal",
  ];
  s.addText([{ text: "Data-quality checks — both files", options: { bold: true, color: TEAL, fontSize: 13, breakLine: true, paraSpaceAfter: 6 } },
    ...dq.map((t, i) => ({ text: (i < 6 ? "✓  " : "⚠  ") + t, options: { color: INK, fontSize: 11, breakLine: i < dq.length - 1, paraSpaceAfter: 5 } }))],
    { x: 7.25, y: 3.05, w: 5.45, h: 3.4, isTextBox: true, margin: 0, valign: "top", fontFace: BFONT });
  footer(s, 4);
  s.addNotes("Two rules govern the deck: ratios over magnitudes, wellbeing over credit. Data quality is clean except the documented synthetic caveats.");
})();

// ---------- generic content slides ----------
const SM = "Source: consumer_financial_health_engagement_2025 — 10,992 consumer-months, 999 consumers, 2025.";
const ST = "Source: consumer_transactions_2025 — 1,852,394 transactions, 2025.";
const SMT = "Source: transactions file joined to the consumer-month file on consumer_id + month.";
const SK = "Source: team k-means (k=4) on 8 z-scaled ratios, 999 consumers (task4_features.csv).";
function cap(s, txt, x, y, w) {
  s.addText(txt, { x, y, w, h: 0.28, isTextBox: true, margin: 0, fontFace: BFONT, fontSize: 8.5, italic: true, color: MUTE, valign: "top" });
}
function statBox(s, st, y = 5.55) {
  s.addShape(p.ShapeType.roundRect, { x: 0.5, y, w: 3.7, h: 1.15, rectRadius: 0.08, fill: { color: NAVY } });
  s.addText(st[0], { x: 0.5, y: y + 0.08, w: 3.7, h: 0.68, isTextBox: true, margin: 0, align: "center",
    fontFace: HFONT, fontSize: 26, bold: true, color: MINT });
  s.addText(st[1], { x: 0.5, y: y + 0.76, w: 3.7, h: 0.33, isTextBox: true, margin: 0, align: "center",
    fontFace: BFONT, fontSize: 11, color: WHITE });
}
// one chart right, bullets left
function contentOne(n, sec, title, bullets, chartName, opts = {}) {
  const s = p.addSlide();
  s.background = { color: WHITE };
  tag(s, sec); heading(s, title);
  s.addText(bulletList(bullets, opts.fs || 13), { x: 0.5, y: 1.7, w: 6.3, h: opts.stat ? 3.75 : 5.0, isTextBox: true, valign: "top" });
  chart(s, chartName, 7.05, 1.7, 5.8, 4.4);
  cap(s, opts.src || SM, 7.05, 6.15, 5.8);
  if (opts.cav)
    s.addText("⚠  " + opts.cav, { x: 7.05, y: 6.45, w: 5.8, h: 0.55, isTextBox: true, margin: 0,
      fontFace: BFONT, fontSize: 9.5, italic: true, color: MUTE, valign: "top" });
  if (opts.stat) statBox(s, opts.stat);
  footer(s, n);
  if (opts.note) s.addNotes(opts.note);
}
// bullets top band, two charts below
function contentTwo(n, sec, title, bullets, c1, c2, opts = {}) {
  const s = p.addSlide();
  s.background = { color: WHITE };
  tag(s, sec); heading(s, title);
  s.addText(bulletList(bullets, opts.fs || 12.5), { x: 0.5, y: 1.55, w: 12.3, h: 1.75, isTextBox: true, valign: "top" });
  chart(s, c1, 0.55, 3.3, 5.95, 3.35);
  chart(s, c2, 6.85, 3.3, 5.95, 3.35);
  cap(s, opts.src || SM, 0.55, 6.72, 12.25);
  footer(s, n);
  if (opts.note) s.addNotes(opts.note);
}
// bullets top band, three charts below
function contentThree(n, sec, title, bullets, cs, opts = {}) {
  const s = p.addSlide();
  s.background = { color: WHITE };
  tag(s, sec); heading(s, title);
  s.addText(bulletList(bullets, opts.fs || 12.5), { x: 0.5, y: 1.55, w: 12.3, h: 1.65, isTextBox: true, valign: "top" });
  const ws = opts.widths || [4.0, 4.0, 4.0]; let x = 0.5;
  cs.forEach((c, i) => { chart(s, c, x, 3.25, ws[i], 3.4); x += ws[i] + 0.15; });
  cap(s, opts.src || SM, 0.5, 6.72, 12.3);
  footer(s, n);
  if (opts.note) s.addNotes(opts.note);
}
// bullets top band, one full-width chart
function contentWide(n, sec, title, bullets, chartName, opts = {}) {
  const s = p.addSlide();
  s.background = { color: WHITE };
  tag(s, sec); heading(s, title);
  s.addText(bulletList(bullets, opts.fs || 12.5), { x: 0.5, y: 1.55, w: 12.3, h: 1.6, isTextBox: true, valign: "top" });
  chart(s, chartName, 0.5, 3.2, 12.3, 3.45);
  cap(s, opts.src || SM, 0.5, 6.72, 12.3);
  footer(s, n);
  if (opts.note) s.addNotes(opts.note);
}

// ============ SLIDES 5–21 (auto-numbered) ============
let N = 4;
contentOne(++N, "Task 1 · EDA · Q1", "December is the spending engine — and it runs on frequency",
  ["Peak: December = 488.0B VND = 15.04% of the 3.24T annual spend. Trough: February = 174.4B VND = 5.37% → December is 2.8× February.",
   "Decomposition: transaction count +187% peak vs trough, while the average ticket falls 2.6% (1.74M vs 1.79M VND).",
   "The uplift is uniform — all 14 categories grow +181% to +193%; no single category drives it.",
   "Behaviour: customers buy more often, not pricier (year-end / Tết preparation) → scale capacity, fraud monitoring and campaigns to volume, not basket size."],
  "t1_monthly_spend.png",
  { src: ST, cav: "Case note §12: two source years folded onto 2025 inflate monthly volume — treat 15% as directional.",
    note: "Peaks are a frequency phenomenon across every category — the lever is trip frequency, not upsell." });

contentTwo(++N, "Task 1 · EDA · Q2 — the spine", "Financial stress flips the budget: essential → discretionary",
  ["Stressed months (FHS < 40; 95 consumer-months, 70 consumers): 28.4% essential / 71.6% discretionary. Healthy months (FHS ≥ 80; 475 months, 303 consumers): 59.5% / 40.5%.",
   "A gradient, not a threshold artefact: discretionary share 71.6% → 64.2% → 57.3% → 54.4% → 49.2% → 40.6% across FHS bands; every cutoff pair keeps the direction (FHS < 35 vs ≥ 85: 73.5% vs 30.2%).",
   "Stress re-allocates the budget toward wants, not needs → the non-punitive lever is discretionary-spend visibility, not credit restriction. This anchors Tasks 4–5."],
  "t1_essential_discretionary.png", "t1_discretionary_gradient.png",
  { note: "THE slide — the gradient proves the inversion is real, not an artefact of the 40/80 cutoffs." });

contentTwo(++N, "Task 1 · EDA · Q4 & Q5", "Categories: habit vs basket. Age: active 25–34 is weakest — barely",
  ["Q4 — top by COUNT: Fuel & Transport, 188,029 transactions, avg ticket 1.59M VND (bought by 96.8% of consumers, 17.3 times per buyer-month). Top by SPEND: in-store Groceries, 513.8B VND, avg ticket 2.92M VND (1.8×) — frequent top-ups vs stock-up baskets.",
   "Q5 — 25–34 is active (178.7 transactions/month, above the cohort median 177.8) with the lowest FHS 65.8 (best 67.0). Drivers: highest spend-to-income 0.716 (national 0.700) with a below-average essential ratio 0.468 (national 0.481) → overspend on wants.",
   "But bootstrap 95% CIs of all six cohorts overlap (65.8–67.0): age is a weak differentiator — target the ratios, not birth year."],
  "t1_category_ticket.png", "t1_age_cohort.png",
  { src: ST + " Age cohorts: consumer-month file.", note: "Answer Q4 and Q5 exactly as asked, then show the honest limit (CI overlap)." });

contentOne(++N, "Task 1 · EDA · Q3", "No regional digital divide: high-spend provinces mirror the nation",
  ["5 provinces with above-median spend but below-average digital share: Ha Noi, Dong Nai, Lam Dong, Hung Yen, Hai Phong.",
   "Channel breakdown (share of transactions): POS 58.9–59.3% vs 58.8% nationally · QR ~19.8–20.1% · E-commerce ~8.5% · Mobile ~7.5% · Recurring ~5%.",
   "Largest digital gap: −0.46pp (Dong Nai); digital share of value 40.9–41.5% vs 41.5% nationally.",
   "The gap is statistically real but commercially negligible → province is not a lever for digital adoption; behaviour is."],
  "t1_province_channel.png",
  { src: ST, stat: ["≤ 0.46pp", "largest digital-share gap vs national"],
    note: "Q3 asked for the channel breakdown — every hub has the national mix." });

contentOne(++N, "Task 2 · Financial Health · D1", "Health is a tight band; distress is episodic, never chronic",
  ["Consumer level (n = 999): mean 66.3, median 66.2, std 4.7, IQR 63.4–69.3, range 42.3–80.8, skew −0.32 (mild low tail).",
   "Month level (n = 10,992): std 9.5 — twice the consumer spread. Segments: Stable 72.5% · Watch 22.4% · Healthy 4.3% · Stressed 0.9%.",
   "0 of 999 consumers have a 12-month mean below 40 — stress is episodic: healthy people dip in specific months (Feb 73.6 → Dec 54.2).",
   "Implication: trigger help on the current month, not on a static risk list."],
  "t2_fhs_distribution.png",
  { note: "Nobody is chronically unhealthy — trigger on the month, not the person." });

contentTwo(++N, "Task 2 · Financial Health · D2", "Low health is an overspend story",
  ["Top correlates with FHS (month grain, n = 10,992): spend-to-income −0.90, credit-utilization −0.86, volatility −0.50. Stressed vs healthy months: spend/income 2.10 vs 0.29; utilization 0.58 vs 0.08.",
   "Step by step: mean FHS 72.4 → 68.4 → 66.0 → 63.8 → 60.9 across spend-to-income quintiles (−11.4 pts, ~10× the age spread).",
   "Counter-intuitive: stressed months are MORE engaged (81.1 vs 72.7). FHS and ratios share spend fields — directional, not causal."],
  "t2_low_health_drivers.png", "t2_sti_quintile.png",
  { note: "Two ratios are the whole game — the quintile chart makes r = −0.90 tangible." });

contentTwo(++N, "Task 2 · Financial Health · D4", "The \"Stressed but Engaged\" crossover — and when to reach it",
  ["Reproducible rule (consumer-month): financial_health_score < 40 AND engagement_score ≥ p75 (81.4) → 43 consumers / 49 months = 52% of ALL stress episodes. Robust: p70 / p80 give 44 / 41 consumers (53% / 48%).",
   "Profile: spend/income 1.89, credit-utilization 0.55, online share 0.49 (2× national) — active, digital, over-extended.",
   "Timing (transactions): stressed months put 23.5% of spend value into 22–23h vs 8.3% (bigger late tickets, not more: count 11.6% vs 9.7%); Sunday + Monday = 42% vs 34% → alerts Sun–Mon evenings, before 22:00."],
  "t2_crossover.png", "t2_timing.png",
  { src: SM + " Timing: " + SMT, note: "More than half of every stress episode happens to someone we can reach in-app — and we know when." });

contentWide(++N, "Task 2 · Financial Health · D3", "Who differs? Province and age barely; occupation through spending",
  ["Province: 22 of 27 provinces (≥ 15 consumers) have a 95% CI containing the national mean 66.3 (extremes Thai Nguyen 63.0, HCMC 67.6). Age: all six cohort CIs overlap (65.8–67.0).",
   "Occupation (396 raw titles → 8 keyword groups): Engineering/science/IT 69.1 (n = 229), Business/finance 68.7 (126) vs Office/public 64.5 (443), Manual/trades 62.9 (23) — a ~6-pt spread that mirrors spend-to-income (0.60 vs 0.76–0.79).",
   "Demographics act through the overspend ratio → target the ratio, never the group (fairness)."],
  "t2_demographics.png",
  { note: "Deliverable 3 — the one demographic gap is really a spending gap." });

contentThree(++N, "Task 3 · Engagement · D1–D2", "Engagement is saturated; channels are POS-first",
  ["D1: engagement_score mean 77.8, median 78.1, IQR 74.8–81.4 (consumer-month). Consumers by segment: Low 1.0% (10) · Medium 8.0% (80) · High 74.1% (740) · Very high 16.9% (169) → the score alone does not segment the base.",
   "D2: POS 58.8% · QR 19.8% · E-commerce 8.7% · Mobile App 7.7% · Recurring 4.9% of 1.85M transactions; non-POS = 41% of trips and 41.5% of value. Average online spend share 24.7% per consumer (range 0–95%)."],
  ["t3_engagement_dist.png", "t3_segment_share.png", "t3_channel_mix.png"],
  { src: SM + " Channels: " + ST, widths: [4.75, 3.35, 3.9], note: "Histogram for a continuous score, bar for ordered segments (a pie would hide the 1% tail), bar for nominal channels." });

contentTwo(++N, "Task 3 · Engagement · D3–D4", "What actually discriminates: diversity & consistency",
  ["D3 — category diversity ranges 2–14 (consumer mean 12.9; 908 of 999 at 13–14). r = +0.94 with engagement; still +0.81 without the dormant tail (Spearman +0.85) — not a tail artefact.",
   "D4 — recency 0–30 days (median 0); active days 1–31 (median 30); transactions 2–713 per month (median 150). Links to engagement: active days r +0.59 > recency −0.42 > count +0.40.",
   "Heatmap: 30–31 active days & recency 0 → engagement 79.8 (n = 6,614); every 1–5-active-day cell stays ≤ 55 → consistency beats recency and volume."],
  "t3_diversity_vs_engagement.png", "t3_recency_frequency.png",
  { note: "Scatter for two continuous variables; heatmap for the recency × frequency interaction." });

contentOne(++N, "Task 3 · Engagement · D5", "High-health, low-engagement: 25 good customers drifting away",
  ["Cutoff: FHS ≥ 70 (≈ p79, top 21% of consumers) AND engagement < 70 (below p10 = 71.1) → 25 consumers (2.5%).",
   "Why not stricter / looser: the count stays 25 at engagement < 60, 65, 68, 70 (a natural gap), then jumps to 36 (< 72), 52 (< 74), 63 (< 75) as it reaches the main body. FHS ≥ 65 gives 48; ≥ 75 gives 9.",
   "Profile vs rest: FHS 74.0 vs 66.1 · engagement 46.8 vs 76.1 · 9.9 vs 159 transactions/month · 2.0 vs 27.0 active days · recency 14.3 vs 0.9 days · diversity 4.7 vs 13.1 · online 0.61 vs 0.24.",
   "24 of 25 sit in Emerging Digital → play = reactivation of everyday use, not budgeting."],
  "t3_health_vs_engagement_quadrant.png",
  { fs: 12, cav: "n = 25, synthetic-inflated engagement — a cohort to watch, not a sized forecast.",
    note: "The sensitivity numbers answer 'why this cutoff and not a stricter or looser one'." });

contentOne(++N, "Task 4 · Segmentation · Method", "Preprocessing, features and model choice",
  ["Preprocessing: 10,992 consumer-months → 999 consumers (yearly mean of each ratio = typical monthly profile); 0 nulls after aggregation; raw VND excluded. The preprocessed dataset (task4_features.csv) and its data dictionary are in the submission ZIP.",
   "8 features, z-scaled: health (FHS, spend-to-income, credit-utilization, volatility) · engagement (engagement score, transaction count) · spending (discretionary, online ratio).",
   "Excluded with reason: essential ratio (= 1 − discretionary), diversity / active days / recency (p75 = max, near-constant); demographics kept for profiling only.",
   "k-means over a pure 2×2: boundaries form across all 8 dimensions. k = 4 via elbow + best silhouette in the 4–6 range (0.251; k = 2 wins at 0.557 but collapses the personas). Coverage 999 / 999, 7 minors kept."],
  "t4_silhouette.png",
  { fs: 12, src: SK, note: "Preprocessed dataset + data dictionary are in the ZIP (task4_features.csv, data_dictionary_task4.md)." });

contentTwo(++N, "Task 4 · Segmentation · Profiles", "Four segments, side by side",
  ["Healthy & Highly Engaged — 351 (35.1%): FHS 70.5, lowest spend/income 0.571 & utilization 0.148 → retain & grow value.  ·  Stretched but Highly Engaged — 302 (30.2%): FHS 62.6, highest spend/income 0.835 & utilization 0.248, still engaged 76.5 → wellbeing priority.",
   "Digital Power Users — 258 (25.8%): 251 transactions/month (1.6× avg), highest volatility 1.91 & engagement 80.2 → monetise, monitor drift.  ·  Low Engagement & Emerging Digital — 88 (8.8%): 9.7 transactions/month, engagement 49.6, but 67.1% online & 86.6% discretionary → activate.",
   "Suggested personas not formed: Essential-Spend-Focused = only 4 consumers; Healthy-but-Disengaged = 25, 24 of them inside Emerging Digital."],
  "t4_segment_sizes.png", "t4_segment_profiles.png",
  { src: SK, note: "The heatmap is the side-by-side comparison the brief asks for." });

(() => {   // validation + limitations & future work
  const s = p.addSlide();
  s.background = { color: WHITE };
  const n = ++N;
  tag(s, "Task 4 · Segmentation · Validation & limits"); heading(s, "Stable segments, a December slide — and honest limits");
  s.addText(bulletList([
    "Stability: 20 random seeds → ARI 0.988; 80% bootstrap × 50 → ARI 0.911. Alternative GMM: ARI 0.26 — Emerging Digital identical, the three large segments form one continuum (hence silhouette 0.251).",
    "Rule-based cross-check (2×2 median split of health × engagement): 344 of 351 Healthy and 273 of 302 Stretched customers fall in the matching halves.",
    "Monthly migration: a Healthy month is followed by a Stretched month 23% of the time — 72% from November to December.",
    "Bias check: segments correlate with age & gender (chi-square p < 0.01) though not inputs → trigger every tool on behaviour, never on demographics.",
  ], 12), { x: 0.5, y: 1.6, w: 6.4, h: 2.85, isTextBox: true, valign: "top" });
  chart(s, "t4_pca.png", 7.05, 1.6, 5.8, 2.95);
  cap(s, SK + " PCA = 73% of variance.", 7.05, 4.55, 5.8);
  const box = (x, title, lines) => {
    s.addShape(p.ShapeType.roundRect, { x, y: 4.9, w: 6.05, h: 2.05, rectRadius: 0.06, fill: { color: ICE } });
    s.addText([{ text: title, options: { bold: true, color: TEAL, fontSize: 12.5, breakLine: true, paraSpaceAfter: 4 } },
      ...lines.map((t, i) => ({ text: "•  " + t, options: { color: INK, fontSize: 10.5, breakLine: i < lines.length - 1, paraSpaceAfter: 3 } }))],
      { x: x + 0.18, y: 4.98, w: 5.7, h: 1.9, isTextBox: true, margin: 0, valign: "top", fontFace: BFONT });
  };
  box(0.5, "Limitations", [
    "Technical: moderate silhouette; yearly means hide within-year trajectory; feature choice is a judgement call.",
    "Data: synthetic, two source years folded onto 2025; engagement engineered high; Emerging Digital (n = 88) least robust.",
    "Operational: segments are wellbeing groups, not risk tiers — never for lending.",
  ]);
  box(6.8, "Future work", [
    "Refit on multi-year real data; track segment migration monthly.",
    "Trajectory features (FHS slope, volatility trend) + GMM soft membership for boundary customers.",
    "Chronological model for next_month_low_health_flag (train Jan–Aug, test Nov) as an early-warning — support only.",
  ]);
  s.addNotes("Stable enough to act on; the Nov→Dec slide is the timing evidence for planning reminders.");
  footer(s, n);
})();

(() => {   // six tools as a table
  const s = p.addSlide();
  s.background = { color: WHITE };
  const n = ++N;
  tag(s, "Task 5 · Recommendations"); heading(s, "Six non-punitive tools, each tied to a data finding");
  const H = (t) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: NAVY }, fontSize: 11 } });
  const rows = [[H("Tool"), H("Target group (n, % of 999)"), H("Data evidence"), H("Action"), H("KPI")],
    ["① Budgeting tool", "Stretched & Engaged: 302 (30.2%)", "spend_to_income r −0.90; segment spend/income 0.835", "In-app spend-vs-income dashboard, discretionary category view", "spend/income; % months FHS < 40"],
    ["② Spend alerts", "Crossover: 43 (4.3%) = 52% of stress months", "FHS < 40 & engagement ≥ p75; 23.5% of spend at 22–23h", "Pacing alert Sun–Mon evenings, before 22:00", "stress months / consumer"],
    ["③ Planning reminders", "Power Users 258 (25.8%) + Healthy 351 (35.1%)", "Healthy → Stretched 72% Nov → Dec; volatility r −0.50", "November year-end budget plan & reminder", "Nov → Dec slide rate"],
    ["④ Financial education", "Distress tail: 67 (6.7%)", "discretionary 72% vs 40% under stress", "Needs-vs-wants micro-modules", "essential share next month"],
    ["⑤ Digital nudges", "Emerging Digital: 88 (8.8%)", "diversity r +0.94; 60.5% of spend via E-com + Mobile", "Onboarding & habit loops in the app they already use", "active days; categories / month"],
    ["⑥ Product suggestions", "Healthy & Engaged: 351 (35.1%)", "lowest utilization 0.148, FHS 70.5", "Opt-in savings / loyalty; never auto-extend credit", "opt-in uptake; FHS stable"]];
  s.addTable(rows, { x: 0.5, y: 1.65, w: 12.3, colW: [1.85, 2.55, 3.2, 3.0, 1.7], fontFace: BFONT, fontSize: 10.5, color: INK,
    border: { type: "solid", pt: 0.5, color: "C9D6DB" }, fill: { color: WHITE }, valign: "middle", rowH: 0.62 });
  cap(s, SK + " Crossover & distress tail: consumer-month file; channel share: transactions file.", 0.5, 6.15, 12.3);
  s.addText("No double-counting: the 4 segments partition all 999 consumers; the crossover (43) and distress tail (67) are overlays inside the Stretched segment.", {
    x: 0.5, y: 6.45, w: 12.3, h: 0.5, isTextBox: true, margin: 0, fontFace: BFONT, fontSize: 11, italic: true, color: TEAL });
  s.addNotes("One tool per required type, each with exact size, %, the column it rests on, and a KPI.");
  footer(s, n);
})();

contentOne(++N, "Task 5 · Recommendations", "Prioritization — and the credit-decision rule",
  ["Ranking by reach × driver strength: ① Budgeting (302, |r| 0.90) → ② Alerts (43, 52% of stress) → ③ Reminders (258) → ⑥ Products (351) → ⑤ Nudges (88) → ④ Education (67).",
   "Lead with Budgeting + Alerts (the wellbeing mission); layer growth tools on top.",
   "Fair by design: every trigger is a behavioural ratio; segments correlate with age / gender, so we never target by demographics.",
   "RULE: financial_health_score is never used to deny credit, cut a credit limit, raise a rate or block an account — a low score only triggers help that is offered."],
  "t5_priority_ranking.png",
  { src: SK, stat: ["NEVER", "FHS → credit decision"],
    note: "The rule is the deck's contract — a low score triggers help offered, never access removed." });

contentOne(++N, "Task 5 · Impact", "Expected impact, measurement & a 90-day roadmap",
  ["Scenario (illustrative): FHS = 84.1 − 25.3 × spend-to-income (r −0.90). A 5% trim for the Stretched 302 → stress months 95 → 80 (−16%); 10% → 65 (−32%); 15% → 49.",
   "Measurement: every tool gets one KPI and a randomised holdout (e.g. Budgeting: 10% holdout for 3 months).",
   "Days 0–30: Budgeting + Alerts · 31–60: November Reminders + Digital Nudges · 61–90: Education + opt-in Products; keep what moves the KPI."],
  "t5_impact_scenario.png",
  { src: "Source: team scenario on the consumer-month file (10,992 months).", stat: ["−32%", "stress months at a 10% trim"],
    cav: "FHS embeds spend fields — the slope is mechanical; a scenario to test, not a forecast.",
    note: "Impact is a hypothesis we will measure, not a promise." });

// ============ CLOSING ============
(() => {
  const s = p.addSlide();
  s.background = { color: DARK };
  s.addShape(p.ShapeType.rect, { x: 0, y: 0, w: 0.22, h: H, fill: { color: MINT } });
  s.addText("The contract", { x: 0.9, y: 0.9, w: 8, h: 0.4, isTextBox: true, margin: 0,
    fontFace: BFONT, fontSize: 12, bold: true, color: MINT, charSpacing: 3 });
  s.addText("Grow the healthy, activate the dormant, protect the stretched —\nwithout ever touching their credit.", {
    x: 0.9, y: 1.35, w: 11.6, h: 1.7, isTextBox: true, margin: 0,
    fontFace: HFONT, fontSize: 28, bold: true, color: WHITE, lineSpacingMultiple: 1.05 });
  const pts = [
    ["The spine", "Overspend drives poor health; the budget inverts under stress; stress is episodic, striking the most engaged."],
    ["The payoff", "4 clean segments (351/302/258/88) and a 6-tool plan reaching every customer with the right non-punitive touch."],
    ["Lead action", "Budgeting for 302 + real-time Alerts catching 52% of all stress — highest reach × strongest driver, near-zero cost."],
    ["Honest limits", "Synthetic data with two source years folded onto 2025, engineered engagement, segments on a continuum — sizes directional, conclusions robust on ratios."],
  ];
  let y = 3.35;
  pts.forEach((r) => {
    s.addText(r[0], { x: 0.9, y, w: 2.7, h: 0.8, isTextBox: true, margin: 0, valign: "top",
      fontFace: BFONT, fontSize: 14, bold: true, color: MINT });
    s.addText(r[1], { x: 3.7, y, w: 8.8, h: 0.8, isTextBox: true, margin: 0, valign: "top",
      fontFace: BFONT, fontSize: 13, color: "DCEAEC" });
    y += 0.86;
  });
  s.addText("One guarantee: wellbeing help, never a credit decision.", {
    x: 0.9, y: 6.85, w: 11.6, h: 0.4, isTextBox: true, margin: 0,
    fontFace: BFONT, fontSize: 13, italic: true, bold: true, color: MINT });
  s.addNotes("Close on the contract.");
})();

p.writeFile({ fileName: OUT }).then((f) => console.log("WROTE", f)).catch((e) => { console.error(e); process.exit(1); });
