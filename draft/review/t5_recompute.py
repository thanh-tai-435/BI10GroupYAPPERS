# Independent recompute of every number on deck slides 19-21 (Task 5). Run: PYTHONUTF8=1 py draft/review/t5_recompute.py
import sys; sys.stdout.reconfigure(encoding="utf-8")
import numpy as np, pandas as pd
from scipy.stats import chi2_contingency
M = pd.read_csv("BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv")
F = pd.read_csv("draft/task4_features.csv").set_index("consumer_id")
N = len(F); assert N == 999 and len(M) == 10992
SEG = {"Financially Healthy & Highly Engaged": "Healthy", "Financially Stretched but Highly Engaged": "Stretched",
       "High-Activity Digital Power Users": "Power", "Low Engagement & Emerging Digital": "Emerging"}
F["seg"] = F.segment.map(SEG)
def h(t): print(f"\n=== {t} ===")

h("segments"); print(F.seg.value_counts().to_dict())
print(F.groupby("seg")[["spend_to_income_ratio", "credit_utilization_ratio", "financial_health_score",
      "spending_volatility", "engagement_score", "transaction_count", "online_spend_ratio", "discretionary_spend_ratio"]].mean().round(3).to_string())

h("crossover / tails")
p75 = M.engagement_score.quantile(.75); st = M[M.financial_health_score < 40]; cr = st[st.engagement_score >= p75]
X = set(cr.consumer_id)
print(f"p75 {p75:.2f} | stress months {len(st)} ({st.consumer_id.nunique()} consumers) | crossover months {len(cr)} = {100*len(cr)/len(st):.1f}% | consumers {len(X)}")
D = set(F[(F.financial_health_score < 70) & (F.engagement_score < 70)].index)
Dm = set(F[(F.financial_health_score >= 70) & (F.engagement_score < 70)].index)
print(f"distress {len(D)} | dormant-healthy {len(Dm)} | crossover&distress {len(X & D)}")
for name, ids in [("crossover", X), ("distress", D), ("dormant", Dm)]:
    print(f"  {name} by segment:", F.loc[list(ids), "seg"].value_counts().to_dict())
print("stress months by segment:", st.consumer_id.map(F.seg).value_counts().to_dict())
print("stress consumers by segment:", F.loc[st.consumer_id.unique(), "seg"].value_counts().to_dict())

h("drivers: month-level r with FHS")
cols = ["spend_to_income_ratio", "credit_utilization_ratio", "spending_volatility", "essential_spend_ratio",
        "discretionary_spend_ratio", "online_spend_ratio", "category_diversity", "engagement_score", "transaction_count"]
print(M[cols + ["financial_health_score"]].corr()["financial_health_score"].round(3).to_string())
C = M.groupby("consumer_id")[cols + ["financial_health_score"]].mean()
print("consumer-level r with FHS:\n", C.corr()["financial_health_score"].round(3).to_string())
print(f"r(diversity, engagement) month {M.category_diversity.corr(M.engagement_score):.3f} consumer {C.category_diversity.corr(C.engagement_score):.3f}")
state = pd.Series(np.select([M.financial_health_score < 40, M.financial_health_score >= 80], ["stressed", "healthy"], "mid"), index=M.index)
print("mean discretionary ratio by state:", (100 * M.groupby(state).discretionary_spend_ratio.mean()).round(1).to_dict())

h("regression + scenario")
b, a = np.polyfit(M.spend_to_income_ratio, M.financial_health_score, 1)
print(f"FHS = {a:.2f} {b:+.2f} x STI, r {M.spend_to_income_ratio.corr(M.financial_health_score):.3f}")
isS = M.consumer_id.map(F.seg).eq("Stretched")
for cut in (0, .05, .10, .15):
    new = M.financial_health_score - b * M.spend_to_income_ratio * cut * isS
    print(f"  cut {cut:.0%}: stress months {(new < 40).sum()} consumers {M.loc[new < 40, 'consumer_id'].nunique()} Stretched mean FHS {new[isS].mean():.1f}")
print("  stress months outside Stretched (untouched by scenario):", int(((M.financial_health_score < 40) & ~isS).sum()))
ms = M[isS]; print(f"  slope within Stretched only: {np.polyfit(ms.spend_to_income_ratio, ms.financial_health_score, 1)[0]:.2f}")
A = np.c_[np.ones(len(M)), M.spend_to_income_ratio, M.credit_utilization_ratio]
res = M.financial_health_score - A @ np.linalg.lstsq(A, M.financial_health_score, rcond=None)[0]
print(f"  R2 of FHS on STI+util: {1 - res.var()/M.financial_health_score.var():.3f}")

h("Nov->Dec Healthy->Stretched via nearest segment centroid (z-space)")
feat = ["financial_health_score", "spend_to_income_ratio", "credit_utilization_ratio", "spending_volatility",
        "engagement_score", "transaction_count", "discretionary_spend_ratio", "online_spend_ratio"]
