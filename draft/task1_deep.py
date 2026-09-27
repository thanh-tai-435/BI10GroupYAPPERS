"""
Task 1 deep-dive (P1). Run: PYTHONUTF8=1 py draft/task1_deep.py > draft/task1_deep_output.txt
Each '## CELL' block is also one cell of notebooks/task1_eda.ipynb (after %run -i draft/task1_eda.py).
"""
import runpy, sys
sys.stdout.reconfigure(encoding="utf-8")
globals().update(runpy.run_path("draft/task1_eda.py"))
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
def h(t): print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)
# cột bổ sung cho Q1/Q4 (task1_eda.py chỉ nạp 6 cột)
tx2 = pd.read_csv(TXN, usecols=["consumer_id", "activity_datetime", "spending_category", "transaction_month"])

## CELL 2
h("DEEP Q3 - Channel breakdown for high-spend, below-average-digital provinces")
CH = ["POS", "QR Payment", "E-commerce", "Mobile App", "Recurring Payment"]
top = target.head(5)["province_city"].tolist()
sub = txn[txn.province_city.isin(top)]
cnt = pd.crosstab(sub.province_city, sub.transaction_channel, normalize="index")[CH] * 100
val = pd.crosstab(sub.province_city, sub.transaction_channel, values=sub.spend_amount_vnd, aggfunc="sum", normalize="index")[CH] * 100
nat_c = txn.transaction_channel.value_counts(normalize=True)[CH] * 100
nat_v = txn.groupby("transaction_channel").spend_amount_vnd.sum()[CH] / txn.spend_amount_vnd.sum() * 100
cnt.loc["National"], val.loc["National"] = nat_c, nat_v
cnt, val = cnt.loc[top + ["National"]], val.loc[top + ["National"]]
print("Share of TRANSACTIONS by channel (%):\n", cnt.round(1).to_string())
print("\nShare of SPEND VALUE by channel (%):\n", val.round(1).to_string())
gap = (cnt.drop("National")[CH[1:]].sum(1) - cnt.loc["National", CH[1:]].sum()).round(2)
print("\nDigital-share gap vs national (pp, by count):\n", gap.to_string())
print(f"-> max |gap| = {gap.abs().max():.2f}pp: channel mix is near-identical; digital value share "
      f"{val.drop('National')[CH[1:]].sum(1).min():.1f}-{val.drop('National')[CH[1:]].sum(1).max():.1f}% vs national {val.loc['National', CH[1:]].sum():.1f}%")

EN = {"Thành phố Hồ Chí Minh": "Ho Chi Minh City", "Hà Nội": "Ha Noi", "Đồng Nai": "Dong Nai", "Lâm Đồng": "Lam Dong",
      "Hưng Yên": "Hung Yen", "Hải Phòng": "Hai Phong", "Cần Thơ": "Can Tho", "Đà Nẵng": "Da Nang", "National": "National avg"}
fig, ax = plt.subplots(figsize=(10, 5.5))
cols = [C["muted"], C["primary"], C["good"], C["warn"], C["accent"]]
left = np.zeros(len(cnt))
for ch, col in zip(CH, cols):
    ax.barh([EN.get(p, p) for p in cnt.index], cnt[ch], left=left, color=col, label=ch)
    for i, v in enumerate(cnt[ch]):
        if v > 4: ax.text(left[i] + v / 2, i, f"{v:.1f}", ha="center", va="center", color="white", fontsize=9)
    left += cnt[ch].values
ax.invert_yaxis(); ax.set_xlim(0, 100); ax.set_xlabel("% of transactions"); ax.grid(axis="y", visible=False)
ax.set_title("High-spend provinces: channel mix mirrors the national average")
ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(.5, -.12), frameon=False, fontsize=9)
save(fig, "t1_province_channel.png")

## CELL 3
h("DEEP Q2 - Is the essential->discretionary inversion a gradient or a threshold artefact?")
mon["fhs_bin"] = pd.cut(mon.financial_health_score, [0, 40, 50, 60, 70, 80, 90, 101], right=False,
                        labels=["<40", "40-49", "50-59", "60-69", "70-79", "80-89", "90+"])
gb = mon.groupby("fhs_bin", observed=True).apply(lambda d: pd.Series({
    "months": len(d), "discretionary_pct": 100 * d.discretionary_spend_vnd.sum() / (d.essential_spend_vnd.sum() + d.discretionary_spend_vnd.sum())}))
print(gb.round(1).to_string())
print(f"Spearman(FHS, discretionary_spend_ratio) month grain: "
      f"{mon.financial_health_score.corr(mon.discretionary_spend_ratio, method='spearman'):+.3f}")
