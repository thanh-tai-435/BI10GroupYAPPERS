# Data dictionary — task4_features.csv

Preprocessed dataset used for the Task 4 segmentation. One row per customer (999 rows, 23 columns, 0 missing values).
Produced by `notebooks/full_pipeline.ipynb` (section "Task 4", cell "preprocessed dataset used for modelling").

**Source:** `consumer_financial_health_engagement_2025.csv` (10,992 consumer-months). Each customer's months are averaged into one yearly profile.
Only ratios and scores are used: raw VND fields (income, credit limit, balances, spend) are excluded because the synthetic magnitudes are inflated.

**Feature selection:** 8 behavioural features covering health, engagement and spending. Excluded: `essential_spend_ratio` (equals 1 − `discretionary_spend_ratio`), and `category_diversity`, `active_transaction_days` and `transaction_recency_days`, which are near-constant (their 75th percentile equals the maximum). Demographics are kept for profiling only and are NOT model inputs.

| Column | Type | Description |
|---|---|---|
| `consumer_id` | string | Customer key; links to both source files |
| `financial_health_score` | float (0–100) | Mean monthly `financial_health_score` (health axis) |
| `spend_to_income_ratio` | float | Mean monthly `spend_to_income_ratio` (health axis) |
| `credit_utilization_ratio` | float | Mean monthly `credit_utilization_ratio` (health axis) |
| `spending_volatility` | float | Mean monthly `spending_volatility` (health axis) |
| `engagement_score` | float (0–100) | Mean monthly `engagement_score` (engagement axis) |
| `transaction_count` | float | Mean transactions per month (engagement axis) |
| `discretionary_spend_ratio` | float (0–1) | Mean discretionary share of spend (spending axis) |
| `online_spend_ratio` | float (0–1) | Mean online share of spend (spending axis) |
| `cluster` | int (0–3) | k-means label (k = 4, `n_init=25`, `random_state=42`) |
| `segment` | string | Business label: `Healthy & Engaged` (351), `Stretched & Engaged` (302), `High-Activity Users` (258), `Occasional Online-First` (88) |
| `z_financial_health_score` … `z_online_spend_ratio` | float | The 8 features above, z-scaled (`StandardScaler` fitted on the 999 customers); these 8 columns are the exact k-means input |
| `age` | int (15–96) | Age in years; profiling only (7 customers under 18 kept) |
| `gender` | string | `Nam` = male, `Nữ` = female; profiling only |
| `occupation` | string | Occupation title (Vietnamese, as in the source); profiling only |
| `province` | string | Province/city (Vietnamese, as in the source); profiling only |

**How segment names are assigned:** the cluster with the highest mean FHS → Healthy & Engaged; highest spend-to-income → Stretched & Engaged; highest transaction count → High-Activity Users; lowest engagement → Occasional Online-First.

**Usage rule:** `financial_health_score` and `segment` are for wellbeing support only. They must never be used to approve or deny credit, cut a limit, raise a rate or block an account.
