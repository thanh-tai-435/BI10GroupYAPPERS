"""
Independent re-check of Task 4 (slides 16-18). Does NOT import task4.py.
Run: PYTHONUTF8=1 py draft/review/t4_recheck.py > draft/review/t4_recheck_output.txt
"""
import sys, numpy as np, pandas as pd
sys.stdout.reconfigure(encoding="utf-8")
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.metrics import (silhouette_score, adjusted_rand_score as ari,
                             calinski_harabasz_score, davies_bouldin_score)
from scipy.stats import chi2_contingency

MON = "BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv"
F = ["financial_health_score", "spend_to_income_ratio", "credit_utilization_ratio", "spending_volatility",
     "engagement_score", "transaction_count", "discretionary_spend_ratio", "online_spend_ratio"]
def h(t): print(f"\n=== {t} ===")

mon = pd.read_csv(MON).sort_values(["consumer_id", "analysis_month"])
mon["m"] = pd.to_datetime(mon.analysis_month).dt.month
cons = mon.groupby("consumer_id")[F].mean()
demo = mon.groupby("consumer_id")[["age", "gender", "occupation"]].first()
print("rows", len(mon), "consumers", len(cons), "nulls", int(cons.isna().sum().sum()), "min age", demo.age.min())

sc = StandardScaler().fit(cons); X = sc.transform(cons)

h("k scan: silhouette / CH / DB")
for k in range(2, 9):
    lab = KMeans(k, n_init=10, random_state=42).fit_predict(X)
    print(k, f"sil {silhouette_score(X, lab):.4f}  CH {calinski_harabasz_score(X, lab):.0f}  DB {davies_bouldin_score(X, lab):.3f}  sizes {sorted(np.bincount(lab), reverse=True)}")

km = KMeans(4, n_init=25, random_state=42).fit(X); lab = km.labels_
prof = cons.groupby(lab)[F].mean()
name = {prof.financial_health_score.idxmax(): "Healthy", prof.spend_to_income_ratio.idxmax(): "Stretched",
        prof.transaction_count.idxmax(): "PowerUsers", prof.engagement_score.idxmin(): "Emerging"}
assert len(set(name.values())) == 4
cons["seg"] = pd.Series(lab, index=cons.index).map(name)
ORDER = ["Healthy", "Stretched", "PowerUsers", "Emerging"]
print(f"\nfinal sil {silhouette_score(X, lab):.4f}; coverage {cons.seg.notna().sum()}/999")

h("profiles (yearly-mean)")
p = cons.groupby("seg")[F].mean().loc[ORDER]
p.insert(0, "n", cons.seg.value_counts()); p.insert(1, "pct", 100 * p.n / 999)
print(p.round(3).T.to_string()); print("global\n", cons[F].mean().round(3).to_string())
print("txn ratio PowerUsers/avg", round(p.loc["PowerUsers", "transaction_count"] / cons.transaction_count.mean(), 2))

h("k=2 and k=3 splits (what the silhouette winner actually is)")
for k in (2, 3):
    l = KMeans(k, n_init=25, random_state=42).fit_predict(X)
    print(k, pd.crosstab(cons.seg, l).loc[ORDER].to_string())

h("extra profile columns (not clustering inputs)")
g = mon.assign(seg=mon.consumer_id.map(cons.seg))
extra = g.groupby("seg").agg(
    essential=("essential_spend_ratio", "mean"), active_days=("active_transaction_days", "mean"),
    diversity=("category_diversity", "mean"), recency=("transaction_recency_days", "mean"),
    stress_month_pct=("financial_health_score", lambda s: 100 * (s < 40).mean()),
    next_low_flag_pct=("next_month_low_health_flag", lambda s: 100 * s.mean()),
).loc[ORDER]
fhs_sd = g.groupby(["seg", "consumer_id"]).financial_health_score.std().groupby("seg").mean().loc[ORDER]
extra["fhs_within_year_sd"] = fhs_sd
anyst = g.groupby(["seg", "consumer_id"]).financial_health_score.min().lt(40).groupby("seg").sum().loc[ORDER]
extra["consumers_with_stress_month"] = anyst
extra["age_mean"] = cons.join(demo).groupby("seg").age.mean().loc[ORDER]
extra["female_pct"] = 100 * cons.join(demo).groupby("seg").gender.apply(lambda s: (s == "Nữ").mean()).loc[ORDER]
print(extra.round(3).T.to_string())
print("FHS segment mix % by seg:\n", (100 * pd.crosstab(g.seg, g.financial_health_segment, normalize="index")).loc[ORDER].round(1).to_string())

