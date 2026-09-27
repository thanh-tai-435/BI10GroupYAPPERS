"""Independent recomputation of every number on deck slides 5-8 (Task 1 EDA).
Run: PYTHONUTF8=1 py draft/review/t1_verify.py
"""
import sys
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
D = "BI10_ROUND01_DATASET/"
m = pd.read_csv(D + "consumer_financial_health_engagement_2025.csv")
t = pd.read_csv(D + "consumer_transactions_2025.parquet/consumer_transactions_2025.csv",
                usecols=["consumer_id", "activity_datetime", "province_city", "spending_category",
                         "spend_amount_vnd", "transaction_channel", "online_transaction_flag",
                         "essential_spending_flag", "transaction_month"])
B = 1e9
print("rows", len(m), m.consumer_id.nunique(), len(t))
print("years in timestamps:", pd.to_datetime(t.activity_datetime).dt.year.unique())

# ---------------- Q1 ----------------
print("\n== Q1 ==")
mo = t.groupby("transaction_month").agg(spend=("spend_amount_vnd", "sum"), n=("spend_amount_vnd", "size"),
                                        consumers=("consumer_id", "nunique"))
mo["ticket"] = mo.spend / mo.n
mo["share"] = mo.spend / mo.spend.sum() * 100
mo["days"] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
mo["spend_per_day_B"] = mo.spend / mo.days / B
mo["txn_per_consumer"] = mo.n / mo.consumers
print(mo.assign(spend_B=mo.spend / B).round(3).to_string())
print("annual T", mo.spend.sum() / 1e12)
pk, lo = mo.spend.idxmax(), mo.spend.idxmin()
P, L = mo.loc[pk], mo.loc[lo]
print("peak", pk, "low", lo, "ratio", P.spend / L.spend, "diff B", (P.spend - L.spend) / B,
      "share pp diff", P.share - L.share)
print("count chg %", (P.n / L.n - 1) * 100, "ticket chg %", (P.ticket / L.ticket - 1) * 100)
# log decomposition of spend ratio into count and ticket
lr = np.log(P.spend / L.spend)
print("log share count", np.log(P.n / L.n) / lr, "ticket", np.log(P.ticket / L.ticket) / lr)
# count = consumers x txn per consumer
print("active consumers chg %", (P.consumers / L.consumers - 1) * 100,
      "txn/consumer chg %", (P.txn_per_consumer / L.txn_per_consumer - 1) * 100)
print("per-day spend ratio", P.spend_per_day_B / L.spend_per_day_B)
# vs mean of other months
oth = mo.drop(pk)
print("Dec vs avg other month: spend x", P.spend / oth.spend.mean(), "count x", P.n / oth.n.mean(),
      "ticket chg %", (P.ticket / (oth.spend.sum() / oth.n.sum()) - 1) * 100)
cat = t[t.transaction_month.isin([pk, lo])].pivot_table(index="spending_category", columns="transaction_month",
                                                        values="spend_amount_vnd", aggfunc=["size", "sum"])
g = (cat[("size", pk)] / cat[("size", lo)] - 1) * 100
gs = (cat[("sum", pk)] / cat[("sum", lo)] - 1) * 100
print("n categories", len(g), "count growth range", g.min(), g.max(), "spend growth range", gs.min(), gs.max())
inc = cat[("size", pk)] - cat[("size", lo)]
print("added txns", inc.sum(), "largest contributor", inc.idxmax(), inc.max() / inc.sum() * 100)
# Nov->Dec and Dec vs Jan-Nov monthly file check
print("monthly-file total spend matches txns:", abs(m.total_spend_vnd.sum() - t.spend_amount_vnd.sum()) < 1)
m["month"] = pd.to_datetime(m.analysis_month).dt.month
print("consumer-months by month:\n", m.groupby("month").size().to_string())
print("mean FHS by month:\n", m.groupby("month").financial_health_score.mean().round(1).to_string())

# ---------------- Q2 ----------------
print("\n== Q2 ==")
def comp(mask, lab):
    s = m[mask]
    ess = s.essential_spend_vnd.sum() / s.total_spend_vnd.sum() * 100
    print(f"{lab}: months {len(s)} consumers {s.consumer_id.nunique()} ess {ess:.2f} disc {100-ess:.2f}"
          f" | mean-of-ratios ess {s.essential_spend_ratio.mean()*100:.2f}"
          f" | spend/inc median {s.spend_to_income_ratio.median():.2f} mean {s.spend_to_income_ratio.mean():.2f}")
