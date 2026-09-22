# BI10 Round 01 — Group YAPPERS

Consumer finance customer understanding & segmentation case (ITB). Full brief: [DeBai.md](DeBai.md).

## Structure

```
BI10_ROUND01_DATASET/   raw data (git-ignored, provided separately)
notebooks/              one notebook per task (task1_eda … task5_recommendations)
src/                    shared helpers (data loading, plotting)
outputs/figures/        exported charts (git-ignored)
DeBai.md                assignment brief
```

## Data

Not in git (large / provided). Place the `BI10_ROUND01_DATASET/` folder at repo root:

- `consumer_financial_health_engagement_2025.csv` — consumer-month grain (primary source)
- `consumer_transactions_2025.parquet` — transaction grain (detail)
- `data_dictionary.xlsx` — field definitions

Link the two on `consumer_id`. Values in VND. Data is synthetic.

## Tasks

1. Exploratory data analysis
2. Financial health analysis
3. Customer engagement analysis
4. Customer segmentation
5. Business recommendations

**Rule:** `financial_health_score` is for understanding only — never used to deny credit, cut a limit, or block an account.

## Setup

```bash
pip install -r requirements.txt
jupyter lab
```

## Deadline

Slide proposal (≤22 slides, 16:9, English) by **23:59 Sep 28, 2026**. File: `[TeamName_LeaderName_BI10_R01]`.
