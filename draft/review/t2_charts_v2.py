"""v2 charts for Task 2 slides. Run: PYTHONUTF8=1 py draft/review/t2_charts_v2.py
Writes outputs/figures/v2_t2_*.png (150 dpi)."""
import sys, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.stdout.reconfigure(encoding="utf-8")
C = dict(primary="#2E5EAA", accent="#E4572E", good="#3C9D6E", warn="#E0A32E", muted="#9AA5B1", ink="#22303F")
plt.rcParams.update({"font.size": 12, "axes.titlesize": 14, "axes.titleweight": "bold", "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})
MON = "BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv"
TXN = "BI10_ROUND01_DATASET/consumer_transactions_2025.parquet/consumer_transactions_2025.csv"
F = "financial_health_score"
m = pd.read_csv(MON, parse_dates=["analysis_month"]); m["mo"] = m.analysis_month.dt.month
def save(fig, n): fig.tight_layout(); fig.savefig(f"outputs/figures/{n}", dpi=150, bbox_inches="tight"); print("saved", n)

# 1 D1: consumer-level vs month-level distribution (5.8 x 4.4 slot)
c = m.groupby("consumer_id")[F].mean()
fig, ax = plt.subplots(figsize=(8, 6))
bins = np.arange(0, 92, 2)
ax.hist(m[F], bins, density=True, color=C["muted"], alpha=.6, label="Consumer-months (n = 10,992), std 9.5")
ax.hist(c, bins, density=True, histtype="step", lw=2.5, color=C["primary"], label="Consumer average (n = 999), std 4.7")
ax.axvline(40, color=C["accent"], ls="--"); ax.axvline(60, color=C["warn"], ls=":")
ax.text(39, ax.get_ylim()[1] * .2, "FHS < 40:\n95 months,\n70 consumers,\n0 consumers\non average", ha="right", color=C["accent"], fontsize=11)
ax.text(86, ax.get_ylim()[1] * .8, "< 60 at least once:\n869 of 999\nconsumers", ha="center", color=C["warn"], fontsize=11)
ax.set_xlabel("Financial health score"); ax.set_ylabel("Share (density)"); ax.set_yticks([])
ax.set_title("Averages hide the dips: nobody is stressed on average,\nbut 87% of consumers dip below 60 at least once")
ax.legend(frameon=False, loc="upper left", fontsize=10)
save(fig, "v2_t2_distribution.png")

# 2 D2: month-level spend-to-income quintile -> % of months below 60 / below 40 (5.95 x 3.35 slot)
m["q"] = pd.qcut(m.spend_to_income_ratio, 5, labels=False)
q = m.groupby("q").agg(sti=("spend_to_income_ratio", "mean"), fhs=(F, "mean"),
                       w=(F, lambda x: 100 * (x < 60).mean()), s=(F, lambda x: 100 * (x < 40).mean()))
fig, ax = plt.subplots(figsize=(9, 5))
lab = [f"Q{i+1}\nspend/inc {r.sti:.2f}" for i, r in q.iterrows()]
b = ax.bar(lab, q.w, color=[C["good"], C["good"], C["good"], C["warn"], C["accent"]])
for r, w, s, fh in zip(b, q.w, q.s, q.fhs):
    ax.annotate(f"{w:.0f}%" + (f"\n({s:.1f}% < 40)" if s else "") + f"\nmean FHS {fh:.0f}", (r.get_x() + r.get_width() / 2, r.get_height()),
                xytext=(0, 3), textcoords="offset points", ha="center", fontsize=10)
ax.set_ylim(0, 125); ax.set_yticks([0, 25, 50, 75, 100]); ax.set_ylabel("% of months with FHS < 60")
ax.set_xlabel("Spend-to-income quintile (consumer-months, ~2,200 each)")
ax.set_title("Health breaks when spending passes income:\n93% of top-quintile months fall below 60")
save(fig, "v2_t2_sti_threshold.png")

# 3 D3: raw vs spend-to-income-adjusted spread of group means (12.3 x 3.45 slot)
cons = m.groupby("consumer_id").agg(fhs=(F, "mean"), sti=("spend_to_income_ratio", "mean"), age=("age", "first"),
                                    prov=("province_city", "first"), occ=("occupation", "first"))
cons["res"] = cons.fhs - np.polyval(np.polyfit(cons.sti, cons.fhs, 1), cons.sti) + cons.fhs.mean()
cons["Age cohort (6)"] = pd.cut(cons.age, [0, 24, 34, 44, 54, 64, 200])
cons["Province, n ≥ 15 (27)"] = cons.prov.where(cons.prov.map(cons.prov.value_counts()) >= 15)
# ponytail: reuse draft/task2_deep.py keyword map verbatim via exec of its OCC block, not a copy
src = open("draft/task2_deep.py", encoding="utf-8").read()
exec(src[src.index("OCC = ["):src.index("def occ_group")])
cons["og"] = cons.occ.str.lower().map(lambda s: next((g for g, k in OCC if any(w in s for w in k)), "Other"))
cons["Occupation group, n ≥ 20 (7)"] = cons.og.where(cons.og.map(cons.og.value_counts()) >= 20)
dims = ["Age cohort (6)", "Province, n ≥ 15 (27)", "Occupation group, n ≥ 20 (7)"]
fig, axes = plt.subplots(1, 2, figsize=(16, 4.5), sharey=True)
nat = cons.fhs.mean()
for ax, col, t in zip(axes, ["fhs", "res"], ["As observed", "After adjusting for spend-to-income"]):
    for y, d in enumerate(dims):
        g = cons.groupby(d, observed=True)[col].mean()
        ax.plot([g.min(), g.max()], [y, y], color=C["muted"], lw=6, solid_capstyle="round", alpha=.5)
        ax.scatter(g, [y] * len(g), color=C["primary"], s=40, zorder=3)
        ax.text(g.max() + .25, y, f"{g.max() - g.min():.1f} pts", va="center", fontsize=12, color=C["ink"], fontweight="bold")
    ax.axvline(nat, color=C["accent"], ls="--", lw=1.2); ax.set_title(t); ax.set_xlim(61.5, 71)
    ax.set_xlabel("Mean FHS of each group (consumer level, n = 999)"); ax.grid(axis="y", visible=False)
axes[0].set_yticks(range(3), dims); axes[0].invert_yaxis()
fig.suptitle("Province and occupation gaps are spending gaps: holding spend-to-income constant, no group spread exceeds 1.7 pts",
             fontsize=14, fontweight="bold")
for d in dims:
    g = cons.groupby(d, observed=True)
    print(d, "raw range %.2f, adjusted range %.2f" % (np.ptp(g.fhs.mean()), np.ptp(g.res.mean())))
save(fig, "v2_t2_demog_adjusted.png")

# 4 D4: late-night (22-23h) share of spend by FHS band, value vs count (5.95 x 3.35 slot)
tx = pd.read_csv(TXN, usecols=["consumer_id", "transaction_month", "transaction_hour", "spend_amount_vnd"])
j = tx.merge(m[["consumer_id", "mo", F]].rename(columns={"mo": "transaction_month"}), on=["consumer_id", "transaction_month"])
j["band"] = pd.cut(j[F], [-1, 40, 60, 80, 101], right=False, labels=["< 40\nstressed", "40–60\nwatch", "60–80\nstable", "≥ 80\nhealthy"])
j["late"] = j.transaction_hour >= 22
val = j.groupby("band", observed=True).apply(lambda d: 100 * d.spend_amount_vnd[d.late].sum() / d.spend_amount_vnd.sum(), include_groups=False)
cnt = j.groupby("band", observed=True).late.mean() * 100
val, cnt = val[::-1], cnt[::-1]
fig, ax = plt.subplots(figsize=(9, 5)); x = np.arange(4); w = .38
bv = ax.bar(x - w / 2, val, w, color=[C["good"], C["primary"], C["warn"], C["accent"]], label="% of spend VALUE")
bc = ax.bar(x + w / 2, cnt, w, color=C["muted"], label="% of transaction COUNT")
for r in list(bv) + list(bc):
    ax.annotate(f"{r.get_height():.1f}%", (r.get_x() + r.get_width() / 2, r.get_height()), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=10)
ax.set_xticks(x, val.index.astype(str)); ax.set_ylabel("Share spent 22:00–23:59"); ax.set_xlabel("Financial health band of the month")
ax.set_ylim(0, 28); ax.legend(frameon=False, loc="upper left")
ax.set_title("Late-night spend value rises step by step as health falls;\ntransaction count barely moves")
save(fig, "v2_t2_latenight.png")
