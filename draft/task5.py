# Task 5 - recompute/verify every group size used in recommendations.
# ponytail: pure verification, no abstractions. Two CSVs + task4_features.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd

MONTH = "BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv"
FEAT  = "draft/task4_features.csv"

m = pd.read_csv(MONTH)
f = pd.read_csv(FEAT)
N = f["consumer_id"].nunique()
def pct(n): return f"{n} ({100*n/N:.1f}%)"

print(f"Base: {N} consumers | {len(m)} consumer-months\n")

# --- Task 4 segments (the sizing backbone for reach) ---
print("=== T4 segments (consumer level) ===")
seg = f["segment"].value_counts()
for name, n in seg.items():
    print(f"  {name}: {pct(n)}")
print()

# --- T2 crossover: stressed AND highly engaged, MONTH grain ---
p75 = m["engagement_score"].quantile(0.75)
stressed_m = m[m["financial_health_score"] < 40]
cross_m = stressed_m[stressed_m["engagement_score"] >= p75]
print("=== T2 crossover (Stressed & Engaged), month grain ===")
print(f"  engagement p75 = {p75:.2f}")
print(f"  stressed consumer-months (FHS<40): {len(stressed_m)} ({stressed_m['consumer_id'].nunique()} distinct)")
print(f"  crossover consumer-months: {len(cross_m)}")
print(f"  crossover distinct consumers: {pct(cross_m['consumer_id'].nunique())}")
print(f"  share of all stress months: {100*len(cross_m)/len(stressed_m):.0f}%\n")

# --- T3 dormant good customers: consumer-level FHS>=70 AND eng<70 ---
print("=== T3 dormant good (FHS>=70 & eng<70), consumer level ===")
dorm = f[(f["financial_health_score"] >= 70) & (f["engagement_score"] < 70)]
print(f"  {pct(len(dorm))}\n")

# --- T3 distress tail: consumer-level FHS<70... actually low-health & low-eng ---
# T3 stated: 67 low-health/low-engagement (eng<70 & health<70)
print("=== T3 distress tail (FHS<70 & eng<70), consumer level ===")
distress = f[(f["financial_health_score"] < 70) & (f["engagement_score"] < 70)]
print(f"  {pct(len(distress))}\n")

# --- 25-34 cohort (Task 1 vulnerability) ---
print("=== Age 25-34 cohort ===")
c2534 = f[(f["age"] >= 25) & (f["age"] <= 34)]
print(f"  {pct(len(c2534))}\n")

# --- Fairness check: segment 2 (wellbeing target) not skewed by geo/age/gender ---
print("=== Fairness: Stretched segment vs base (age/gender/top provinces) ===")
stretch = f[f["segment"] == "Financially Stretched but Highly Engaged"]
print(f"  Stretched n={len(stretch)}  mean age {stretch['age'].mean():.1f} vs base {f['age'].mean():.1f}")
print(f"  gender mix stretched: {stretch['gender'].value_counts(normalize=True).round(3).to_dict()}")
print(f"  gender mix base:      {f['gender'].value_counts(normalize=True).round(3).to_dict()}")
# province representation ratio (share in stretched / share in base) for top provinces
base_prov = f["province"].value_counts(normalize=True)
str_prov = stretch["province"].value_counts(normalize=True)
rep = (str_prov / base_prov).dropna().sort_values(ascending=False)
print("  province over/under-representation (stretched share / base share), top provinces (base n>=15):")
big = f["province"].value_counts()
for prov in big[big >= 15].index:
    if prov in rep.index:
        print(f"    {prov} (base n={big[prov]}): {rep[prov]:.2f}x")

# assert internal consistency
assert len(m) == 10992 and N == 999
assert cross_m['consumer_id'].nunique() == 43, cross_m['consumer_id'].nunique()
assert len(dorm) == 25, len(dorm)
print("\nOK all assertions passed.")
