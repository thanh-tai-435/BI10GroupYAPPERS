import sys; sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd, numpy as np
from scipy import stats
m = pd.read_csv("BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv")
print(m.shape, m.consumer_id.nunique())
e = m.engagement_score
print("CM eng mean/median/q25/q75/min/max", e.mean().round(2), e.median(), e.quantile([.25,.75]).round(2).tolist(), e.min(), e.max())
print(m.engagement_segment.value_counts(), (m.engagement_segment.value_counts(normalize=True)*100).round(2))
# months per consumer
mc = m.groupby("consumer_id").size(); print("months per consumer", mc.value_counts().sort_index().to_dict())
# modal segment
mode = m.groupby("consumer_id").engagement_segment.agg(lambda s: s.value_counts().index[0])
print("modal seg", mode.value_counts().to_dict(), (mode.value_counts(normalize=True)*100).round(1).to_dict())
# ever-low / ever below high
print("consumers with >=1 low month", m[m.engagement_segment=="Tương tác thấp"].consumer_id.nunique(),
      "with >=1 medium", m[m.engagement_segment=="Tương tác trung bình"].consumer_id.nunique())
c = m.groupby("consumer_id").agg(eng=("engagement_score","mean"), fhs=("financial_health_score","mean"),
    div=("category_diversity","mean"), rec=("transaction_recency_days","mean"), tc=("transaction_count","mean"),
    ad=("active_transaction_days","mean"), onl=("online_spend_ratio","mean"), n=("analysis_month","size"),
    age=("age","first"), gender=("gender","first"), occ=("occupation","first"), prov=("province_city","first"),
    sti=("spend_to_income_ratio","mean"), cu=("credit_utilization_ratio","mean"), disc=("discretionary_spend_ratio","mean"))
print("consumer eng mean/median/p10/q25/q75/min/max", c.eng.mean().round(2), c.eng.median().round(2), c.eng.quantile([.1,.25,.75]).round(2).tolist(), c.eng.min().round(2), c.eng.max().round(2))
# consumer-level segment by avg score using segment thresholds: infer thresholds
print(m.groupby("engagement_segment").engagement_score.agg(["min","max"]))
print("months per consumer for dormant (div<10)", c[c["div"]<10].n.value_counts().to_dict(), "count", (c["div"]<10).sum())
print("online share consumer mean/min/max", (c.onl.mean()*100).round(2), c.onl.min(), (c.onl.max()*100).round(1), "CM mean", (m.online_spend_ratio.mean()*100).round(2))
print("div CM range", m.category_diversity.min(), m.category_diversity.max(), "cons mean", c["div"].mean().round(2), "13-14:", (c["div"]>=13).sum(), "div>=12.5", (c["div"]>=12.5).sum())
print("r div-eng cons", stats.pearsonr(c["div"], c.eng)[0].round(3), "CM", stats.pearsonr(m.category_diversity, e)[0].round(3))
core = c[c["div"]>=10]
print("core n", len(core), "r", stats.pearsonr(core["div"], core.eng)[0].round(3), "spearman", stats.spearmanr(core["div"], core.eng)[0].round(3))
print("spearman all cons", stats.spearmanr(c["div"], c.eng)[0].round(3))
for col in ["transaction_recency_days","active_transaction_days","transaction_count"]:
    print(col, m[col].min(), m[col].median(), m[col].max(), "r CM", stats.pearsonr(m[col], e)[0].round(3), "spearman CM", stats.spearmanr(m[col], e)[0].round(3))
for col in ["rec","ad","tc"]:
    print("cons", col, c[col].min().round(2), c[col].median().round(2), c[col].max().round(2), "r", stats.pearsonr(c[col], c.eng)[0].round(3))
# heatmap cells
rb = pd.cut(m.transaction_recency_days, [-1,0,3,10,31], labels=["0","1-3","4-10","11-30"])
ab = pd.cut(m.active_transaction_days, [0,5,15,25,29,31], labels=["1-5","6-15","16-25","26-29","30-31"])
print(m.groupby([rb,ab], observed=True).engagement_score.agg(["mean","size"]).round(1))
# D5
hi_n = (c.fhs>=70).sum(); print("FHS>=70", hi_n, "pct rank of 70:", (c.fhs<70).mean().round(3), "p75/p79/p90", c.fhs.quantile([.75,.79,.9]).round(2).tolist())
for ec in [60,65,68,70,72,74,75]: print("eng<",ec, ((c.fhs>=70)&(c.eng<ec)).sum())
for fc in [60,65,68,70,72,75]: print("fhs>=",fc, ((c.fhs>=fc)&(c.eng<70)).sum())
g = (c.fhs>=70)&(c.eng<70); print("group", g.sum(), "low-eng total", (c.eng<70).sum())
print(c.groupby(g)[["fhs","eng","tc","ad","rec","div","onl","sti","cu","disc","age","n"]].mean().round(3).T)
print("gap: eng values between 62 and 71 among consumers", c.eng[(c.eng>60)&(c.eng<72)].sort_values().round(2).tolist()[:15])
print("group gender", c[g].gender.value_counts().to_dict(), "base", c.gender.value_counts(normalize=True).round(2).to_dict())
print("group occ top", c[g].occ.value_counts().head(5).to_dict())
print("group months", c[g].n.value_counts().to_dict())
print("group ages", c[g].age.describe().round(1).to_dict(), "base age mean", c.age.mean().round(1))
# Task4 segment link
try:
    f = pd.read_csv("draft/task4_features.csv"); segcol=[x for x in f.columns if "seg" in x.lower()]; print(segcol)
    s = f.set_index("consumer_id")[segcol[0]]; print(s.reindex(c[g].index).value_counts().to_dict())
except Exception as ex: print("t4", ex)
c.to_csv("C:/Users/ThanhTai/AppData/Local/Temp/claude/D--BI10GroupYAPPERS/ef94e05d-86d4-408a-89c9-635ffbeb08a4/scratchpad/t3_cons.csv")
