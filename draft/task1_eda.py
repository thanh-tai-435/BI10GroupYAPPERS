"""
Task 1 - Exploratory Data Analysis (BI10 Round 01)
Answers EDA Q1-Q5 with exact numbers. Run: py draft/task1_eda.py
Sources: monthly consumer file + transaction-level file.
"""
import sys, pandas as pd, numpy as np
sys.stdout.reconfigure(encoding="utf-8")

DATA = "BI10_ROUND01_DATASET"
TXN = f"{DATA}/consumer_transactions_2025.parquet/consumer_transactions_2025.csv"
MON = f"{DATA}/consumer_financial_health_engagement_2025.csv"

def vnd(x):  # human-readable VND
    for u, d in [("T", 1e12), ("B", 1e9), ("M", 1e6)]:
        if abs(x) >= d:
            return f"{x/d:,.2f}{u} VND"
    return f"{x:,.0f} VND"

def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)

mon = pd.read_csv(MON, parse_dates=["analysis_month"])
mon["month"] = mon["analysis_month"].dt.month

# Transactions: load only what each question needs (keeps memory sane).
txn = pd.read_csv(TXN, usecols=[
    "transaction_month", "spend_amount_vnd", "transaction_channel",
    "spending_category", "province_city", "essential_spending_flag"])
txn["digital"] = txn["transaction_channel"].ne("POS")

# ----------------------------------------------------------------------------
h("Q1 - Peak vs trough month: driver = count or ticket?")
g = txn.groupby("transaction_month")["spend_amount_vnd"].agg(["sum", "count"])
g["avg_ticket"] = g["sum"] / g["count"]
annual = g["sum"].sum()
g["pct_annual"] = 100 * g["sum"] / annual
peak, trough = g["sum"].idxmax(), g["sum"].idxmin()
print(g.round(0).to_string())
print(f"\nAnnual total spend: {vnd(annual)}")
p, t = g.loc[peak], g.loc[trough]
print(f"PEAK  month {peak}: {vnd(p['sum'])} ({p['pct_annual']:.2f}% of annual) | "
      f"{int(p['count']):,} txns | ticket {vnd(p['avg_ticket'])}")
print(f"TROUGH month {trough}: {vnd(t['sum'])} ({t['pct_annual']:.2f}% of annual) | "
      f"{int(t['count']):,} txns | ticket {vnd(t['avg_ticket'])}")
print(f"Peak vs trough: spend +{100*(p['sum']/t['sum']-1):.1f}%, "
      f"count +{100*(p['count']/t['count']-1):.1f}%, "
      f"ticket {100*(p['avg_ticket']/t['avg_ticket']-1):+.1f}%")
print("-> Driver = TRANSACTION COUNT" if (p['count']/t['count']) > (p['avg_ticket']/t['avg_ticket'])
      else "-> Driver = TICKET SIZE")

# ----------------------------------------------------------------------------
h("Q2 - Essential vs Discretionary: stressed (FHS<40) vs healthy (FHS>=80)")
def compo(df):
    e, d = df["essential_spend_vnd"].sum(), df["discretionary_spend_vnd"].sum()
    tot = e + d
    return e, d, 100 * e / tot, 100 * d / tot
for label, sub in [("Stressed  (FHS<40) ", mon[mon.financial_health_score < 40]),
                   ("Healthy   (FHS>=80)", mon[mon.financial_health_score >= 80])]:
    n = len(sub); cust = sub.consumer_id.nunique()
    e, d, ep, dp = compo(sub)
    print(f"{label}: {n:,} consumer-months / {cust} consumers | "
          f"Essential {ep:.1f}% | Discretionary {dp:.1f}% | "
          f"mean essential_spend_ratio {sub.essential_spend_ratio.mean():.3f}")

# ----------------------------------------------------------------------------
h("Q3 - High-spend provinces with below-average digital share")
prov = txn.groupby("province_city").agg(
    total_spend=("spend_amount_vnd", "sum"),
    txns=("spend_amount_vnd", "count"),
    digital_txns=("digital", "sum")).reset_index()
prov["digital_share"] = 100 * prov["digital_txns"] / prov["txns"]
prov["pos_share"] = 100 - prov["digital_share"]
avg_digital = 100 * txn["digital"].sum() / len(txn)
spend_median = prov["total_spend"].median()
print(f"National digital txn share: {avg_digital:.1f}%  (POS {100-avg_digital:.1f}%)")
target = prov[(prov.total_spend > spend_median) & (prov.digital_share < avg_digital)] \
    .sort_values("total_spend", ascending=False)
print(f"\nHigh-spend (> median {vnd(spend_median)}) AND digital < national avg:")
for _, r in target.head(6).iterrows():
    print(f"  {r.province_city:<18} spend {vnd(r.total_spend):>14} | "
          f"digital {r.digital_share:5.1f}% | POS {r.pos_share:5.1f}% | "
          f"gap {r.digital_share-avg_digital:+.1f}pp")

# ----------------------------------------------------------------------------
h("Q4 - Top category by count vs by spend; ticket comparison")
cat = txn.groupby("spending_category")["spend_amount_vnd"].agg(["sum", "count"])
cat["avg_ticket"] = cat["sum"] / cat["count"]
top_cnt = cat["count"].idxmax(); top_spend = cat["sum"].idxmax()
print(cat.sort_values("sum", ascending=False).round(0).to_string())
c, s = cat.loc[top_cnt], cat.loc[top_spend]
print(f"\nTop by COUNT: {top_cnt} -> {int(c['count']):,} txns, ticket {vnd(c['avg_ticket'])}")
print(f"Top by SPEND: {top_spend} -> {vnd(s['sum'])}, ticket {vnd(s['avg_ticket'])}")
print(f"Ticket ratio (spend-leader / count-leader): {s['avg_ticket']/c['avg_ticket']:.1f}x")

# ----------------------------------------------------------------------------
h("Q5 - Age cohort: active but lowest financial health")
bins = [14, 24, 34, 44, 54, 64, 200]  # min age is 15; start at 14 so all 999 consumers are covered
labels = ["15-24", "25-34", "35-44", "45-54", "55-64", "65+"]
mon["cohort"] = pd.cut(mon.age, bins=bins, labels=labels)
coh = mon.groupby("cohort", observed=True).agg(
    consumers=("consumer_id", "nunique"),
    avg_fhs=("financial_health_score", "mean"),
    avg_txn=("transaction_count", "mean"),
    avg_active_days=("active_transaction_days", "mean"),
    ess_ratio=("essential_spend_ratio", "mean"),
    spend_to_income=("spend_to_income_ratio", "mean")).round(3)
print(coh.to_string())
active_med = coh["avg_txn"].median()
vuln = coh[coh.avg_txn >= active_med].sort_values("avg_fhs").head(1)
name = vuln.index[0]
print(f"\nMost vulnerable (active but lowest FHS): cohort {name}")
print(f"  avg FHS {vuln.avg_fhs.iloc[0]:.1f} vs cohort best {coh.avg_fhs.max():.1f} | "
      f"txns {vuln.avg_txn.iloc[0]:.1f} | ess_ratio {vuln.ess_ratio.iloc[0]:.3f} | "
      f"spend/income {vuln.spend_to_income.iloc[0]:.3f}")
print(f"  National mean spend/income {mon.spend_to_income_ratio.mean():.3f}, "
      f"ess_ratio {mon.essential_spend_ratio.mean():.3f}")
