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
    ["Stress is episodic & hits the engaged", "0 of 999 chronically stressed; the crossover = 43 consumers = 52% of ALL stress episodes."],
    ["Four actionable segments", "k-means (k=4), 999/999 covered — sizes 351 / 302 / 258 / 88."],
    ["A 6-tool wellbeing plan", "lead with Budgeting (302) + in-app Spend Alerts (43); FHS never denies, cuts, or blocks credit."],
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

// ============ SLIDES 5–17 ============
contentOne(5, "Task 1 · EDA", "December is the spending engine — and it runs on frequency",
  ["Dec = 488B VND = 15.0% of the 3.24T annual — 2.8× the Feb trough.",
   "Peak is frequency: transaction count +187%, avg ticket −2.6%.",
   "Customers buy more often, not pricier (year-end / Tết prep).",
   "Scale capacity, fraud monitoring & campaigns to volume, not basket size."],
  "t1_monthly_spend.png",
  { cav: "Source folds two years onto 2025, amplifying December — treat 15% as directional.",
    note: "Peaks are a frequency phenomenon — the lever is trip frequency, not upsell." });

contentOne(6, "Task 1 · EDA — the spine", "Financial stress flips the budget: essential → discretionary",
  ["Stressed (FHS < 40): 28% essential / 72% discretionary.",
   "Healthy (FHS ≥ 80): 60% essential / 40% discretionary.",
   "The mix inverts completely — low health is NOT people scraping by on necessities.",
   "Highest-leverage help = budgeting visibility on discretionary spend, not credit restriction.",
   "This single contrast anchors segmentation (Task 4) and recommendations (Task 5)."],
  "t1_essential_discretionary.png",
  { stat: ["72% vs 40%", "discretionary: stressed vs healthy"],
    note: "This is THE slide — every later decision traces back to this inversion." });

contentTwo(7, "Task 1 · EDA", "Where the signal is NOT: geography & age are flat",
  ["No regional digital divide — every high-spend province sits at ~41% digital (±0.5pp); province is not a lever.",
   "Two shopping rhythms: Fuel = frequent touchpoint (1.59M ticket); Groceries = 1.8× larger stock-up basket.",
   "25–34 is the vulnerability hotspot (lowest FHS 65.8, highest spend/income 0.716) — but age spreads only 65.8–67.0, a weak differentiator. Target behavioural ratios, not the map or birth year."],
  "t1_category_ticket.png", "t1_age_cohort.png",
  { note: "Two honest negatives (geography, age) + one behavioural positive." });

contentOne(8, "Task 2 · Financial Health", "Health is a tight band; distress is episodic, never chronic",
  ["Consumer-level FHS: mean 66.3, range 42–81 — a narrow band with a mild low tail.",
   "Stressed months only 0.9%; 0 of 999 consumers have a 12-month mean below 40.",
   "Distress is episodic — healthy people dip in specific months (Feb 73.6 → Dec 54.2).",
   "Interventions must be event-triggered on the current month, not a static risk list."],
  "t2_fhs_distribution.png",
  { note: "Nobody is chronically unhealthy — trigger on the month, not the person." });

contentOne(9, "Task 2 · Financial Health", "Low health is an overspend story",
  ["Top correlates: spend-to-income −0.90, credit-utilization −0.86, volatility −0.50.",
   "Stressed vs healthy months: spend/income 2.10 vs 0.29; util 0.58 vs 0.08.",
   "Counter-intuitive: stressed months are MORE engaged (81.1 vs 72.7, r −0.30).",
   "Demographics add nothing — score & alert on two ratios, reach via the channel they use."],
  "t2_low_health_drivers.png",
  { cav: "FHS and essential/discretionary ratios share spend fields — directional, not causal.",
    note: "Two ratios are the whole game — and the stressed are active, not disengaged." });

contentOne(10, "Task 2 · Financial Health", "The \"Stressed but Engaged\" crossover",
  ["Reproducible rule (month grain): FHS < 40 AND engagement ≥ p75 (81.4).",
   "43 consumers / 49 months = 52% of ALL stress episodes.",
   "Profile: spend/income 1.89, credit-util 0.55, online 0.49 (2× national).",
   "Active, digital, over-extended — reachable at near-zero cost via in-app alerts."],
  "t2_crossover.png",
  { stat: ["52%", "of all stress episodes"],
    cav: "49 months / 43 consumers is a small synthetic cell — a directional archetype.",
    note: "More than half of every stress episode happens to someone we can text right now." });

