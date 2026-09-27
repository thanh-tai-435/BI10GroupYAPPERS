# CLAUDE.md — BI10 Round 01, Group YAPPERS

Data-analysis case for ITB (Vietnamese consumer finance). Deliverable = a ≤22-slide deck. Full brief in `DeBai.md`; case detail in `BI10_ROUND01_DATASET/consumer_financial_health_case_study.md`.

## Golden rules of the case
- **Wellbeing study, NOT credit scoring.** `financial_health_score` must NEVER deny credit, cut a limit, raise a rate, or block an account.
- **Use ratios, not raw VND.** Synthetic income/credit/balance magnitudes are inflated and meaningless in absolute terms. Compare on ratios/shares.
- Every claim must be backed by a number or chart.

## Environment gotchas (already solved — don't rediscover)
- **Run Python with `py`, NOT `python`.** Plain `python` = a venv without pandas. `py` (3.12) has pandas 2.3.3, numpy, pyarrow, sklearn, matplotlib.
- **Vietnamese text breaks the cp1252 console.** Every script: `import sys; sys.stdout.reconfigure(encoding="utf-8")` and run with env `PYTHONUTF8=1`. Figures/pptx are fine — only the console breaks.
- **Node/pptxgenjs:** `pptxgenjs` is installed locally (`node_modules/`). Build deck: `node draft/build_deck.js`.
- **LibreOffice on Windows:** the skill's `soffice.py` wrapper is Unix-only (needs AF_UNIX). Call the binary directly: `"/c/Program Files/LibreOffice/program/soffice.exe" --headless --convert-to pdf --outdir draft/ <file.pptx>`.
- **pdftoppm here has `-png`, not `-jpeg`.** Use `pdftoppm -png -r 100 file.pdf slide`.

## Data files — naming is MISLEADING
Only TWO real datasets, each stored twice under confusing names (no real parquet exists despite extensions):

| Use this | What it is | Rows |
|---|---|---|
| `BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv` | **monthly** consumer-month grain (primary) | 10,992 (999 consumers) |
| `BI10_ROUND01_DATASET/consumer_transactions_2025.parquet/consumer_transactions_2025.csv` | **transactions** (plain CSV despite folder name) | 1,852,394 |

**Traps — do NOT use:** `consumer_transactions_2025.csv.gz` (actually a duplicate of the monthly file) and `consumer_transactions_2025.parquet.gz` (gzipped copy of the transactions CSV).

Link the two on `consumer_id`. 999 consumers, min age **15** (7 minors aged 15–17 — don't drop them when binning). Categorical fields are in Vietnamese.

## Project structure
```
DeBai.md              cleaned brief
CLAUDE.md             this file
draft/                all analysis (see below) — the working area
outputs/figures/      chart PNGs (git-ignored): make_charts.py + taskN_deep.py
notebooks/            full_pipeline.ipynb = SUBMISSION notebook (English, self-contained code, no GitHub token, downloads data from public Drive; saved with outputs). task*_*.ipynb = team working notebooks P1–P5 (need GH_TOKEN; cells generated from draft/taskN_deep.py)
BI10_ROUND01_DATASET/ raw data (git-ignored)
```
`.gitignore` excludes data, PDFs, all `*.csv`/`*.parquet*`, outputs, `node_modules`. Scripts + findings + outline ARE tracked.

## What's done (all 5 tasks + deck)
Each task in `draft/`: `taskN*.py` (analysis) + `taskN_output.txt` (captured run) + `taskN_findings.md` (senior-BI write-up). Every script was actually run; numbers reproduce.
- **task1_eda** — EDA Q1–Q5. **task2** — financial health. **task3** — engagement. **task4** — segmentation (+ `task4_features.csv`, per-consumer segment labels, git-ignored). **task5** — recommendations.
- **Deep-dives** `taskN_deep.py` (+ `taskN_deep_output.txt`): each runs its base script then extra analysis; its `## CELL` blocks are the notebook cells. New charts: t1_province_channel, t1_discretionary_gradient, t2_demographics, t2_timing, t2_sti_quintile, t3_segment_share, t3_diversity_hist, t3_recency_frequency, t4_pca, t5_impact_scenario. Task 4 also writes `data_dictionary_task4.md`.
- `make_charts.py` → the original 16 PNGs in `outputs/figures/` (t1_*..t5_*).
- `slide_outline.md` → original 18-slide plan (header notes the 4 added slides).
- `build_deck.js` → **`draft/YAPPERS_BI10_R01.pptx`** (**22 slides**, auto-numbered, QA'd 27/09).
- Team guide: `draft/YAPPERS_huong_dan_Colab.xlsx` (per-person sheets, statuses).

## Key findings (the spine)
- **Overspend drives low health:** spend-to-income r −0.90, credit-utilization r −0.86. Not low income.
- **Budget inverts under stress:** stressed (FHS<40) = 72% discretionary vs healthy (FHS≥80) = 40%. Strongest signal.
- **Stress is episodic:** 0/999 chronically stressed; crossover (FHS<40 & engagement≥p75 81.4) = 43 consumers = 52% of all stress episodes.
- **Weak levers:** geography (max digital gap 0.46pp) and age (all cohort CIs overlap). Occupation spreads ~6 FHS pts but tracks spend-to-income — target ratios, not demographics.
- **Timing:** stressed months put 23.5% of spend value into 22–23h (vs 8.3%; bigger tickets, not more); Sun+Mon 42%. Healthy→Stretched slide = 72.4% Nov→Dec.
- **Two-years-folded caveat is REAL** (case study §12: two source years folded onto 2025, timestamps re-dated so all read 2025; inflates monthly volume). Dec uplift is uniform across 14 categories. Non-POS = 41% of trips AND of value (the old '21% of spend' mixed in online_spend_ratio).
- **4 segments** (k-means k=4, silhouette 0.251, seed ARI 0.988, bootstrap ARI 0.911, 999/999 covered; correlate with age/gender p<0.01): Healthy&Engaged 351 / Stretched&Engaged 302 / Digital Power Users 258 / Emerging Digital 88.
- **6-tool plan** priority: Budgeting(302) → Alerts(43) → Reminders(258) → Products(351) → Nudges(88) → Education(67).

## Regenerate everything
```bash
PYTHONUTF8=1 py draft/task1_eda.py     # (task2..task5 likewise)
PYTHONUTF8=1 py draft/task1_deep.py   # (task2..task5_deep likewise; task2_deep reads task1_age_ci.csv if present)
PYTHONUTF8=1 py draft/make_charts.py   # charts
node draft/build_deck.js               # deck -> draft/YAPPERS_BI10_R01.pptx
```

## Before submitting
- **Rename the deck** to the required format: `[TeamName_LeaderName_BI10_R01]` — insert the leader's name (currently `YAPPERS_BI10_R01.pptx`).
- Deck must stay ≤22 slides, 16:9, English. Additional files → one ZIP/RAR named `[TeamName_LeaderName_BI10_R01_data]`.
- **Deadline: 23:59, Sep 28, 2026.**

## Git
- Repo: https://github.com/thanh-tai-435/BI10GroupYAPPERS (private). Commits use the global account (Tai Pham), no Claude co-author.
```