h("feature correlations (yearly means)")
print(cons[F].corr().round(2).to_string())

h("rank of each segment on each feature (1 = highest)")
print(p[F].rank(ascending=False).astype(int).to_string())

h("stability")
sa = [ari(lab, KMeans(4, n_init=10, random_state=s).fit_predict(X)) for s in range(20)]
print(f"seed ARI min {min(sa):.3f} mean {np.mean(sa):.3f}")
rng = np.random.default_rng(42); ba = []
for _ in range(50):
    i = rng.choice(999, 799, replace=False)
    ba.append(ari(lab, KMeans(4, n_init=10, random_state=42).fit(X[i]).predict(X)))
print(f"bootstrap ARI mean {np.mean(ba):.3f} p5 {np.percentile(ba, 5):.3f}")
gm = GaussianMixture(4, covariance_type="full", n_init=5, random_state=42).fit(X)
gl, gp = gm.predict(X), gm.predict_proba(X).max(1)
print(f"GMM ARI {ari(lab, gl):.3f}; boundary p<0.6 {(gp < .6).sum()}")
print(pd.crosstab(cons.seg, gl).loc[ORDER].to_string())
# ARI among only the 3 big segments
big = cons.seg.ne("Emerging").values
print(f"GMM ARI on the 911 non-Emerging consumers: {ari(lab[big], gl[big]):.3f}")
pca = PCA(2, random_state=42).fit(X); print("PCA var", pca.explained_variance_ratio_.round(3), round(pca.explained_variance_ratio_.sum(), 3))
print("PC loadings\n", pd.DataFrame(pca.components_.T, index=F, columns=["PC1", "PC2"]).round(2).to_string())
# per-segment silhouette
from sklearn.metrics import silhouette_samples
ss = pd.Series(silhouette_samples(X, lab), index=cons.index)
print("per-seg silhouette\n", ss.groupby(cons.seg).mean().loc[ORDER].round(3).to_string())

h("2x2 median cross-check")
mh, me = cons.financial_health_score.median(), cons.engagement_score.median()
r = np.where(cons.financial_health_score >= mh, np.where(cons.engagement_score >= me, "H+E", "H+D"),
             np.where(cons.engagement_score >= me, "S+E", "V+D"))
cons["r2"] = r
print(f"medians FHS {mh:.2f} eng {me:.2f}")
print(pd.crosstab(cons.seg, cons.r2, margins=True).loc[ORDER + ["All"]].to_string())
print("engagement median by seg:", cons.groupby("seg").engagement_score.median().loc[ORDER].round(1).to_dict())
print("% above engagement median by seg:", (100 * cons.engagement_score.ge(me).groupby(cons.seg).mean()).loc[ORDER].round(1).to_dict())

h("migration A: deck method (monthly rows -> yearly-fitted centroids, yearly scaler)")
g["mseg"] = pd.Series(km.predict(sc.transform(g[F])), index=g.index).map(name)
g["nxt"] = g.groupby("consumer_id").mseg.shift(-1)
t = g.dropna(subset=["nxt"])
hh = t[t.mseg == "Healthy"]
sl = hh.groupby("m").nxt.apply(lambda s: 100 * (s == "Stretched").mean())
print("Healthy->Stretched by start month\n", sl.round(1).to_string())
print(f"mean of monthly rates {sl.mean():.1f} | pooled {100 * (hh.nxt == 'Stretched').mean():.1f}")
print("month-level segment share % (deck method):\n", (100 * pd.crosstab(g.m, g.mseg, normalize="index"))[ORDER].round(1).to_string())
print(f"consumer-months landing in their own yearly segment: {100 * (g.mseg == g.seg).mean():.1f}%")
print("by yearly seg:", (100 * (g.mseg == g.seg).groupby(g.seg).mean()).loc[ORDER].round(1).to_dict())
print("monthly vs yearly std of features (ratio):\n", (g[F].std() / cons[F].std()).round(2).to_string())

