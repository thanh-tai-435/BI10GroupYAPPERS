"""
Task 2 - Financial Health Analysis (BI10 Round 01)
Answers the 4 deliverables with exact numbers. Run: PYTHONUTF8=1 py draft/task2.py
Source: monthly consumer-month file (10,992 rows, 999 consumers). Wellbeing study, NOT credit scoring.
"""
import sys, pandas as pd, numpy as np
sys.stdout.reconfigure(encoding="utf-8")

MON = "BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv"
LOW = 40  # "low health" cutoff (matches Task 1's stressed definition)

def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)

mon = pd.read_csv(MON, parse_dates=["analysis_month"])
mon["month"] = mon["analysis_month"].dt.month

RATIOS = ["spend_to_income_ratio", "credit_utilization_ratio", "essential_spend_ratio",
          "discretionary_spend_ratio", "online_spend_ratio", "spending_volatility",
          "category_diversity", "engagement_score", "transaction_recency_days",
          "average_transaction_value_vnd", "active_transaction_days"]

# Consumer-level frame: mean over the 12 months (stable signal per person).
# ponytail: plain mean aggregation; fine since panel is balanced (~11 mo/consumer).
cons = mon.groupby("consumer_id").agg(
    fhs=("financial_health_score", "mean"),
    age=("age", "first"),
    occupation=("occupation", "first"),
    province=("province_city", "first"),
    engagement=("engagement_score", "mean"),
    **{r: (r, "mean") for r in RATIOS}).reset_index()

# ---------------------------------------------------------------------------
h("Q1 - Distribution of financial_health_score")
c = cons["fhs"]
print("CONSUMER LEVEL (n=%d, mean of each consumer's months)" % len(cons))
print(f"  mean {c.mean():.2f} | median {c.median():.2f} | std {c.std():.2f} | "
      f"min {c.min():.2f} | max {c.max():.2f}")
print(f"  IQR {c.quantile(.25):.2f}-{c.quantile(.75):.2f} | "
      f"skew {c.skew():.3f} (neg = left tail of low-health)")
for q in [5, 10, 25, 50, 75, 90, 95]:
    print(f"    p{q:<2} = {c.quantile(q/100):.2f}")

m = mon["financial_health_score"]
print("\nMONTH LEVEL (n=%d consumer-months)" % len(mon))
print(f"  mean {m.mean():.2f} | median {m.median():.2f} | std {m.std():.2f} | "
      f"min {m.min():.2f} | max {m.max():.2f}")
print("  month-to-month mean FHS:")
print(mon.groupby("month")["financial_health_score"].mean().round(2).to_string())

print("\nSegment shares (financial_health_segment, consumer-months):")
seg = mon["financial_health_segment"].value_counts()
for k, v in seg.items():
    print(f"  {k:<36} {v:>6,} ({100*v/len(mon):5.1f}%)")
print("\n  Consumer-months with FHS < %d: %d (%.1f%%) | FHS >= 80: %d (%.1f%%)"
      % (LOW, (m < LOW).sum(), 100*(m < LOW).mean(), (m >= 80).sum(), 100*(m >= 80).mean()))
print("  Consumers whose 12-mo mean FHS < %d: %d (%.1f%%)"
      % (LOW, (c < LOW).sum(), 100*(c < LOW).mean()))

# ---------------------------------------------------------------------------
h("Q2 - Main factors associated with low health (Pearson corr with FHS)")
# Correlate at month level for maximum n and to catch within-consumer swings.
corr = mon[["financial_health_score"] + RATIOS].corr()["financial_health_score"].drop("financial_health_score")
corr = corr.reindex(corr.abs().sort_values(ascending=False).index)
print("Ranked |correlation| of ratio fields vs financial_health_score (n=%d months):" % len(mon))
for k, v in corr.items():
    print(f"  {v:+.3f}  {k}")
print(f'\n"Low health" defined as FHS < {LOW}.')
lowm, him = mon[mon.financial_health_score < LOW], mon[mon.financial_health_score >= 80]
print(f"  Low (FHS<{LOW}, n={len(lowm)}) vs Healthy (FHS>=80, n={len(him)}) mean of top drivers:")
for f in corr.index[:6]:
    print(f"    {f:<28} low {lowm[f].mean():8.3f} | healthy {him[f].mean():8.3f}")

