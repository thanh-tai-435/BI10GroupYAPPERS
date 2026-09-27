"""v2 Task 3 charts -> outputs/figures/v2_t3_*.png. Run: PYTHONUTF8=1 py draft/review/t3_charts_v2.py"""
import sys; sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import stats

P, A, G, W, M = "#2E5EAA", "#E4572E", "#3C9D6E", "#E0A32E", "#9AA5B1"
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": "#E6E9ED", "grid.linewidth": 0.8, "axes.axisbelow": True, "font.size": 10})
OUT = "outputs/figures/"
D = "BI10_ROUND01_DATASET/"
m = pd.read_csv(D + "consumer_financial_health_engagement_2025.csv")
c = m.groupby("consumer_id").agg(eng=("engagement_score", "mean"), fhs=("financial_health_score", "mean"),
                                 div=("category_diversity", "mean"), n=("analysis_month", "size"))
c["burst"] = c.n < 12  # 91 consumers active on only 1-2 days of 2025
BANDS = [(0, 40, "Low", A), (40, 60, "Medium", W), (60, 80, "High", P), (80, 100.01, "Very high", G)]
save = lambda fig, name: (fig.savefig(OUT + name, dpi=150, bbox_inches="tight"), plt.close(fig), print("saved", name))

# 1 - engagement histogram with official segment bands (one panel replaces hist + segment bar)
fig, ax = plt.subplots(figsize=(7.2, 4.05))
bins = np.arange(0, 102, 2)
for lo, hi, lab, col in BANDS:
    s = m.engagement_score[(m.engagement_score >= lo) & (m.engagement_score < hi)]
    ax.hist(s, bins=bins, color=col, edgecolor="white", linewidth=0.4)
    ax.axvspan(lo, min(hi, 100), color=col, alpha=0.06, lw=0)
    mo = len(s) / len(m) * 100
    cs = ((c.eng >= lo) & (c.eng < hi)).mean() * 100
    ax.text((lo + min(hi, 100)) / 2, 2350, f"{lab}\n{mo:.1f}% of months\n{cs:.1f}% of cust.",
            ha="center", va="top", fontsize=7.5, color=col, fontweight="bold")
low = m.engagement_score < 60; nb = m.consumer_id[low].isin(c.index[c.burst]).sum()
ax.annotate(f"{low.sum()} months ({low.mean()*100:.1f}%) below 60;\n{nb} of them from the {c.burst.sum()} one-off consumers",
            xy=(52, 15), xytext=(4, 900), fontsize=8, color="#5B6573",
            arrowprops=dict(arrowstyle="->", color="#5B6573", lw=0.7))
for x in (40, 60, 80): ax.axvline(x, color="#5B6573", lw=0.8, ls="--")
ax.set_xlim(0, 100); ax.set_ylim(0, 2400)
ax.set_xlabel("engagement_score (consumer-month; segment bands 40 / 60 / 80)")
ax.set_ylabel("Consumer-months")
ax.set_title("99% of consumer-months sit in High / Very high", loc="left", fontweight="bold")
save(fig, "v2_t3_engagement_segments.png")

# 2 - channel mix: share of transactions + share of consumers who used it at least once
t = pd.read_csv(D + "consumer_transactions_2025.parquet/consumer_transactions_2025.csv",
                usecols=["consumer_id", "transaction_channel", "spend_amount_vnd"])
share = t.transaction_channel.value_counts(normalize=True) * 100
vshare = t.groupby("transaction_channel").spend_amount_vnd.sum(); vshare = vshare / vshare.sum() * 100
adopt = (t.groupby(["consumer_id", "transaction_channel"]).size().unstack(fill_value=0) > 0).mean() * 100
order = share.sort_values().index
names = {"POS": "POS", "QR Payment": "QR", "E-commerce": "E-commerce", "Mobile App": "Mobile App", "Recurring Payment": "Recurring"}
fig, ax = plt.subplots(figsize=(7.2, 4.05))
y = np.arange(len(order))
ax.barh(y, share[order], color=[P if ch == "POS" else G for ch in order], height=0.6)
for i, ch in enumerate(order):
    ax.text(share[ch] + 0.8, i, f"{share[ch]:.1f}% of trips · {vshare[ch]:.1f}% of value · used by {adopt[ch]:.0f}% of consumers",
            va="center", fontsize=8.5)