mu, sd = F[feat].mean(), F[feat].std(ddof=0)
cen = ((F[feat] - mu) / sd).groupby(F.seg).mean()
Zm = ((M[feat] - mu) / sd).values
M["seg"] = cen.index[((Zm[:, None, :] - cen.values[None]) ** 2).sum(2).argmin(1)]
M = M.sort_values(["consumer_id", "analysis_month"]); M["nxt"] = M.groupby("consumer_id").seg.shift(-1)
M["mo"] = pd.to_datetime(M.analysis_month).dt.month
hh = M[(M.seg == "Healthy") & M.nxt.notna()]
sl = hh.groupby("mo").nxt.apply(lambda s: 100 * (s == "Stretched").mean())
print(sl.round(1).to_dict(), f"mean {sl.mean():.1f}; Nov base n={int((hh.mo == 11).sum())}")

h("transactions: 22-23h value share, channel mix by segment")
T = pd.read_csv("BI10_ROUND01_DATASET/consumer_transactions_2025.parquet/consumer_transactions_2025.csv",
                usecols=["consumer_id", "transaction_month", "transaction_hour", "transaction_day_of_week", "spend_amount_vnd", "transaction_channel"])
mm = M[["consumer_id", "mo", "financial_health_score"]].rename(columns={"mo": "transaction_month"})
t = T.merge(mm, on=["consumer_id", "transaction_month"])
t["state"] = np.select([t.financial_health_score < 40, t.financial_health_score >= 80], ["stressed", "healthy"], "mid")
for s in ("stressed", "healthy"):
    d = t[t.state == s]; v = d.spend_amount_vnd.sum()
    print(f"  {s}: 22-23h {100*d.loc[d.transaction_hour >= 22, 'spend_amount_vnd'].sum()/v:.1f}% | Sun+Mon {100*d.loc[d.transaction_day_of_week.isin([0, 6]), 'spend_amount_vnd'].sum()/v:.1f}%")
T["seg"] = T.consumer_id.map(F.seg)
ch = T.pivot_table(index="seg", columns="transaction_channel", values="spend_amount_vnd", aggfunc="sum")
print((100 * ch.div(ch.sum(1), axis=0)).round(1).to_string())

h("ranking inputs: |r| of each tool's trigger column with FHS and with engagement (month level)")
rF = M[cols + ["financial_health_score"]].corr()["financial_health_score"].abs()
rE = M[cols].corr()["engagement_score"].abs()
tools = [("Budgeting", 302, "spend_to_income_ratio"), ("Alerts", len(X), "credit_utilization_ratio"),
         ("Reminders", 258, "spending_volatility"), ("Education", len(D), "discretionary_spend_ratio"),
         ("Nudges", 88, "category_diversity"), ("Products", 351, "credit_utilization_ratio")]
rk = pd.DataFrame([(t, n, c, rF[c], rE[c], n * rF[c]) for t, n, c in tools], columns=["tool", "reach", "trigger", "r_FHS", "r_eng", "reach_x_rFHS"])
print(rk.sort_values("reach_x_rFHS", ascending=False).round(3).to_string(index=False))
tgt = {"Budgeting": set(F.index[F.seg == "Stretched"]), "Alerts": X, "Education": D, "Reminders": set(F.index[F.seg == "Power"]),
       "Nudges": set(F.index[F.seg == "Emerging"]), "Products": set(F.index[F.seg == "Healthy"])}
print("stress months (of 95) falling on each target:", {k: int(st.consumer_id.isin(v).sum()) for k, v in tgt.items()})

h("fairness per target group")
F["age_grp"] = pd.cut(F.age, [14, 17, 24, 34, 44, 54, 64, 120], labels=["15-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"])
base_a = F.age_grp.value_counts(normalize=True)
for g, ids in tgt.items():
    msk = F.index.isin(ids); s = F[msk]
    p = chi2_contingency(pd.crosstab(msk, F.age_grp))[1]; pg = chi2_contingency(pd.crosstab(msk, F.gender))[1]
    po = chi2_contingency(pd.crosstab(msk, F.province))[1]; pocc = chi2_contingency(pd.crosstab(msk, F.occupation))[1]
    ra = (s.age_grp.value_counts(normalize=True) / base_a).round(2)
    print(f"{g} n={msk.sum()} age {s.age.mean():.1f} (base {F.age.mean():.1f}) female {100*(s.gender=='Nữ').mean():.1f}% (base {100*(F.gender=='Nữ').mean():.1f}%)"
          f" minors {int((s.age < 18).sum())} | chi2 p age={p:.3g} gender={pg:.3g} province={po:.3g} occupation={pocc:.3g}")
    print("   age-band ratio vs base:", ra.to_dict())
print("occupations:", F.occupation.nunique(), "provinces:", F.province.nunique(), "minors total:", int((F.age < 18).sum()))
# union reach of the plan
allids = set().union(*tgt.values()) | Dm
print(f"union reach of 6 targets: {len(allids)} consumers")
