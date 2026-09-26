"""
Task 3 - Customer Engagement Analysis (BI10 Round 01)
Answers the six deliverables with exact numbers. Run: PYTHONUTF8=1 py draft/task3.py
Sources: monthly consumer-month file (engagement/ratios) + transaction-level file (channel).
"""
import sys, pandas as pd, numpy as np
sys.stdout.reconfigure(encoding="utf-8")

DATA = "BI10_ROUND01_DATASET"
TXN = f"{DATA}/consumer_transactions_2025.parquet/consumer_transactions_2025.csv"
MON = f"{DATA}/consumer_financial_health_engagement_2025.csv"

def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)

mon = pd.read_csv(MON, usecols=[
    "consumer_id", "engagement_score", "engagement_segment", "category_diversity",
    "transaction_recency_days", "transaction_count", "active_transaction_days",
    "online_spend_ratio", "financial_health_score", "financial_health_segment"])

# ponytail: consumer-level = mean of each consumer's months. Grain differs per Q so
# both are reported; consumer-level is the "customer base" view (999 people, 1 vote each).
con = mon.groupby("consumer_id").mean(numeric_only=True)
N = len(con)
print(f"Rows(consumer-months)={len(mon):,}  consumers={N}")

# ----------------------------------------------------------------------------
h("Q1 - Engagement score distribution + segment shares")
es = mon["engagement_score"]
print("engagement_score (consumer-month):")
print(es.describe().round(2).to_string())
print(f"consumer-level mean engagement: {con['engagement_score'].mean():.2f}, "
      f"median {con['engagement_score'].median():.2f}, "
      f"min {con['engagement_score'].min():.2f}, max {con['engagement_score'].max():.2f}")
print("\nSegment share (consumer-months):")
seg = mon["engagement_segment"].value_counts()
for k, v in seg.items():
    print(f"  {k:<24} {v:>6,}  {100*v/len(mon):5.1f}%")
# consumer-level: assign each consumer their most-frequent (modal) segment
modal = mon.groupby("consumer_id")["engagement_segment"].agg(lambda s: s.mode().iloc[0])
print("\nSegment share (consumers, modal segment):")
for k, v in modal.value_counts().items():
    print(f"  {k:<24} {v:>4}  {100*v/N:5.1f}%")

# ----------------------------------------------------------------------------
h("Q2 - Channel adoption breakdown + online spend share")
ch = pd.read_csv(TXN, usecols=["transaction_channel"])["transaction_channel"].value_counts()
tot = ch.sum()
print(f"Total transactions: {tot:,}")
for k, v in ch.items():
    print(f"  {k:<18} {v:>10,}  {100*v/tot:5.1f}%")
print(f"\nAvg online_spend_ratio (consumer-month): {mon['online_spend_ratio'].mean():.4f} "
      f"({100*mon['online_spend_ratio'].mean():.1f}%)")
print(f"Avg online_spend_ratio (consumer-level):  {con['online_spend_ratio'].mean():.4f} "
      f"({100*con['online_spend_ratio'].mean():.1f}%)")
print(f"online_spend_ratio range (consumer-level): "
      f"{con['online_spend_ratio'].min():.3f} - {con['online_spend_ratio'].max():.3f}")

# ----------------------------------------------------------------------------
h("Q3 - Category diversity range + link to engagement")
cd = mon["category_diversity"]
print(f"category_diversity (consumer-month): min {cd.min()}, max {cd.max()}, "
      f"mean {cd.mean():.2f}, median {cd.median()}")
print(f"category_diversity (consumer-level): min {con['category_diversity'].min():.2f}, "
      f"max {con['category_diversity'].max():.2f}, mean {con['category_diversity'].mean():.2f}")
