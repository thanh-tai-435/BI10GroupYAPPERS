"""
Task 4 - Customer Segmentation (BI10 Round 01)
Aggregate 12 monthly rows -> 1 row/consumer, cluster on scaled behavioural ratios.
Run: PYTHONUTF8=1 py draft/task4.py   (tee to task4_output.txt)
Source: monthly consumer file (PRIMARY grain).
"""
import sys, pandas as pd, numpy as np
sys.stdout.reconfigure(encoding="utf-8")
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

MON = "BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv"
SEED = 42
def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)

# ---------------------------------------------------------------------------
# 1. PREPROCESS: 12 monthly rows -> 1 row/consumer.
# Aggregation = MEAN across the year: a ratio's yearly mean is each consumer's
# typical monthly behaviour, robust to a single odd month. (Ratios/scores only;
# raw VND excluded per case caveat on inflated synthetic magnitudes.)
# ---------------------------------------------------------------------------
h("1. PREPROCESSING & FEATURE ENGINEERING")
mon = pd.read_csv(MON)

# Feature set spans the 3 required axes. Excluded, with reason:
#  - essential_spend_ratio: = 1 - discretionary (collinear), keep discretionary only.
#  - category_diversity / active_transaction_days / transaction_recency_days:
#    near-constant (75th pct = max), no discriminating signal.
FEATURES = {
    "financial_health_score":    "health",
    "spend_to_income_ratio":     "health",
    "credit_utilization_ratio":  "health",
    "spending_volatility":       "health",
    "engagement_score":          "engagement",
    "transaction_count":         "engagement",
    "discretionary_spend_ratio": "spending",
    "online_spend_ratio":        "spending",
}
feat = list(FEATURES)
cons = mon.groupby("consumer_id")[feat].mean()
# demographics: take first (constant per consumer) for profiling only, not clustering
demo = mon.groupby("consumer_id").agg(age=("age", "first"),
                                      gender=("gender", "first"),
                                      occupation=("occupation", "first"),
                                      province=("province_city", "first"))
print(f"Monthly rows {len(mon):,} -> consumers {len(cons):,}")
print(f"Clustering features ({len(feat)}): {feat}")
print(f"Nulls after aggregation: {int(cons.isnull().sum().sum())}")

X = StandardScaler().fit_transform(cons.values)  # scale before clustering

# ---------------------------------------------------------------------------
# 2. MODEL SELECTION: k-means, pick k via elbow (inertia) + silhouette.
# ---------------------------------------------------------------------------
h("2. MODEL SELECTION - k via elbow + silhouette (k=2..8)")
print(f"{'k':>3} {'inertia':>12} {'silhouette':>12}")
scores = {}
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(X)
    sil = silhouette_score(X, km.labels_)
    scores[k] = (km.inertia_, sil)
    print(f"{k:>3} {km.inertia_:>12.1f} {sil:>12.4f}")

# ponytail: pick k = silhouette winner among business-interpretable range 4-6.
# (k=2/3 win on silhouette but collapse the case's 4-6 personas; we report both.)
best_overall = max(scores, key=lambda k: scores[k][1])
K = max([4, 5, 6], key=lambda k: scores[k][1])
print(f"\nSilhouette winner overall: k={best_overall} ({scores[best_overall][1]:.4f})")
print(f"Chosen k={K} (best silhouette in the interpretable 4-6 range = {scores[K][1]:.4f}) "
      f"- k=2/3 over-collapse the personas the case asks for.")

km = KMeans(n_clusters=K, n_init=25, random_state=SEED).fit(X)
cons["cluster"] = km.labels_
sil_final = silhouette_score(X, km.labels_)

# ---------------------------------------------------------------------------
# 3. VALIDATION: coverage + quality.
# ---------------------------------------------------------------------------
h("3. VALIDATION")
covered = cons["cluster"].notna().sum()
print(f"Coverage: {covered}/999 consumers assigned to exactly one segment "
      f"({'PASS' if covered == 999 else 'FAIL'})")
print(f"Final silhouette (k={K}): {sil_final:.4f}")
print("Cluster sizes:\n" + cons["cluster"].value_counts().sort_index().to_string())

# ---------------------------------------------------------------------------
# 4. PROFILING: mean features per cluster -> business labels.
# ---------------------------------------------------------------------------
h("4. SEGMENT PROFILES (cluster means, unscaled)")
prof = cons.groupby("cluster")[feat].mean()
prof.insert(0, "n", cons["cluster"].value_counts().sort_index())
prof.insert(1, "pct", (100 * prof["n"] / len(cons)).round(1))
gmean = cons[feat].mean()
print("Global means:\n" + gmean.round(3).to_string())
print("\nPer-cluster means:\n" + prof.round(3).to_string())

# Label by each cluster's DEFINING extreme (rank-driven -> always unique).
# The clusters separate on 4 identifiable poles: best health, worst health/most
# stretched, most transactions (power users), least engaged (near-dormant).
labels = {}
labels[prof.financial_health_score.idxmax()]  = "Financially Healthy & Highly Engaged"
labels[prof.spend_to_income_ratio.idxmax()]   = "Financially Stretched but Highly Engaged"
labels[prof.transaction_count.idxmax()]       = "High-Activity Digital Power Users"
labels[prof.engagement_score.idxmin()]        = "Low Engagement & Emerging Digital"
# safety: any cluster the poles missed (collision) gets a fallback so all K are named
for c in prof.index:
    labels.setdefault(c, f"Segment {c} (mixed profile)")
cons["segment"] = cons["cluster"].map(labels)
assert cons["segment"].notna().all() and len(set(labels.values())) == K, "label coverage/uniqueness broke"
print("\nBusiness labels:")
for c in prof.index:
    print(f"  cluster {c}: {labels[c]}  (n={int(prof.loc[c].n)}, {prof.loc[c].pct}%)")

# ---------------------------------------------------------------------------
# 5. RULE-BASED 2x2 CROSS-CHECK (health x engagement on medians) vs k-means.
# ---------------------------------------------------------------------------
h("5. RULE-BASED 2x2 CROSS-CHECK (validation, not the delivered model)")
med_h = cons["financial_health_score"].median()
med_e = cons["engagement_score"].median()
cons["rule2x2"] = np.where(cons.financial_health_score >= med_h,
                    np.where(cons.engagement_score >= med_e, "Healthy+Engaged", "Healthy+Disengaged"),
                    np.where(cons.engagement_score >= med_e, "Stretched+Engaged", "Vulnerable+Disengaged"))
print(f"Split on medians: FHS={med_h:.1f}, engagement={med_e:.1f}")
print("Rule-based 2x2 sizes:\n" + cons["rule2x2"].value_counts().to_string())
print("\nk-means x rule-2x2 crosstab (agreement check):")
print(pd.crosstab(cons["cluster"], cons["rule2x2"]).to_string())

# ---------------------------------------------------------------------------
# 6. SAVE preprocessed feature table + labels (the deliverable).
# ---------------------------------------------------------------------------
out = cons.join(demo)
out.to_csv("draft/task4_features.csv")
print("\nSaved draft/task4_features.csv  ("
      f"{len(out)} rows, {out.shape[1]} cols incl. cluster/segment/demographics)")
print(f"Final coverage recheck: {out['segment'].notna().sum()}/999 labelled.")
