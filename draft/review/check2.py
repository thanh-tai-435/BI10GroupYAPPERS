import sys; sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd
f=pd.read_csv("draft/task4_features.csv"); seg=f.set_index("consumer_id")["segment"]
t=pd.read_csv("BI10_ROUND01_DATASET/consumer_transactions_2025.parquet/consumer_transactions_2025.csv",usecols=["consumer_id","spend_amount_vnd","transaction_channel","merchant_id","province_city","transaction_month"])
t["seg"]=t.consumer_id.map(seg)
for s,g in t.groupby("seg"): print(s,(g.groupby("transaction_channel").spend_amount_vnd.sum()/g.spend_amount_vnd.sum()*100).round(1).to_dict())
np_=t.transaction_channel!="POS"
print("nonPOS trips %.1f value %.1f"%(np_.mean()*100,t.loc[np_,"spend_amount_vnd"].sum()/t.spend_amount_vnd.sum()*100))
print("merchants",t.merchant_id.nunique(),"provinces",t.province_city.nunique())
mo=t.groupby("transaction_month").spend_amount_vnd.sum(); print((mo/mo.sum()*100).round(2).to_dict(), mo.sum())