r = mon[["category_diversity", "engagement_score"]].corr().iloc[0, 1]
rc = con[["category_diversity", "engagement_score"]].corr().iloc[0, 1]
print(f"corr(category_diversity, engagement_score): {r:.3f} (month), {rc:.3f} (consumer)")
print("\nMean category_diversity by engagement_segment (consumer-months):")
gd = mon.groupby("engagement_segment").agg(
    n=("category_diversity", "size"),
    mean_diversity=("category_diversity", "mean"),
    mean_engagement=("engagement_score", "mean")).round(2).sort_values("mean_engagement")
print(gd.to_string())

# ----------------------------------------------------------------------------
h("Q4 - Recency & frequency ranges + link to engagement")
for c in ["transaction_recency_days", "transaction_count", "active_transaction_days"]:
    s = mon[c]
    print(f"{c:<26} min {s.min():>6.1f} | median {s.median():>7.1f} | "
          f"mean {s.mean():>7.1f} | max {s.max():>7.1f}")
mon["txn_per_active_day"] = mon["transaction_count"] / mon["active_transaction_days"].replace(0, np.nan)
print(f"{'txn_per_active_day':<26} min {mon.txn_per_active_day.min():>6.2f} | "
      f"median {mon.txn_per_active_day.median():>7.2f} | mean {mon.txn_per_active_day.mean():>7.2f} | "
      f"max {mon.txn_per_active_day.max():>7.2f}")
print("\nCorrelation with engagement_score (consumer-month):")
for c in ["transaction_recency_days", "transaction_count", "active_transaction_days", "txn_per_active_day"]:
    print(f"  {c:<26} {mon[[c,'engagement_score']].corr().iloc[0,1]:+.3f}")
print("\nMeans by engagement_segment (consumer-months):")
gf = mon.groupby("engagement_segment").agg(
    recency=("transaction_recency_days", "mean"),
    txn_count=("transaction_count", "mean"),
    active_days=("active_transaction_days", "mean"),
    engagement=("engagement_score", "mean")).round(2).sort_values("engagement")
print(gf.to_string())

# ----------------------------------------------------------------------------
h("Q5 - High-health, low-engagement group (retention/growth risk)")
# Cutoff picked on consumer-level distribution (each customer = 1 vote).
he, ee = con["financial_health_score"], con["engagement_score"]
print("Percentiles to justify cutoff (consumer-level):")
print(f"  engagement    p10 {ee.quantile(.10):.1f} p25 {ee.quantile(.25):.1f} "
      f"median {ee.median():.1f} p75 {ee.quantile(.75):.1f}")
print(f"  health        p25 {he.quantile(.25):.1f} median {he.median():.1f} "
      f"p75 {he.quantile(.75):.1f} p90 {he.quantile(.90):.1f}")
# CUTOFF: high health = FHS >= 70 ; low engagement = engagement < 70
HI_H, LO_E = 70, 70
grp = con[(con.financial_health_score >= HI_H) & (con.engagement_score < LO_E)]
print(f"\nCUTOFF: financial_health_score >= {HI_H} (high) AND engagement_score < {LO_E} (low)")
print(f"Group size: {len(grp)} consumers ({100*len(grp)/N:.1f}% of {N})")
# sensitivity: show how the count moves at stricter/looser engagement cutoffs
for lo in [65, 68, 70, 72, 74]:
    g = con[(con.financial_health_score >= HI_H) & (con.engagement_score < lo)]
    print(f"  sensitivity: FHS>=70 & eng<{lo}: {len(g)} consumers ({100*len(g)/N:.1f}%)")
print("\nProfile of the group vs rest of base (consumer-level means):")
rest = con.drop(grp.index)
prof = pd.DataFrame({
    "group": grp.mean(numeric_only=True),
    "rest": rest.mean(numeric_only=True)}).round(3)
prof = prof.loc[["financial_health_score", "engagement_score", "category_diversity",
                 "online_spend_ratio", "transaction_count", "active_transaction_days",
                 "transaction_recency_days"]]
print(prof.to_string())
