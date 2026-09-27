import sys; sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd
m=pd.read_csv("BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv")
f=pd.read_csv("draft/task4_features.csv")
print(f.columns.tolist())
seg=f.set_index("consumer_id")["segment"] if "segment" in f else None
p75=m.engagement_score.quantile(.75)
cx=m[(m.financial_health_score<40)&(m.engagement_score>=p75)].consumer_id.unique()
print("crossover",len(cx)); print(seg.reindex(cx).value_counts())
c=m.groupby("consumer_id")[["financial_health_score","engagement_score"]].mean()
dt=c[(c.financial_health_score<70)&(c.engagement_score<70)].index
print("distress tail",len(dt)); print(seg.reindex(dt).value_counts())
print("tail mean FHS",c.loc[dt].financial_health_score.mean())
st=m[m.financial_health_score<40].consumer_id.unique(); print("stressed consumers by seg"); print(seg.reindex(st).value_counts())
t=pd.read_csv("BI10_ROUND01_DATASET/consumer_transactions_2025.parquet/consumer_transactions_2025.csv",usecols=["consumer_id","amount","transaction_channel"] if True else None)
t["seg"]=t.consumer_id.map(seg)
e=t[t.seg.str.contains("Emerging",na=False)]
print((e.groupby("transaction_channel").amount.sum()/e.amount.sum()*100).round(1))
print("nonPOS trips",(t.transaction_channel!="POS").mean()*100,"value",t.loc[t.transaction_channel!="POS","amount"].sum()/t.amount.sum()*100)
print("provinces",m.province.nunique() if "province" in m else "?")
