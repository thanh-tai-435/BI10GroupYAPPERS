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
outputs/figures/      16 chart PNGs (git-ignored, regen via draft/make_charts.py)
notebooks/            empty per-task notebooks (unused; work went into draft/*.py)
BI10_ROUND01_DATASET/ raw data (git-ignored)
```
`.gitignore` excludes data, PDFs, all `*.csv`/`*.parquet*`, outputs, `node_modules`. Scripts + findings + outline ARE tracked.

## What's done (all 5 tasks + deck)
Each task in `draft/`: `taskN*.py` (analysis) + `taskN_output.txt` (captured run) + `taskN_findings.md` (senior-BI write-up). Every script was actually run; numbers reproduce.
- **task1_eda** — EDA Q1–Q5. **task2** — financial health. **task3** — engagement. **task4** — segmentation (+ `task4_features.csv`, per-consumer segment labels, git-ignored). **task5** — recommendations.
- `make_charts.py` → 16 PNGs in `outputs/figures/` (t1_*..t5_*).
- `slide_outline.md` → 18-slide plan.
- `build_deck.js` → **`draft/YAPPERS_BI10_R01.pptx`** (18 slides, validated, QA'd).

## Key findings (the spine)
- **Overspend drives low health:** spend-to-income r −0.90, credit-utilization r −0.86. Not low income.
- **Budget inverts under stress:** stressed (FHS<40) = 72% discretionary vs healthy (FHS≥80) = 40%. Strongest signal.
- **Stress is episodic:** 0/999 chronically stressed; crossover (FHS<40 & engagement≥p75 81.4) = 43 consumers = 52% of all stress episodes.
- **Weak levers:** geography (all provinces ~41% digital) and age (FHS 65.8–67.0) — target behavioural ratios, not demographics.
- **4 segments** (k-means k=4, silhouette 0.251, 999/999 covered): Healthy&Engaged 351 / Stretched&Engaged 302 / Digital Power Users 258 / Emerging Digital 88.
- **6-tool plan** priority: Budgeting(302) → Alerts(43) → Reminders(258) → Products(351) → Nudges(88) → Education(67).

## Regenerate everything
```bash
PYTHONUTF8=1 py draft/task1_eda.py     # (task2..task5 likewise)
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