# ---------------------------------------------------------------------------
h("Q3 - Differences by occupation, age, province (consumer level)")

def grp(col, minn):
    g = cons.groupby(col).agg(n=("fhs", "size"), mean_fhs=("fhs", "mean")).reset_index()
    g = g[g.n >= minn].sort_values("mean_fhs")
    return g

# ponytail: 396 occupations / 999 consumers -> max 10 per group; occupation is unusable as a lever.
print("OCCUPATION: 396 distinct values, max 10 consumers each -> too fragmented to compare.")
occ = grp("occupation", 6)  # >=6 consumers: still tiny, shown only to bound the range
print("  Occupations with >= 6 consumers (samples still tiny, read as noise):")
print(occ.round(2).to_string(index=False))
if len(occ):
    print(f"  range across these: {occ.mean_fhs.max()-occ.mean_fhs.min():.2f} FHS pts "
          f"({occ.iloc[-1].occupation} {occ.iloc[-1].mean_fhs:.1f} vs {occ.iloc[0].occupation} {occ.iloc[0].mean_fhs:.1f})")

print("\nAGE COHORT:")
bins = [14, 24, 34, 44, 54, 64, 200]
labels = ["15-24", "25-34", "35-44", "45-54", "55-64", "65+"]
cons["cohort"] = pd.cut(cons.age, bins=bins, labels=labels)
age = cons.groupby("cohort", observed=True).agg(n=("fhs", "size"), mean_fhs=("fhs", "mean")).round(2)
print(age.to_string())
print(f"  spread best-worst: {age.mean_fhs.max()-age.mean_fhs.min():.2f} FHS pts")

print("\nPROVINCE (only >= 15 consumers):")
prov = grp("province", 15)
print(prov.round(2).to_string(index=False))
print(f"  spread best-worst: {prov.mean_fhs.max()-prov.mean_fhs.min():.2f} FHS pts")
print(f"\n  National consumer-mean FHS = {cons.fhs.mean():.2f}, std across consumers = {cons.fhs.std():.2f}")

# ---------------------------------------------------------------------------
h("Q4 - Crossover: financially stressed BUT highly engaged")
# KEY: no consumer is CHRONICALLY stressed (min 12-mo mean FHS = %.2f). Stress is EPISODIC,
# so the crossover only exists at the consumer-MONTH grain. Rule applied there.
print("Note: 0 consumers have a 12-mo mean FHS < %d (min = %.2f) -> stress is episodic, "
      "not a stable trait." % (LOW, cons.fhs.min()))
eng_p75 = mon.engagement_score.quantile(0.75)
print(f"Rule (consumer-month grain): financial_health_score < {LOW} AND "
      f"engagement_score >= p75 ({eng_p75:.2f}).")
crossm = mon[(mon.financial_health_score < LOW) & (mon.engagement_score >= eng_p75)]
stressedm = mon[mon.financial_health_score < LOW]
print(f"  Stressed consumer-months (FHS<{LOW}): {len(stressedm)} "
      f"({stressedm.consumer_id.nunique()} distinct consumers)")
print(f"  CROSSOVER (stressed + high engagement): {len(crossm)} consumer-months "
      f"= {crossm.consumer_id.nunique()} distinct consumers "
      f"({100*crossm.consumer_id.nunique()/999:.1f}% of 999 consumers; "
      f"{100*len(crossm)/max(len(stressedm),1):.0f}% of stressed months)")
print("\nProfile (crossover-months vs all consumer-months, means):")
prof = ["financial_health_score", "engagement_score", "spend_to_income_ratio",
        "credit_utilization_ratio", "essential_spend_ratio", "discretionary_spend_ratio",
        "online_spend_ratio", "spending_volatility", "category_diversity",
        "active_transaction_days", "transaction_count"]
for f in prof:
    print(f"  {f:<28} crossover {crossm[f].mean():9.3f} | all {mon[f].mean():9.3f}")
print(f"\n  Crossover age mean {crossm.age.mean():.1f} vs all {mon.age.mean():.1f}")
print("  Crossover cohort mix (consumer-months):")
print(pd.cut(crossm.age, bins=bins, labels=labels).value_counts().sort_index().to_string())

# self-check: crossover must be a subset of stressed
assert set(crossm.index) <= set(stressedm.index), "crossover not subset of stressed"
print("\n[self-check OK] crossover ⊆ stressed (month grain)")
