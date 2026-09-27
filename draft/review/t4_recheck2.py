"""Follow-up checks: naming faithfulness (channels), sensitivity of the clustering, Emerging months.
Run after t4_recheck.py (reads scratchpad t4_cons.csv). PYTHONUTF8=1 py draft/review/t4_recheck2.py"""
import sys, numpy as np, pandas as pd
sys.stdout.reconfigure(encoding="utf-8")
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score as ari
SCR = "C:/Users/ThanhTai/AppData/Local/Temp/claude/D--BI10GroupYAPPERS/ef94e05d-86d4-408a-89c9-635ffbeb08a4/scratchpad/t4_cons.csv"
cons = pd.read_csv(SCR, index_col=0); ORDER = ["Healthy", "Stretched", "PowerUsers", "Emerging"]
F = ["financial_health_score", "spend_to_income_ratio", "credit_utilization_ratio", "spending_volatility",
     "engagement_score", "transaction_count", "discretionary_spend_ratio", "online_spend_ratio"]
mon = pd.read_csv("BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv")
mon["seg"] = mon.consumer_id.map(cons.seg); mon["m"] = pd.to_datetime(mon.analysis_month).dt.month
print("months per consumer by seg:", mon.groupby("seg").consumer_id.value_counts().groupby("seg").mean().round(2).to_dict())
print("engagement_segment % consumer-months:\n", (100 * pd.crosstab(mon.seg, mon.engagement_segment, normalize="index")).loc[ORDER].round(1).to_string())
print("Emerging FHS by month:", mon[mon.seg == "Emerging"].groupby("m").financial_health_score.mean().round(1).to_dict())
print("Emerging txn by month:", mon[mon.seg == "Emerging"].groupby("m").transaction_count.mean().round(1).to_dict())

# channel mix per segment from transactions (value + count)
tx = pd.read_csv("BI10_ROUND01_DATASET/consumer_transactions_2025.parquet/consumer_transactions_2025.csv",
                 usecols=["consumer_id", "transaction_channel", "spend_amount_vnd", "online_transaction_flag"])
tx["seg"] = tx.consumer_id.map(cons.seg)
print("tx unmatched:", tx.seg.isna().sum(), "rows", len(tx))
print("channel % of trips:\n", (100 * pd.crosstab(tx.seg, tx.transaction_channel, normalize="index")).loc[ORDER].round(1).to_string())
v = tx.pivot_table(index="seg", columns="transaction_channel", values="spend_amount_vnd", aggfunc="sum")
print("channel % of value:\n", (100 * v.div(v.sum(1), axis=0)).loc[ORDER].round(1).to_string())
print("non-POS % value:", (100 * (1 - v["POS"] / v.sum(1))).loc[ORDER].round(1).to_dict() if "POS" in v else "")
print("online flag % trips:", (100 * tx.groupby("seg").online_transaction_flag.mean()).loc[ORDER].round(1).to_dict())

# sensitivity: alternative feature sets / aggregation
X = StandardScaler().fit_transform(cons[F])
base = KMeans(4, n_init=25, random_state=42).fit_predict(X)
def alt(cols, df=cons):
    return ari(base, KMeans(4, n_init=25, random_state=42).fit_predict(StandardScaler().fit_transform(df[cols])))
red = ["financial_health_score", "spending_volatility", "engagement_score", "transaction_count", "online_spend_ratio"]
print(f"ARI reduced 5 features (drop s2i, util, discretionary): {alt(red):.3f}")
fsd = mon.groupby("consumer_id").financial_health_score.std().fillna(0).rename("fhs_sd")  # 1-month consumers -> 0
ad = mon.groupby("consumer_id").active_transaction_days.mean().rename("active_days")
c2 = cons.join(fsd).join(ad)
print(f"ARI + fhs_sd + active_days: {alt(F + ['fhs_sd', 'active_days'], c2):.3f}")
med = mon.groupby("consumer_id")[F].median()
print(f"ARI median aggregation: {alt(F, med.loc[cons.index]):.3f}")
ex_dec = mon[mon.m < 12].groupby("consumer_id")[F].mean()
ix = ex_dec.index  # 9 Dec-only consumers drop out
print(f"ARI Jan-Nov only (drop Dec), n={len(ix)}: " + str(round(ari(pd.Series(base, cons.index)[ix],
      KMeans(4, n_init=25, random_state=42).fit_predict(StandardScaler().fit_transform(ex_dec[F]))), 3)))

# months observed per consumer vs segment (Emerging = consumers seen in ~1 month)
nm = mon.groupby("consumer_id").size().rename("n_months")
print("n_months distribution:", nm.value_counts().sort_index().to_dict())
print(pd.crosstab(cons.seg, nm.reindex(cons.index)).loc[ORDER].to_string())
print(f"ARI(k-means, 'observed <12 months' rule) on all 999: "
      f"{ari(cons.seg.eq('Emerging'), nm.reindex(cons.index).lt(12)):.3f}")
em = cons.index[cons.seg == "Emerging"]
print("Emerging active month distribution:", mon[mon.consumer_id.isin(em)].m.value_counts().sort_index().to_dict())
# silhouette & k on the 911 full-year consumers only
from sklearn.metrics import silhouette_score
full = nm.reindex(cons.index).eq(12).values
Xf = StandardScaler().fit_transform(cons.loc[full, F])
for k in range(2, 7):
    l = KMeans(k, n_init=25, random_state=42).fit_predict(Xf)
    print(f"full-year only k={k} sil {silhouette_score(Xf, l):.3f} sizes {sorted(np.bincount(l), reverse=True)}")
l3 = KMeans(3, n_init=25, random_state=42).fit_predict(Xf)
print("full-year k=3 vs current 3 big segs ARI:", round(ari(cons.seg[full], l3), 3))
Xall = X[full]
for k in (3, 4):
    l = KMeans(k, n_init=25, random_state=42).fit_predict(Xall)
    print(f"full-year, deck scaler, k={k}: ARI vs current = {ari(cons.seg[full], l):.3f}")