f = m.financial_health_score
comp(f < 40, "stressed<40"); comp(f >= 80, "healthy>=80")
comp(f < 35, "<35"); comp(f >= 85, ">=85"); comp(f < 50, "<50"); comp(f >= 70, ">=70")
for lo_, hi_ in [(0, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 101)]:
    comp((f >= lo_) & (f < hi_), f"band {lo_}-{hi_}")
comp(f.notna(), "all")
print("spearman FHS vs disc ratio", m[["financial_health_score", "discretionary_spend_ratio"]].corr("spearman").iloc[0, 1])
# transaction-level cross-check of essential share via flag
tm = t.assign(month=t.transaction_month).merge(m[["consumer_id", "month", "financial_health_score"]],
                                               on=["consumer_id", "month"])
for lab, msk in [("stressed", tm.financial_health_score < 40), ("healthy", tm.financial_health_score >= 80)]:
    s = tm[msk]
    print(lab, "txn-flag essential value share", s.spend_amount_vnd[s.essential_spending_flag == 1].sum() / s.spend_amount_vnd.sum() * 100,
          "essential count share", s.essential_spending_flag.mean() * 100)
# which categories absorb the discretionary shift (value share by category)
cs = tm.assign(seg=np.select([tm.financial_health_score < 40, tm.financial_health_score >= 80], ["S", "H"], "M"))
cs = cs[cs.seg != "M"].pivot_table(index="spending_category", columns="seg", values="spend_amount_vnd", aggfunc="sum")
cs = cs / cs.sum() * 100
cs["diff"] = cs.S - cs.H
ess_cat = t.groupby("spending_category").essential_spending_flag.mean()
cs["ess"] = ess_cat
print(cs.sort_values("diff").round(2).to_string())

# ---------------- Q3 ----------------
print("\n== Q3 ==")
t["digital"] = (t.transaction_channel != "POS").astype(int)
print("channels:", t.transaction_channel.value_counts(normalize=True).mul(100).round(2).to_dict())
print("online flag == non-POS?", (t.digital == t.online_transaction_flag).mean())
nat_d = t.digital.mean() * 100
nat_dv = t.spend_amount_vnd[t.digital == 1].sum() / t.spend_amount_vnd.sum() * 100
print("national digital txn share", nat_d, "value share", nat_dv)
pv = t.groupby("province_city").agg(spend=("spend_amount_vnd", "sum"), n=("digital", "size"), dig=("digital", "mean"))
pv["dig_val"] = t[t.digital == 1].groupby("province_city").spend_amount_vnd.sum() / pv.spend * 100
pv["dig"] *= 100
pv["spend_share"] = pv.spend / pv.spend.sum() * 100
pv["gap_pp"] = pv.dig - nat_d
pv["z"] = pv.gap_pp / 100 / np.sqrt(nat_d / 100 * (1 - nat_d / 100) / pv.n)
ch = pd.crosstab(t.province_city, t.transaction_channel, normalize="index") * 100
pv = pv.join(ch)
pv = pv.sort_values("spend", ascending=False)
print("n provinces", len(pv), "median spend B", pv.spend.median() / B)
print(pv.assign(spend=pv.spend / B).round(2).to_string())
sel = pv[(pv.spend > pv.spend.median()) & (pv.dig < nat_d)]
print("\nSELECTED (above-median spend & below-avg digital):")
print(sel.assign(spend=sel.spend / B).round(2).to_string())
print("national channel mix", ch.columns.tolist(), t.transaction_channel.value_counts(normalize=True).mul(100).round(2).to_dict())
print("digital range across provinces", pv.dig.min(), pv.dig.idxmin(), pv.dig.max(), pv.dig.idxmax(), "spread", pv.dig.max() - pv.dig.min())
# top-10 by spend alternative definition
t10 = pv.head(10)
print("top10 by spend below avg digital:", t10[t10.dig < nat_d].index.tolist())
# chi-square: selected provinces' pooled digital vs rest
from scipy.stats import chi2_contingency
tab = pd.crosstab(t.province_city.isin(sel.index), t.digital)
print("chi2 selected vs rest p=", chi2_contingency(tab)[1], "pooled sel digital", t[t.province_city.isin(sel.index)].digital.mean() * 100)
tab2 = pd.crosstab(t.province_city, t.digital)
print("chi2 across all 34 provinces p=", chi2_contingency(tab2)[1])
# consumer-level digital share variation (what IS the lever?)
cd = t.groupby("consumer_id").digital.mean() * 100
print("consumer digital share p10/p50/p90", cd.quantile([.1, .5, .9]).round(1).to_dict(), "range", cd.min(), cd.max())
print("consumers per province min/max", t.groupby("province_city").consumer_id.nunique().agg(["min", "max"]).to_dict())

