# CLAUDE.md — BI10 Round 01, Group YAPPERS

Data-analysis case for ITB (Vietnamese consumer finance). Deliverable = a ≤22-slide deck + one ZIP of supporting files. Full brief in `DeBai.md`; case detail + grading rubric in `BI10_ROUND01_DATASET/consumer_financial_health_case_study.md`.

## Golden rules of the case
- **Wellbeing study, NOT credit scoring.** `financial_health_score` must NEVER deny credit, cut a limit, raise a rate, or block an account. Product suggestions = opt-in savings/loyalty, never a credit-line increase.
- **Use ratios, not raw VND.** Synthetic income/credit/balance magnitudes are inflated. Compare on ratios/shares (no VND fields in driver charts).
- Every claim must be backed by a number or chart, and **every number on a slide must be printed by the submission notebook**.
- Target by behaviour, never by demographics (segments correlate with age/gender).

## What the brief requires (checklist)
- **Format:** ≤22 slides incl. 1 Executive Summary + 1 Table of Contents; 4 sections (Exec Summary, TOC, Introduction to the Case, Task 1–5 results); English; 16:9; ≤100 MB; **every chart has a source/caption**; show process, reasoning, conclusions.
- **File names:** deck `[TeamName_LeaderName_BI10_R01]`, extra files in ONE ZIP/RAR `[TeamName_LeaderName_BI10_R01_data]`.
- **Rubric (case study §10):** data quality 15% · EDA 20% · health & engagement 20% · segmentation 20% · recommendations 15% · communication 10%.
- **Task 1:** Q1–Q5 (Q1 VND + % + count-vs-ticket; Q3 ≥2 provinces with channel breakdown; top-performing AND lagging segments).
- **Task 2:** D1 distribution · D2 drivers of low health · D3 occupation/age/province · D4 reproducible "stressed but engaged" rule. Brief suggests using the transaction file (category, timestamps).
- **Task 3:** D1 distribution + share per segment · D2 5 channels + avg online share · D3 diversity range/link · D4 recency & frequency ranges/links · D5 healthy-but-disengaged size, profile, cutoff and WHY vs stricter/looser · D6 chart type fits the data.
- **Task 4:** preprocessing & features, model choice + parameter justification, 100% coverage, validation, business labels, side-by-side profiles + recommendations, limitations & future work, preprocessed dataset deliverable.
- **Task 5 = the "6 tool types"** (brief wording): budgeting tools · spend alerts · financial-planning reminders · financial-education content · digital-channel nudges · suitable product suggestions. Each tied to a real number/column, exact target size + %, ranked by reach AND driver strength, plus the credit rule stated explicitly.

## Environment gotchas (already solved — don't rediscover)
- **Run Python with `py`, NOT `python`.** Plain `python` = a venv without pandas. `py` (3.12) has pandas 2.3.3, numpy, sklearn, scipy, matplotlib, nbclient.
- **Vietnamese text breaks the cp1252 console.** Scripts: `sys.stdout.reconfigure(encoding="utf-8")` + env `PYTHONUTF8=1`. In notebooks `sys.stdout` has no `reconfigure` (shim it or avoid it).
- **Long heredocs in the Bash tool often fail** ("unexpected EOF") — write files with the Write tool, then run them.
- **Grep the brief/case case-insensitively** (`-i`): a case-sensitive search for "fold" missed "Folding" and a correct caveat was wrongly removed once.
- **Node/pptxgenjs** installed locally. Build: `node draft/build_deck.js`. Table `margin` is in inches (a value like 6 breaks the table).
- **Validate the deck** with the pptx skill: `py <pptx-skill>/scripts/office/validate.py draft/YAPPERS_BI10_R01.pptx`.
- **LibreOffice:** call the binary directly: `"/c/Program Files/LibreOffice/program/soffice.exe" --headless --convert-to pdf --outdir draft/ <file.pptx>`; then `pdftoppm -png -r 80 file.pdf slide` (no `-jpeg`).

## Data files — naming is MISLEADING
| Use this | What it is | Rows |
|---|---|---|
| `BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv` | **monthly** consumer-month grain (primary) | 10,992 (999 consumers) |
| `BI10_ROUND01_DATASET/consumer_transactions_2025.parquet/consumer_transactions_2025.csv` | **transactions** (plain CSV despite folder name) | 1,852,394 |

**Traps:** `consumer_transactions_2025.csv.gz` (duplicate of the monthly file), `consumer_transactions_2025.parquet.gz` (gzipped transactions CSV — used only by Colab download). Link on `consumer_id` (+ month). Min age **15** (7 minors — keep them). Categories are Vietnamese. `transaction_day_of_week` 0 = Monday. Engagement segment bands 40/60/80. 908 customers have 12 months; **91 appear in only 1–2 months (1–2 active days)**. Public Drive file IDs (anyone with link): monthly `1YyueAH9Kasid6V_obml9pCMwh2dB0ryn`, transactions gz `1O33KpFbUx6_BRGwFTb80xVSB3tzXqt5H`, dictionary `1nFlZHmuaoK8VQ5xqRN2f4ZLqoR3gk2j1`.