ax.set_yticks(y, [names[ch] for ch in order]); ax.set_xlim(0, 110); ax.grid(axis="y", visible=False)
ax.set_xlabel("Share of 1,852,394 transactions (%)")
ax.set_title(f"POS carries {share['POS']:.0f}% of trips; {(share.drop('POS').sum()):.0f}% are non-POS", loc="left", fontweight="bold")
save(fig, "v2_t3_channel_mix.png")

# 3 - diversity vs engagement, full-year vs one-burst consumers
f = c[~c.burst]; b = c[c.burst]
r_all = stats.pearsonr(c["div"], c.eng)[0]; r_f = stats.pearsonr(f["div"], f.eng)[0]
rng = np.random.default_rng(0)
fig, ax = plt.subplots(figsize=(7.2, 4.05))
ax.scatter(f["div"], f.eng, s=10, alpha=0.45, color=P, lw=0, label=f"Active all 12 months (n={len(f)})")
ax.scatter(b["div"] + rng.uniform(-0.15, 0.15, len(b)), b.eng, s=16, alpha=0.8, color=A, lw=0,
           label=f"Active on 1-2 days only (n={len(b)})")
ax.text(2.2, 80, f"r = {r_all:+.2f} all consumers\nr = {r_f:+.2f} within the 12-month base", fontsize=9, va="top")
ax.set_xlabel("Category diversity (avg categories used per month, consumer)")
ax.set_ylabel("Engagement score (consumer avg)")
ax.set_title("Broad spenders are engaged; the narrow tail is one-off users", loc="left", fontweight="bold")
ax.legend(loc="lower right", frameon=False, fontsize=8.5)
save(fig, "v2_t3_diversity_engagement.png")

# 4 - health x engagement quadrant, cutoff sensitivity inset
g = (c.fhs >= 70) & (c.eng < 70)
fig, ax = plt.subplots(figsize=(7.2, 5.46))
ax.scatter(c.eng[~g & ~c.burst], c.fhs[~g & ~c.burst], s=9, color=M, alpha=0.5, lw=0, label="Active all 12 months")
ax.scatter(c.eng[~g & c.burst], c.fhs[~g & c.burst], s=14, color=W, alpha=0.8, lw=0, label="1-2 active days, FHS < 70")
ax.scatter(c.eng[g], c.fhs[g], s=26, color=A, lw=0, label=f"Target: FHS ≥ 70 & engagement < 70 (n={g.sum()})")
ax.axhline(70, color="#5B6573", lw=0.8, ls="--"); ax.axvline(70, color="#5B6573", lw=0.8, ls="--")
gap_lo, gap_hi = c.eng[c.burst].max(), c.eng[~c.burst].min()
ax.axvspan(gap_lo, gap_hi, color=G, alpha=0.12, lw=0)
ax.text((gap_lo + gap_hi) / 2, 44, f"empty gap\n{gap_lo:.1f}–{gap_hi:.1f}", ha="center", fontsize=8, color=G)
ax.set_xlabel("Engagement score (consumer avg)"); ax.set_ylabel("Financial health score (consumer avg)")
ax.set_title("25 healthy customers who used the card on only 1-2 days", loc="left", fontweight="bold")
ax.set_ylim(38, 97)
ax.legend(loc="lower left", frameon=False, fontsize=8)
ins = ax.inset_axes([0.07, 0.74, 0.34, 0.2])
cuts = [60, 65, 68, 70, 72, 74, 75]; ns = [((c.fhs >= 70) & (c.eng < k)).sum() for k in cuts]
ins.plot(cuts, ns, marker="o", color=A, ms=3); ins.axvline(70, color="#5B6573", lw=0.7, ls="--")
for k, n in zip(cuts, ns): ins.text(k, n + 3, str(n), ha="center", fontsize=6.5)
ins.set_ylim(0, 80); ins.set_title("Group size vs engagement cutoff (FHS ≥ 70)", fontsize=7)
ins.tick_params(labelsize=6.5); ins.set_facecolor("white")
save(fig, "v2_t3_quadrant.png")

assert g.sum() == 25 and c.burst.sum() == 91 and g[g].index.isin(c[c.burst].index).all()  # group = healthy one-burst consumers
