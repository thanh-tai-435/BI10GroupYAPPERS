"""
Task 3 deep-dive (P3). Run: PYTHONUTF8=1 py draft/task3_deep.py > draft/task3_deep_output.txt
Each '## CELL' block is also one cell of notebooks/task3_engagement.ipynb (after %run -i draft/task3.py).
"""
import runpy, sys
sys.stdout.reconfigure(encoding="utf-8")
globals().update(runpy.run_path("draft/task3.py"))
import matplotlib; matplotlib.use("Agg")

## CELL 1
# Style chung cho chart (giống draft/make_charts.py)
import os, numpy as np, pandas as pd, matplotlib.pyplot as plt
pd.set_option("display.width", 250, "display.max_columns", 30)
plt.rcParams.update({"figure.figsize": (10, 6), "font.size": 11, "axes.titlesize": 15, "axes.titleweight": "bold",
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})
C = dict(primary="#2E5EAA", accent="#E4572E", good="#3C9D6E", warn="#E0A32E", muted="#9AA5B1", ink="#22303F")
os.makedirs("outputs/figures", exist_ok=True)
def save(fig, name):
    fig.tight_layout(); fig.savefig(f"outputs/figures/{name}", dpi=150, bbox_inches="tight"); plt.show(); print("saved", name)
SEG_EN = {"Financially Healthy & Highly Engaged": "Healthy & Engaged", "Financially Stretched but Highly Engaged": "Stretched & Engaged",
          "High-Activity Digital Power Users": "Digital Power Users", "Low Engagement & Emerging Digital": "Emerging Digital"}
ENG_EN = {"Tương tác thấp": "Low", "Tương tác trung bình": "Medium", "Tương tác cao": "High", "Tương tác rất cao": "Very high"}

## CELL 2
h("DEEP D1 - Share of consumers in EACH engagement segment (consumer = modal segment)")
share = modal.map(ENG_EN).value_counts().reindex(["Low", "Medium", "High", "Very high"])
print(pd.DataFrame({"consumers": share, "pct": (100 * share / N).round(1)}).to_string())
fig, ax = plt.subplots(figsize=(9, 5))
b = ax.bar(share.index, share.values, color=[C["accent"], C["warn"], C["primary"], C["good"]])
for r, v in zip(b, share.values):
    ax.annotate(f"{v} ({100*v/N:.1f}%)", (r.get_x() + r.get_width()/2, v), xytext=(0, 3), textcoords="offset points", ha="center")
ax.set_ylabel("Consumers (modal monthly segment)"); ax.set_xlabel("Engagement segment")
ax.set_title("91% of consumers sit in High / Very-high engagement")
save(fig, "t3_segment_share.png")

## CELL 3
h("DEEP D2 - Average online spend share + who uses QR / Mobile (by Task 4 segment)")
print(f"Average online spend share (consumer level): {100*con.online_spend_ratio.mean():.1f}% "
      f"(month level {100*mon.online_spend_ratio.mean():.1f}%)")
seg = pd.read_csv("draft/task4_features.csv", usecols=["consumer_id", "segment"])
tx = pd.read_csv(TXN, usecols=["consumer_id", "transaction_channel", "spend_amount_vnd"]).merge(seg, on="consumer_id")
chs = pd.crosstab(tx.segment.map(SEG_EN), tx.transaction_channel, normalize="index") * 100
chv = pd.crosstab(tx.segment.map(SEG_EN), tx.transaction_channel, values=tx.spend_amount_vnd, aggfunc="sum", normalize="index") * 100
print("Channel share of TRANSACTIONS by segment (%):\n", chs.round(1).to_string())
print("\nChannel share of SPEND by segment (%):\n", chv.round(1).to_string())

