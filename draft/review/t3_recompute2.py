import sys; sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd, numpy as np
m = pd.read_csv("BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv")
c = m.groupby("consumer_id").agg(eng=("engagement_score","mean"), fhs=("financial_health_score","mean"), n=("analysis_month","size"))
part = c[c.n<12].index
g = c[(c.fhs>=70)&(c.eng<70)].index
print("month of partial consumers", m[m.consumer_id.isin(part)].analysis_month.value_counts().sort_index().to_dict())
print("month of group", m[m.consumer_id.isin(g)].analysis_month.value_counts().sort_index().to_dict())
# consumer-level segment by avg score with official thresholds
seg = pd.cut(c.eng, [-1,40,60,80,101], right=False, labels=["Low","Medium","High","Very high"])
print("avg-score seg", seg.value_counts().to_dict(), (seg.value_counts(normalize=True)*100).round(1).to_dict())
# modal with tie -> lowest? try highest-share ordering
order = {"Tương tác thấp":0,"Tương tác trung bình":1,"Tương tác cao":2,"Tương tác rất cao":3}
m["o"]=m.engagement_segment.map(order)
med = m.groupby("consumer_id").o.median().round().astype(int); print("median seg", med.value_counts().sort_index().to_dict())
# full-year consumers only
full = c[c.n==12]; print("full-year eng min", full.eng.min().round(2), "all >=60?", (full.eng>=60).all())
print("12-month consumers segment months", m[m.consumer_id.isin(full.index)].engagement_segment.value_counts().to_dict())
print("partial consumers eng mean", c.loc[part].eng.mean().round(1), "fhs mean", c.loc[part].fhs.mean().round(1))
t = pd.read_csv("BI10_ROUND01_DATASET/consumer_transactions_2025.parquet/consumer_transactions_2025.csv",
    usecols=["consumer_id","activity_datetime","transaction_channel","spend_amount_vnd","online_transaction_flag","transaction_month"])
ch = t.transaction_channel.value_counts(); print((ch/len(t)*100).round(2).to_dict(), len(t))
v = t.groupby("transaction_channel").spend_amount_vnd.sum(); print("value share", (v/v.sum()*100).round(2).to_dict())
print("non-POS count", round((t.transaction_channel!="POS").mean()*100,2))
print("online flag share count", round(t.online_transaction_flag.mean()*100,2), "value", round(t.loc[t.online_transaction_flag==1,"spend_amount_vnd"].sum()/t.spend_amount_vnd.sum()*100,2))
print(t.groupby("transaction_channel").online_transaction_flag.mean().round(3).to_dict())
# adoption: share of consumers using each channel at least once
ad = t.groupby(["consumer_id","transaction_channel"]).size().unstack(fill_value=0)
print("adoption % consumers", ((ad>0).mean()*100).round(1).to_dict(), "n consumers in txn", len(ad))
print("channels used per consumer", (ad>0).sum(axis=1).value_counts().sort_index().to_dict())
# group in transactions
tg = t[t.consumer_id.isin(g)]; tg["d"]=pd.to_datetime(tg.activity_datetime)
print("group txn months", tg.transaction_month.value_counts().sort_index().to_dict(), "n txns", len(tg))
print("group channel mix", (tg.transaction_channel.value_counts(normalize=True)*100).round(1).to_dict())
tp = t[t.consumer_id.isin(part)]; print("partial txn months", tp.transaction_month.value_counts().sort_index().to_dict())
# per-consumer online share distribution
cc = c.join(m.groupby("consumer_id").online_spend_ratio.mean().rename("onl"))
print("online share quantiles", cc.onl.quantile([.1,.25,.5,.75,.9]).round(3).to_dict(), "full-year mean", cc[cc.n==12].onl.mean().round(3), "partial mean", cc[cc.n<12].onl.mean().round(3))