# ---------------- Q4 ----------------
print("\n== Q4 ==")
c = t.groupby("spending_category").agg(n=("spend_amount_vnd", "size"), spend=("spend_amount_vnd", "sum"),
                                       ess=("essential_spending_flag", "mean"), consumers=("consumer_id", "nunique"))
c["ticket_M"] = c.spend / c.n / 1e6
c["n_share"] = c.n / c.n.sum() * 100
c["spend_share"] = c.spend / c.spend.sum() * 100
c["reach"] = c.consumers / t.consumer_id.nunique() * 100
bm = t.groupby(["spending_category", "consumer_id", "transaction_month"]).size()
c["per_buyer_month"] = bm.groupby(level=0).mean()
c["months_per_buyer"] = bm.groupby(level=[0, 1]).size().groupby(level=0).mean()
c["median_ticket_M"] = t.groupby("spending_category").spend_amount_vnd.median() / 1e6
print(c.assign(spend=c.spend / B).sort_values("n", ascending=False).round(3).to_string())
print("overall avg ticket M", t.spend_amount_vnd.mean() / 1e6)
tc, ts = c.n.idxmax(), c.spend.idxmax()
print("top count", tc, "top spend", ts, "ticket ratio", c.loc[ts, "ticket_M"] / c.loc[tc, "ticket_M"])

# ---------------- Q5 ----------------
print("\n== Q5 ==")
bins = [0, 24, 34, 44, 54, 64, 200]
labs = ["15-24", "25-34", "35-44", "45-54", "55-64", "65+"]
print("min age", m.age.min(), "ages vary within consumer?", (m.groupby("consumer_id").age.nunique() > 1).sum())
m["cohort"] = pd.cut(m.age, bins, labels=labs)
# consumer-level cohort by first-month age
first_age = m.sort_values("month").groupby("consumer_id").age.first()
m["cohort_c"] = m.consumer_id.map(pd.cut(first_age, bins, labels=labs))
for col in ["cohort", "cohort_c"]:
    q = m.groupby(col, observed=True).agg(consumers=("consumer_id", "nunique"), fhs=("financial_health_score", "mean"),
                                          txn=("transaction_count", "mean"), ess=("essential_spend_ratio", "mean"),
                                          sti=("spend_to_income_ratio", "mean"), sti_med=("spend_to_income_ratio", "median"),
                                          disc=("discretionary_spend_ratio", "mean"), cu=("credit_utilization_ratio", "mean"),
                                          stress_rate=("financial_health_score", lambda s: (s < 40).mean() * 100),
                                          days=("active_transaction_days", "mean"))
    print(col); print(q.round(3).to_string())
    print("median of cohort txn means", q.txn.median())
print("national: fhs", m.financial_health_score.mean(), "ess", m.essential_spend_ratio.mean(),
      "sti", m.spend_to_income_ratio.mean(), "txn", m.transaction_count.mean(), "cu", m.credit_utilization_ratio.mean())
# consumer-level bootstrap CI of mean FHS by cohort (first-age cohort)
cons = m.groupby("consumer_id").agg(fhs=("financial_health_score", "mean"), coh=("cohort_c", "first"))
rng = np.random.default_rng(0)
cis = {}
for k, g_ in cons.groupby("coh", observed=True).fhs:
    v = g_.values
    bs = rng.choice(v, (5000, len(v))).mean(1)
    cis[k] = (v.mean(), *np.percentile(bs, [2.5, 97.5]), len(v))
print(pd.DataFrame(cis, index=["mean", "lo", "hi", "n"]).T.round(2).to_string())
from scipy.stats import f_oneway, kruskal
print("ANOVA consumer FHS by cohort p=", f_oneway(*[g_.values for _, g_ in cons.groupby("coh", observed=True).fhs]).pvalue)
print("stressed-month share by cohort already above; overall", (m.financial_health_score < 40).mean() * 100)
