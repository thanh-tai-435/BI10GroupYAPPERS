import sys; sys.stdout.reconfigure(encoding="utf-8")
import numpy as np, pandas as pd
M = pd.read_csv("BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv")
F = pd.read_csv("draft/task4_features.csv").set_index("consumer_id")
D = F[(F.financial_health_score < 70) & (F.engagement_score < 70)]
print("distress tail means:", D[["financial_health_score","engagement_score","discretionary_spend_ratio","online_spend_ratio","spend_to_income_ratio"]].mean().round(3).to_dict())
print("base means:", F[["financial_health_score","discretionary_spend_ratio","online_spend_ratio"]].mean().round(3).to_dict())
print("share of base with consumer FHS<70:", round((F.financial_health_score<70).mean()*100,1))
s = np.select([M.financial_health_score<40, M.financial_health_score>=80], ["stressed","healthy"], "mid")
g = M.groupby(s)[["discretionary_spend_vnd","total_spend_vnd"]].sum()
print("spend-weighted discretionary %:", (100*g.discretionary_spend_vnd/g.total_spend_vnd).round(1).to_dict())
isS = M.consumer_id.map(F.segment).eq("Financially Stretched but Highly Engaged")
for b in (-25.33, -22.22):
    print(b, [int((M.financial_health_score - b*M.spend_to_income_ratio*c*isS < 40).sum()) for c in (0,.05,.1,.15)])
print("r(util, engagement) signed:", round(M.credit_utilization_ratio.corr(M.engagement_score),3), "r(div,eng) month", round(M.category_diversity.corr(M.engagement_score),3))