## Source of truth & pipeline
1. **`draft/notebook_src/full_pipeline_src.py`** (percent-format `# %%` cells) is the source of the submission notebook. Edit it, then:
   `PYTHONUTF8=1 py draft/notebook_src/py2nb.py draft/notebook_src/full_pipeline_src.py notebooks/full_pipeline.ipynb`
2. Execute the notebook (Colab "Run all", or locally with nbclient, working dir `notebooks/`; it `chdir`s to the repo root). It downloads data if missing, prints every number, and its **Appendix writes the 21 deck charts `outputs/figures/deck_*.png`** (blue theme) plus a "Supporting numbers quoted on the slides" cell. Save it WITH outputs.
3. `node draft/build_deck.js` → `draft/YAPPERS_BI10_R01.pptx`, then validate + render + look at every slide.
- `full_pipeline.ipynb` is English, self-contained, needs **no GitHub token**. The team notebooks `notebooks/task*_*.ipynb` (P1–P5) clone the private repo and need a **classic** token with `repo` scope (fine-grained tokens can't reach another user's repo as collaborator).
- Older layers, kept for history only: `draft/task*.py`, `draft/task*_deep.py`, `draft/make_charts.py`, `draft/task*_findings.md` (pre-review wording), `draft/review/` (6-agent review reports + v2 chart scripts, no longer used by the deck).

## Deck design conventions (blue & white, consulting style)
- Action titles = one-sentence insight; one message per slide; left big chart, right panel = big number + 3 short takeaways; two-chart slides get 3 insight cards below; navy title & closing slides.
- Palette NAVY 0B2545 · BLUE 1F5FA8 · MID 4A90D9 · LIGHT A9C6EA · PALE EEF4FB; font Arial. No accent lines under titles, no decorative stripes.
- Long detail goes in speaker notes. Slide order follows the brief: 5–8 Task 1 (Q1, Q2, Q3, Q4&Q5), 9–12 Task 2 (D1–D4), 13–15 Task 3, 16–18 Task 4, 19–21 Task 5, 22 closing.

## Key findings (the spine)
- **Overspend drives low health:** spend-to-income r −0.90, utilization r −0.86 (one factor, R² 0.82); 98% of stress months spend > income.
- **Budget inverts under stress:** 71.6% vs 40.5% discretionary; the flip is in VALUE (purchases ≥10M VND = 4.3% of stressed transactions, 54% of value; travel +22pp).
- **Stress is episodic:** 0/999 stressed on average, 869 (87%) dip below 60 once; Jan+Dec hold 46/95 stress months.
- **Crossover rule:** FHS < 40 AND engagement ≥ 81.4 (p75 of all consumer-months) → 43 customers, 49 months = 52% of stress months (39 Stretched + 4 Healthy); they hold 67/95 (71%) of all stress months.
- **Timing:** stressed months put 23.5% of spend value at 22–23h (vs 8.3%); bigger tickets, not more of them.
- **December** lowers FHS ~13 pts in every full-year segment (calendar effect).
- **Engagement saturated:** 91% High/Very high; the whole low tail = the 91 one-off customers. Healthy-but-disengaged = 25 (FHS ≥ 70 & engagement < 70; flat 60–70 = empty gap).
- **Demographics act through spending:** occupation gap 6.2 → 1.3 pts, province 4.8 → 1.6 once spend-to-income is held constant; age flat (p 0.13). Q3: 6 high-spend provinces trail digital by ≤ 0.46pp.
- **Segments (k-means k=4, 8 z-scaled ratios):** Healthy & Engaged 351 / Stretched & Engaged 302 / High-Activity Users 258 / Occasional Online-First 88 (≈ brief's Emerging Digital). Silhouette 0.25, seed ARI 0.988, bootstrap 0.911, 999/999 covered.
- **Task 5 mapping:** ① Budgeting → Stretched 302 · ② Spend alerts → crossover 43 · ③ Planning reminders → High-Activity 258 (November) · ④ Education → low health & engagement 67 · ⑤ Digital nudges → Occasional 88 · ⑥ Product suggestions → Healthy 351 (adults). Ranking = reach × |r(trigger, outcome)|, wellbeing first: 271 → 128 → 37 → 32 | 74 → 52; alerts launch first (exception). What-if: 10% spend trim → stress months 95 → 65–68 (−28 to −32%).

## Claims that were WRONG and must not come back
- "72% of Healthy slide to Stretched Nov→Dec" — seasonality artefact (dropped).
- "Sunday + Monday = 42% of stressed spend" — not robust month by month (dropped).
- "Digital = 41% of trips but 21% of spend" — mixed two definitions; non-POS is 41% of trips AND value.
- "HCMC has the top FHS" — it is Ha Noi (67.8). Q3 has 6 provinces, not 5 (Nghe An).
- Removing the "two source years folded onto 2025" caveat — it is REAL (case §12).

## Before submitting
- Rename the deck and build the ZIP (needs the leader's name): notebook, `task4_features.csv` + `draft/data_dictionary_task4.md`, scripts, charts.
- **Deadline: 23:59, 28 Sep 2026** (aim for 20:00). Record the screen while submitting; check for ITB Club's confirmation within 24 h.

## Git
- Repo: https://github.com/thanh-tai-435/BI10GroupYAPPERS (private). Commits use the global account (Tai Pham), **no Claude co-author**. Push when the user asks.
