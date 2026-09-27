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
function bulletList(items) {
  return items.map((t, i) => ({
    text: t,
    options: { bullet: { code: "2022", indent: 14 }, breakLine: true,
               paraSpaceAfter: 8, color: INK, fontFace: BFONT, fontSize: 14 },
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

// ============ SLIDE 4 — INTRODUCTION ============
(() => {
  const s = p.addSlide();
  s.background = { color: WHITE };
  tag(s, "Introduction"); heading(s, "The case: understand wellbeing, not score credit");
  s.addText(bulletList([
    "ITB, a Vietnamese consumer-finance company, wants to understand customer wellbeing, spending and engagement.",
    "This is customer understanding & segmentation — NOT credit-risk decision-making.",
    "We read ratios and shares, never absolute VND: synthetic income/credit/balance magnitudes are inflated.",
    "Distress analysed at consumer-MONTH grain (episodic); \"what kind of customer\" at consumer level.",
  ]), { x: 0.5, y: 1.75, w: 6.4, h: 4.6, isTextBox: true, valign: "top" });

  // dataset stat cards (right)
  const stats = [["999", "consumers"], ["1.85M", "transactions"], ["2025", "full year, VND"], ["Synthetic", "ratios are the signal"]];
  stats.forEach((st, i) => {
    const x = 7.3 + (i % 2) * 2.9, y = 1.8 + Math.floor(i / 2) * 1.55;
    s.addShape(p.ShapeType.roundRect, { x, y, w: 2.7, h: 1.35, rectRadius: 0.08, fill: { color: ICE } });
    s.addText(st[0], { x, y: y + 0.12, w: 2.7, h: 0.7, isTextBox: true, margin: 0, align: "center",
      fontFace: HFONT, fontSize: 28, bold: true, color: NAVY });
    s.addText(st[1], { x, y: y + 0.82, w: 2.7, h: 0.4, isTextBox: true, margin: 0, align: "center",
      fontFace: BFONT, fontSize: 11.5, color: MUTE });
  });
  // ethical box
  s.addShape(p.ShapeType.roundRect, { x: 7.3, y: 5.0, w: 5.6, h: 1.35, rectRadius: 0.08,
    fill: { color: NAVY } });
  s.addText([
    { text: "Ethical rule  ", options: { bold: true, color: MINT, fontSize: 13, breakLine: false } },
    { text: "financial_health_score is a wellbeing measure — never used to deny credit, cut a limit, or block an account.", options: { color: WHITE, fontSize: 12.5 } },
  ], { x: 7.55, y: 5.12, w: 5.15, h: 1.1, isTextBox: true, margin: 0, valign: "middle", fontFace: BFONT });
  footer(s, 4);
  s.addNotes("Plant the two rules: ratios over magnitudes, wellbeing over credit.");
})();

// ---------- generic content slides ----------
// one-chart: text left, chart right
function contentOne(n, sec, title, bullets, chartName, opts = {}) {
  const s = p.addSlide();
  s.background = { color: WHITE };
  tag(s, sec); heading(s, title);
  s.addText(bulletList(bullets), { x: 0.5, y: 1.75, w: 6.3, h: 3.5,
    isTextBox: true, valign: "top" });
  chart(s, chartName, 7.05, 1.7, 5.8, 4.6);
  // caveat sits under its chart (right); stat callout in the free lower-left
  if (opts.cav)
    s.addText("⚠  " + opts.cav, { x: 7.05, y: 6.4, w: 5.8, h: 0.6, isTextBox: true, margin: 0,
      fontFace: BFONT, fontSize: 10, italic: true, color: MUTE, valign: "top" });
  if (opts.stat) {
    s.addShape(p.ShapeType.roundRect, { x: 0.5, y: 5.5, w: 3.7, h: 1.2, rectRadius: 0.08, fill: { color: NAVY } });
    s.addText(opts.stat[0], { x: 0.5, y: 5.62, w: 3.7, h: 0.72, isTextBox: true, margin: 0, align: "center",
      fontFace: HFONT, fontSize: 28, bold: true, color: MINT });
    s.addText(opts.stat[1], { x: 0.5, y: 6.32, w: 3.7, h: 0.35, isTextBox: true, margin: 0, align: "center",
      fontFace: BFONT, fontSize: 11, color: WHITE });
  }
  footer(s, n);
  if (opts.note) s.addNotes(opts.note);
}
// two-chart: short bullets top band, two charts bottom
function contentTwo(n, sec, title, bullets, c1, c2, opts = {}) {
  const s = p.addSlide();
  s.background = { color: WHITE };
  tag(s, sec); heading(s, title);
  s.addText(bulletList(bullets), { x: 0.5, y: 1.6, w: 12.3, h: 1.65, isTextBox: true, valign: "top" });
  chart(s, c1, 0.55, 3.35, 5.95, 3.5);
  chart(s, c2, 6.85, 3.35, 5.95, 3.5);
  footer(s, n);
  if (opts.note) s.addNotes(opts.note);
}

// wide: bullets top band, one full-width chart below (for wide multi-panel charts)
function contentWide(n, sec, title, bullets, chartName, opts = {}) {
  const s = p.addSlide();
  s.background = { color: WHITE };
  tag(s, sec); heading(s, title);
  s.addText(bulletList(bullets), { x: 0.5, y: 1.6, w: 12.3, h: 1.55, isTextBox: true, valign: "top" });
  chart(s, chartName, 0.5, 3.2, 12.3, 3.8);
  footer(s, n);
  if (opts.note) s.addNotes(opts.note);
}

// ============ SLIDES 5–21 (auto-numbered) ============
let N = 4;
contentOne(++N, "Task 1 · EDA", "December is the spending engine — and it runs on frequency",
  ["Dec = 488B VND = 15.0% of the 3.24T annual — 2.8× the Feb trough.",
   "Peak is frequency: transaction count +187%, avg ticket −2.6%.",
   "The uplift is uniform: all 14 categories grow +181% to +193% — no single category drives it.",
   "Scale capacity, fraud monitoring & campaigns to volume, not basket size."],
  "t1_monthly_spend.png",
  { cav: "All timestamps are 2025; the uniform uplift looks like a synthetic seasonal multiplier — treat 15% as directional.",
    note: "Peaks are a frequency phenomenon across every category — the lever is trip frequency, not upsell." });

contentTwo(++N, "Task 1 · EDA — the spine", "Financial stress flips the budget: essential → discretionary",
  ["Stressed (FHS < 40): 72% discretionary vs healthy (FHS ≥ 80): 40% — the mix inverts completely.",
   "It is a gradient, not a threshold artefact: 72% → 64% → 57% → 54% → 49% → 41% across FHS bands; any cutoff pair keeps the direction (FHS<35 vs ≥85: 74% vs 30%).",
   "Highest-leverage help = budgeting visibility on discretionary spend, not credit restriction. This contrast anchors Tasks 4 and 5."],
  "t1_essential_discretionary.png", "t1_discretionary_gradient.png",
  { note: "THE slide — the gradient proves the inversion is real, not an artefact of the 40/80 cutoffs." });

contentTwo(++N, "Task 1 · EDA", "Where the signal is NOT: age is flat; categories are habits",
  ["Two shopping rhythms: Fuel = frequent touchpoint (1.59M ticket, bought by 96.8% of consumers); Groceries = 1.8× larger basket, bought by 99.3%.",
   "25–34 has the lowest point estimate (FHS 65.8, highest spend/income 0.716) — but bootstrap 95% CIs of all six age cohorts overlap (65.8–67.0).",
   "Age does not separate financial health → target behavioural ratios, not birth year."],
  "t1_category_ticket.png", "t1_age_cohort.png",
  { note: "One honest negative (age) and one habit insight (fuel/groceries are near-universal)." });

contentOne(++N, "Task 1 · EDA", "No regional digital divide: high-spend provinces mirror the nation",
  ["5 high-spend provinces with below-average digital share: Ha Noi, Dong Nai, Lam Dong, Hung Yen, Hai Phong.",
   "POS 58.9–59.3% of transactions vs 58.8% nationally; QR ~20%, E-com ~8.5%, Mobile ~7.5%, Recurring ~5%.",
   "Largest digital gap: −0.46pp (Dong Nai); digital value share 40.9–41.5% vs 41.5%.",
   "The gap is real but commercially negligible → province is not a lever for digital adoption."],
  "t1_province_channel.png",
  { stat: ["≤ 0.46pp", "largest digital-share gap"],
    note: "Q3 asked for the channel breakdown — it answers itself: every hub has the national mix." });

contentOne(++N, "Task 2 · Financial Health", "Health is a tight band; distress is episodic, never chronic",
  ["Consumer-level FHS: mean 66.3, range 42–81 — a narrow band with a mild low tail.",
   "Stressed months only 0.9%; 0 of 999 consumers have a 12-month mean below 40.",
   "Distress is episodic — healthy people dip in specific months (Feb 73.6 → Dec 54.2).",
   "Interventions must be event-triggered on the current month, not a static risk list."],
  "t2_fhs_distribution.png",
  { note: "Nobody is chronically unhealthy — trigger on the month, not the person." });

contentTwo(++N, "Task 2 · Financial Health", "Low health is an overspend story",
  ["Top correlates: spend-to-income −0.90, credit-utilization −0.86, volatility −0.50. Stressed vs healthy months: spend/income 2.10 vs 0.29.",
   "Step by step: mean FHS falls 72.4 → 68.4 → 66.0 → 63.8 → 60.9 across spend-to-income quintiles (−11.4 pts, ~10× the age spread).",
   "Counter-intuitive: stressed months are MORE engaged (81.1 vs 72.7). FHS and ratios share spend fields — directional, not causal."],
  "t2_low_health_drivers.png", "t2_sti_quintile.png",
  { note: "Two ratios are the whole game — the quintile chart makes r = −0.90 tangible." });

contentTwo(++N, "Task 2 · Financial Health", "The \"Stressed but Engaged\" crossover — and when to reach it",
  ["Rule (month grain): FHS < 40 AND engagement ≥ p75 (81.4) → 43 consumers = 52% of ALL stress episodes; stable at p70/p80 (44/41 consumers, 53%/48%).",
   "Stressed months put 23.5% of spend into 22–23h vs 8.3% for healthy — bigger late-night tickets, not more of them (count 11.6% vs 9.7%).",
   "Sunday + Monday carry 42% of stressed spend (vs 34%) → send pacing alerts Sunday–Monday evenings, before 22:00."],
  "t2_crossover.png", "t2_timing.png",
  { note: "More than half of every stress episode happens to someone we can reach in-app — and we now know when." });

contentWide(++N, "Task 2 · Financial Health", "Who differs? Province and age barely; occupation through spending",
  ["Province: 22 of 27 provinces (≥15 consumers) have a 95% CI containing the national mean 66.3. Age: all six cohort CIs overlap.",
   "Occupation (396 titles → 8 groups): Engineering/IT 69.1 and Business/finance 68.7 vs Office/public 64.5 and Manual 62.9 — a ~6-pt spread that mirrors spend-to-income (0.60 vs 0.76–0.79).",
   "Demographics act through the overspend ratio → target the ratio, never the group."],
  "t2_demographics.png",
  { note: "Deliverable 3 — the honest answer: the one demographic gap is really a spending gap." });

contentTwo(++N, "Task 3 · Engagement", "Engagement is saturated; digital is broad but shallow",
  ["Consumers by engagement segment: Low 1.0% · Medium 8.0% · High 74.1% · Very high 16.9% — the score does NOT segment the base.",
   "Channel mix: POS 58.8% · QR 19.8% · E-com 8.7% · Mobile 7.7% · Recurring 4.9%; average online spend share 24.7% per consumer.",
   "Non-POS channels carry 41% of trips and 41.5% of value (same ticket size as POS); truly online E-com + Mobile is ~17% of value."],
  "t3_segment_share.png", "t3_channel_mix.png",
  { note: "Bar, not pie: a pie would hide the 1% tail. Segment on the behaviours underneath, not the score." });

contentTwo(++N, "Task 3 · Engagement", "What actually discriminates: diversity & consistency",
  ["Category diversity: r +0.94 with engagement; still +0.81 without the dormant tail (Spearman +0.85) — not a tail artefact.",
   "Heatmap: 30–31 active days & recency 0 → engagement 79.8 (n=6,614); every 1–5-active-day cell stays ≤ 55 whatever the recency.",
   "Consistency beats recency and volume → build the early-warning flag on falling diversity and active days."],
  "t3_diversity_vs_engagement.png", "t3_recency_frequency.png",
  { note: "Scatter for two continuous variables; heatmap for the recency × frequency interaction." });

contentOne(++N, "Task 3 · Engagement", "High-health, low-engagement: dormancy hiding in \"healthy\"",
  ["Cutoff: FHS ≥ 70 AND engagement < 70 → 25 consumers (2.5%).",
   "Why 70: the count is 25 at engagement < 60, 65 and 70 (a natural gap) and jumps to 63 at < 75; FHS ≥ 65 gives 48, ≥ 75 gives 9.",
   "They moved spend to narrow online use (diversity 4.7 vs 13.2; online 0.61 vs 0.24); 24 of 25 sit in Emerging Digital.",
   "Play = reactivation of everyday use, NOT budgeting."],
  "t3_health_vs_engagement_quadrant.png",
  { cav: "n = 25, synthetic-inflated engagement — a cohort to watch, not a sized forecast.",
    note: "The sensitivity table is the answer to 'why this cutoff and not tighter or looser'." });

contentOne(++N, "Task 4 · Segmentation", "Method: cluster on behaviour, justify k honestly",
  ["Aggregate 10,992 consumer-months → 999 consumers (yearly mean profile); preprocessed dataset + dictionary delivered.",
   "8 z-scaled behavioural features across health, engagement & spending; demographics kept out of clustering, used only to profile.",
   "k-means chosen over a pure 2×2 so boundaries form across all 8 dimensions at once.",
   "k=4 via elbow + silhouette (0.251); coverage 999/999, all 7 minors retained — PASS."],
  "t4_silhouette.png",
  { note: "Moderate silhouette is expected for a behavioural continuum; the next slides validate it." });

contentTwo(++N, "Task 4 · Segmentation", "The four customer segments",
  ["Financially Healthy & Highly Engaged — 351 (35%): FHS 70.5, lowest util 0.148 → retain & grow value.",
   "Financially Stretched but Highly Engaged — 302 (30%): highest spend/income 0.835, still engaged → the wellbeing priority.",
   "High-Activity Digital Power Users — 258 (26%): most active & volatile → monetise & monitor drift.  ·  Low Engagement & Emerging Digital — 88 (9%): near-dormant, 60% of spend via E-com/Mobile → activate."],
  "t4_segment_sizes.png", "t4_segment_profiles.png",
  { note: "Segment 2 is the addressable wellbeing priority." });

contentOne(++N, "Task 4 · Segmentation", "Validation: stable segments, and a December slide",
  ["Stable: 20 random seeds → ARI 0.988; 80% bootstrap × 50 → ARI 0.911.",
   "GMM agrees only partly (ARI 0.26): Emerging Digital is identical, the three large segments form one continuum — hence silhouette 0.251.",
   "Monthly migration: a Healthy month slides to Stretched 23% of the time — but 72% from November to December.",
   "Segments correlate with age & gender (p < 0.01) though not used as inputs → trigger tools on behaviour only."],
  "t4_pca.png",
  { stat: ["72%", "Healthy → Stretched, Nov → Dec"],
    note: "Stable enough to act on; the Nov→Dec slide is the timing evidence for planning reminders." });

contentOne(++N, "Task 5 · Recommendations", "A six-tool, non-punitive action plan",
  ["① Budgeting → Stretched-Engaged (302): spend-vs-income dashboard (driver −0.90).",
   "② Spend alerts → Crossover (43 = 52% of stress): Sunday–Monday evenings, before 22:00.",
   "③ Planning reminders → Power Users (258) + Healthy (351) in November, before the 72% December slide.",
   "④ Education → Distress tail (67): needs-vs-wants modules (essential ratio +0.48).",
   "⑤ Digital nudges → Emerging Digital (88): in-app habit loops — they already spend 60% via E-com/Mobile.",
   "⑥ Product suggestions → Healthy-Engaged (351): savings/loyalty, opt-in, never auto-extend."],
  "t5_target_sizes.png",
  { note: "One tool per required type, each bound to an exact size, a real ratio and now a timing." });

contentOne(++N, "Task 5 · Recommendations", "Prioritization & the ethical rule",
  ["Ranking (reach × driver): Budgeting → Alerts → Reminders → Products → Nudges → Education.",
   "Lead with Budgeting + Alerts (the wellbeing mission); layer growth on top.",
   "No double-counting: the 4 segments partition 999; crossover (43) & distress (67) are overlays inside Segment 2.",
   "Fair by design: every trigger is a behavioural ratio; segments correlate with age/gender, so we never target by demographics."],
  "t5_priority_ranking.png",
  { stat: ["NEVER", "FHS → credit decision"],
    note: "The rule is the deck's contract — a low score triggers help offered, never access removed." });

contentOne(++N, "Task 5 · Impact", "Expected impact, measurement & a 90-day roadmap",
  ["Scenario (illustrative): FHS = 84.1 − 25.3 × spend/income. A 10% trim for the Stretched 302 cuts stress months 95 → 65 (−32%); 5% → 80 (−16%).",
   "Every tool gets one KPI and a randomised holdout (e.g. Budgeting: spend-to-income, 10% holdout for 3 months).",
   "Days 0–30: Budgeting + Alerts · 31–60: November Reminders + Nudges · 61–90: Education + opt-in Products; keep what moves the KPI."],
  "t5_impact_scenario.png",
  { stat: ["−32%", "stress months at a 10% trim"],
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
    ["Honest limits", "Synthetic single-year data, uniform December uplift, engineered engagement, segments on a continuum — sizes directional, conclusions robust on ratios."],
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