contentTwo(11, "Task 3 · Engagement", "Engagement is saturated; digital is broad but shallow",
  ["99.0% of consumer-months are high/very-high engagement (mean 77.8) — the score does NOT segment the base.",
   "Channel mix: POS 58.8% · QR 19.8% · E-com 8.7% · Mobile 7.7% · Recurring 4.9% → digital = 41% of trips but only 21% of spend.",
   "Digital handles many small tickets; big baskets stay on POS. Grow digital value, not just reach. (Note: synthetic cards are engineered highly active — the 99% is partly an artefact.)"],
  "t3_engagement_dist.png", "t3_channel_mix.png",
  { note: "Don't segment on the engagement score — it's a ceiling. Segment on behaviours underneath." });

contentOne(12, "Task 3 · Engagement", "What actually discriminates: diversity & consistency",
  ["Category diversity is the cleanest signal: r +0.94 with engagement (consumer level).",
   "The dormant tail is disengaged because it is narrow — 4–6 categories vs ~14 for the core.",
   "Consistency (active days r +0.59) beats raw volume (txn count r +0.40).",
   "A falling category count flags disengagement before the composite score moves."],
  "t3_diversity_vs_engagement.png",
  { note: "Build the early-warning flag on category diversity." });

contentOne(13, "Task 3 · Engagement", "High-health, low-engagement: dormancy hiding in \"healthy\"",
  ["Cutoff: FHS ≥ 70 AND engagement < 70 → 25 consumers (2.5%).",
   "Why 70: the same 25 return at eng < 65/68/70 — a natural gap in the data.",
   "They moved spend off-card to narrow online use (diversity 4.7 vs 13.2; online 0.61 vs 0.24).",
   "Play = reactivation of everyday use, NOT budgeting — distinct from the 67 distress-tail customers."],
  "t3_health_vs_engagement_quadrant.png",
  { cav: "n = 25, synthetic-inflated engagement — a cohort to watch, not a sized forecast.",
    note: "Two low-engagement tails, opposite remedies — don't merge them." });

contentOne(14, "Task 4 · Segmentation", "Method: cluster on behaviour, justify k honestly",
  ["Aggregate 10,992 consumer-months → 999 consumers (yearly mean profile).",
   "8 z-scaled behavioural features across health, engagement & spending; demographics excluded (no signal).",
   "k-means chosen over a pure 2×2 so boundaries form across all 8 dimensions at once.",
   "k=4 via elbow + silhouette (0.251); coverage 999/999, all 7 minors retained — PASS."],
  "t4_silhouette.png",
  { note: "Moderate silhouette is expected for a behavioural continuum; the 2×2 validates the poles." });

contentTwo(15, "Task 4 · Segmentation", "The four customer segments",
  ["Financially Healthy & Highly Engaged — 351 (35%): FHS 70.5, lowest util 0.148 → retain & grow value.",
   "Financially Stretched but Highly Engaged — 302 (30%): highest spend/income 0.835, still engaged → the wellbeing priority.",
   "High-Activity Digital Power Users — 258 (26%): most active & volatile → monetise & monitor drift.  ·  Low Engagement & Emerging Digital — 88 (9%): near-dormant but 67% online → activate; highest growth headroom."],
  "t4_segment_sizes.png", "t4_segment_profiles.png",
  { note: "Segment 2 turns Task 1's 25–34 vulnerability into an addressable 302-person group." });

contentOne(16, "Task 5 · Recommendations", "A six-tool, non-punitive action plan",
  ["① Budgeting → Stretched-Engaged (302): spend-vs-income dashboard (driver −0.90).",
   "② Spend alerts → Crossover (43 = 52% of stress): event-triggered in-app pacing.",
   "③ Planning reminders → Power Users (258): pre-December pacing (volatility r −0.50).",
   "④ Education → Distress tail (67): needs-vs-wants modules (essential ratio +0.48).",
   "⑤ Digital nudges → Emerging Digital (88): onboarding & habit loops (diversity r +0.94).",
   "⑥ Product suggestions → Healthy-Engaged (351): savings/loyalty, opt-in, never auto-extend."],
  "t5_target_sizes.png",
  { note: "One tool per required type, each bound to an exact size and a real ratio." });

contentOne(17, "Task 5 · Recommendations", "Prioritization & the ethical rule",
  ["Ranking (reach × driver): Budgeting → Alerts → Reminders → Products → Nudges → Education.",
   "Lead with Budgeting + Alerts (the wellbeing mission); layer growth on top.",
   "No double-counting: the 4 segments partition 999; crossover (43) & distress (67) are overlays inside Segment 2.",
   "Fair by design: targeting on ratios, not demographics; monitor (don't use) a mild male skew."],
  "t5_priority_ranking.png",
  { stat: ["NEVER", "FHS → credit decision"],
    note: "The rule is the deck's contract — a low score triggers help offered, never access removed." });

// ============ SLIDE 18 — CLOSING ============
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
    ["Honest limits", "Synthetic single-year data, flat geography/age, engineered engagement — sizes directional, conclusions robust on ratios."],
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