## CELL 4
h("DEEP D3 - Category diversity distribution + is r=+0.94 driven by the small tail?")
cdv = con.category_diversity
print("Consumer-level diversity bins:\n", pd.cut(cdv, [0, 4, 6, 8, 10, 12, 13, 14.01]).value_counts().sort_index().to_string())
core = con[con.category_diversity >= 8]
print(f"r(all {len(con)}) = {con.category_diversity.corr(con.engagement_score):+.3f} | "
      f"r(diversity>=8, n={len(core)}) = {core.category_diversity.corr(core.engagement_score):+.3f} | "
      f"Spearman(all) = {con.category_diversity.corr(con.engagement_score, method='spearman'):+.3f}")
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(cdv, bins=np.arange(1.5, 14.6, 0.5), color=C["primary"], edgecolor="white")
ax.set_yscale("log"); ax.set_xlabel("Category diversity (consumer mean of monthly count, max 14)")
ax.set_ylabel("Consumers (log scale)"); ax.set_title("Diversity: a saturated core near 14 and a thin dormant tail")
save(fig, "t3_diversity_hist.png")

## CELL 5
h("DEEP D4 - Recency x Frequency heatmap (consumer-month, colour = mean engagement)")
rb = pd.cut(mon.transaction_recency_days, [-0.1, 0, 3, 10, 31], labels=["0 d", "1-3 d", "4-10 d", "11-30 d"])
fb = pd.cut(mon.active_transaction_days, [0, 5, 15, 25, 29, 31], labels=["1-5", "6-15", "16-25", "26-29", "30-31"])
hm = mon.pivot_table(index=rb, columns=fb, values="engagement_score", aggfunc="mean", observed=False)
hn = mon.pivot_table(index=rb, columns=fb, values="engagement_score", aggfunc="size", observed=False)
print("Mean engagement:\n", hm.round(1).to_string()); print("\nConsumer-months per cell:\n", hn.fillna(0).astype(int).to_string())
fig, ax = plt.subplots(figsize=(9, 5.5))
im = ax.imshow(hm.values, cmap="YlGnBu", vmin=20, vmax=85, aspect="auto")
for i in range(hm.shape[0]):
    for j in range(hm.shape[1]):
        n = hn.iloc[i, j]
        if n > 0 and not np.isnan(hm.iloc[i, j]):
            ax.text(j, i, f"{hm.iloc[i, j]:.0f}\nn={int(n):,}", ha="center", va="center", fontsize=9,
                    color="white" if hm.iloc[i, j] > 60 else C["ink"])
ax.set_xticks(range(hm.shape[1]), hm.columns); ax.set_yticks(range(hm.shape[0]), hm.index)
ax.set_xlabel("Active transaction days in month (frequency)"); ax.set_ylabel("Days since last transaction (recency)")
ax.grid(False); fig.colorbar(im, ax=ax, label="Mean engagement score")
ax.set_title("Engagement is driven by consistent activity, not recency alone")
save(fig, "t3_recency_frequency.png")

## CELL 6
h("DEEP D5 - Healthy-but-Disengaged cutoff sensitivity (consumer level)")
tab = pd.DataFrame({f"eng<{e}": [int(((con.financial_health_score >= f) & (con.engagement_score < e)).sum()) for f in (65, 70, 75)]
                    for e in (60, 65, 70, 75)}, index=[f"FHS>={f}" for f in (65, 70, 75)])
print(tab.to_string())
gap = con.engagement_score.sort_values()
print("Engagement values around the cutoff (consumer level): largest gap between consecutive consumers in 50-75:",
      gap[(gap > 50) & (gap < 75)].diff().max().round(2))
print("Why FHS>=70 & eng<70: the count is flat (25) from eng<60 to eng<70 -> a natural gap; eng<75 jumps as it hits the main body.")

## CELL 7
h("Chart-choice rationale (for speaker notes)")
for k, v in {
    "t3_segment_share.png": "Bar of 4 ordered categories with counts + % -> reads shares exactly (pie hides small tails).",
    "t3_diversity_hist.png": "Histogram, log y: continuous variable with a huge spike at 14 and a thin tail -> log keeps the tail visible.",
    "t3_recency_frequency.png": "Heatmap: two binned drivers x one outcome -> shows the interaction a pair of scatters would hide.",
    "t3_diversity_vs_engagement.png": "Scatter: two continuous consumer-level variables, correlation is the claim.",
    "t3_channel_mix.png": "Bar by channel: 5 nominal categories, count vs value compared side by side.",
}.items():
    print(f"  {k:<34} {v}")