for lo, hi in [(35, 85), (40, 80), (45, 75), (50, 70)]:
    a, b = mon[mon.financial_health_score < lo], mon[mon.financial_health_score >= hi]
    da = 100 * a.discretionary_spend_vnd.sum() / (a.essential_spend_vnd.sum() + a.discretionary_spend_vnd.sum())
    db = 100 * b.discretionary_spend_vnd.sum() / (b.essential_spend_vnd.sum() + b.discretionary_spend_vnd.sum())
    print(f"  FHS<{lo} ({len(a):>5} mo) {da:5.1f}% discretionary  vs  FHS>={hi} ({len(b):>5} mo) {db:5.1f}%  -> gap {da-db:+.1f}pp")

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(gb.index.astype(str), gb.discretionary_pct, marker="o", lw=2.5, color=C["accent"])
for x, y, n in zip(gb.index.astype(str), gb.discretionary_pct, gb.months):
    ax.annotate(f"{y:.0f}%\n(n={int(n):,})", (x, y), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=9)
ax.axhline(50, color=C["muted"], ls="--", lw=1); ax.set_ylim(0, 100)
ax.set_xlabel("Financial health score band (consumer-month)"); ax.set_ylabel("Discretionary share of spend (%)")
ax.set_title("Discretionary share falls steadily as health rises")
save(fig, "t1_discretionary_gradient.png")

## CELL 4
h("DEEP Q1 - Which categories drive the December peak? + timestamp-year check")
g = tx2.groupby(["transaction_month", "spending_category"]).size().unstack(fill_value=0)
inc = (g.loc[12] - g.loc[2]).sort_values(ascending=False)
print(f"Dec - Feb transaction count, total increase {inc.sum():,}:")
print(pd.DataFrame({"increase": inc, "share_of_increase_%": (100 * inc / inc.sum()).round(1),
                    "growth_%": (100 * (g.loc[12] / g.loc[2] - 1)).round(0)}).head(14).to_string())
yr = pd.to_datetime(tx2.activity_datetime).dt.year.value_counts().sort_index()
print("\nactivity_datetime years:\n", yr.to_string())
dec = pd.to_datetime(tx2.loc[tx2.transaction_month == 12, "activity_datetime"]).dt.year.value_counts().sort_index()
print("December rows by year:\n", dec.to_string())

## CELL 5
h("DEEP Q4 - Reach & habit of the two top categories")
top_cnt_cat, top_spend_cat = cat["count"].idxmax(), cat["sum"].idxmax()
nmon = tx2.groupby("consumer_id").transaction_month.nunique()
for c_ in [top_cnt_cat, top_spend_cat]:
    s = tx2[tx2.spending_category == c_]
    buyers = s.consumer_id.nunique()
    per = s.groupby(["consumer_id", "transaction_month"]).size()
    print(f"{c_}: {buyers}/999 consumers buy it ({100*buyers/999:.1f}%) | "
          f"{per.mean():.1f} purchases per buyer-month | active in {s.groupby('consumer_id').transaction_month.nunique().mean():.1f} months/yr")

## CELL 6
h("DEEP Q5 - Bootstrap 95% CI of mean FHS per age cohort (consumer level, all 999 incl. 7 minors)")
cons1 = mon.groupby("consumer_id").agg(fhs=("financial_health_score", "mean"), age=("age", "first"))
cons1["cohort"] = pd.cut(cons1.age, bins=bins, labels=labels)
rng = np.random.default_rng(42)
rows = []
for k, s in cons1.groupby("cohort", observed=True).fhs:
    bs = [rng.choice(s.values, len(s)).mean() for _ in range(1000)]
    rows.append((k, len(s), s.mean(), *np.percentile(bs, [2.5, 97.5])))
ci = pd.DataFrame(rows, columns=["cohort", "n", "mean_fhs", "ci_lo", "ci_hi"]).set_index("cohort")
print(ci.round(2).to_string())
lo_max, hi_min = ci.ci_lo.max(), ci.ci_hi.min()
print(f"All CIs overlap: {bool(lo_max <= hi_min)} (max lower {lo_max:.2f} vs min upper {hi_min:.2f})")
ci.to_csv("draft/task1_age_ci.csv")   # P2 dùng chung
assert ci.n.sum() == 999

## CELL 7
h("Slide 4 dataset check")
print(f"consumer-months {len(mon):,} | consumers {mon.consumer_id.nunique()} | transactions {len(txn):,} | "
      f"min age {mon.age.min()} | minors {mon.loc[mon.age < 18].consumer_id.nunique()}")
assert (len(mon), mon.consumer_id.nunique(), len(txn)) == (10992, 999, 1852394)