h("migration B: de-seasonalised (subtract month mean, add back annual mean) then same centroids")
adj = g[F] - g.groupby("m")[F].transform("mean") + g[F].mean()
g["aseg"] = pd.Series(km.predict(sc.transform(adj)), index=g.index).map(name)
g["anx"] = g.groupby("consumer_id").aseg.shift(-1)
t2 = g.dropna(subset=["anx"]); hh2 = t2[t2.aseg == "Healthy"]
sl2 = hh2.groupby("m").anx.apply(lambda s: 100 * (s == "Stretched").mean())
print(sl2.round(1).to_string()); print(f"mean {sl2.mean():.1f}")

h("Dec seasonality: month means")
print(g.groupby("m")[["financial_health_score", "spend_to_income_ratio", "credit_utilization_ratio"]].mean().round(3).to_string())

h("migration C: consumer-level FHS drop Nov->Dec by yearly segment")
pv = g.pivot_table(index="consumer_id", columns="m", values="financial_health_score")
d = (pv[12] - pv[11]).groupby(cons.seg).mean().loc[ORDER]
print("mean FHS change Nov->Dec:", d.round(1).to_dict())

h("demographics")
dd = cons.join(demo)
dd["ag"] = pd.cut(dd.age, [14, 17, 24, 34, 44, 54, 64, 120], labels=["15-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"])
for c in ["gender", "ag"]:
    ct = pd.crosstab(dd.seg, dd[c]); chi2, pv_, dof, exp = chi2_contingency(ct)
    V = np.sqrt(chi2 / (ct.values.sum() * (min(ct.shape) - 1)))
    print(f"{c}: p={pv_:.4f} chi2={chi2:.1f} dof={dof} CramerV={V:.3f} cells exp<5: {(exp < 5).sum()}/{exp.size}")
dd["ag2"] = pd.cut(dd.age, [14, 34, 49, 64, 120], labels=["15-34", "35-49", "50-64", "65+"])
ct = pd.crosstab(dd.seg, dd.ag2); chi2, pv_, dof, exp = chi2_contingency(ct)
print(f"age 4 bins: p={pv_:.2e} CramerV={np.sqrt(chi2 / (999 * 3)):.3f} min exp {exp.min():.1f}")
print((100 * pd.crosstab(dd.seg, dd.ag2, normalize="index")).loc[ORDER].round(1).to_string())
ct = pd.crosstab(dd.seg, dd.occupation); chi2, pv_, dof, exp = chi2_contingency(ct)
print(f"occupation: p={pv_:.3f} CramerV={np.sqrt(chi2 / (999 * 3)):.3f} (sparse: exp<5 {(exp < 5).mean():.0%})")

h("persona mapping")
print("discretionary<0.40:", int((cons.discretionary_spend_ratio < .40).sum()),
      cons[cons.discretionary_spend_ratio < .40].seg.value_counts().to_dict())
print("essential>=0.5 (monthly-mean):", int((1 - cons.discretionary_spend_ratio >= .5).sum()))
hd = (cons.financial_health_score >= 70) & (cons.engagement_score < 70)
print("FHS>=70 & eng<70:", int(hd.sum()), cons[hd].seg.value_counts().to_dict())

cons.join(demo).to_csv("C:/Users/ThanhTai/AppData/Local/Temp/claude/D--BI10GroupYAPPERS/ef94e05d-86d4-408a-89c9-635ffbeb08a4/scratchpad/t4_cons.csv")
