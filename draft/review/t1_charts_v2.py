"""v2 Task 1 charts (review proposal). Run: PYTHONUTF8=1 py draft/review/t1_charts_v2.py
Saves outputs/figures/v2_t1_*.png. Standalone: does not touch existing charts.
"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

sys.stdout.reconfigure(encoding="utf-8")
PRI, ACC, GOOD, WARN, MUTED = "#2E5EAA", "#E4572E", "#3C9D6E", "#E0A32E", "#9AA5B1"
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.alpha": 0.3, "font.size": 11})
OUT = "outputs/figures/"
D = "BI10_ROUND01_DATASET/"
CAT_EN = {"Xăng dầu và di chuyển": "Fuel & Transport", "Siêu thị và tạp hóa tại cửa hàng": "Groceries (in-store)",
          "Du lịch": "Travel", "Ăn uống": "Food & Dining", "Chăm sóc cá nhân": "Personal Care",
          "Dịch vụ trực tuyến khác": "Other Online Services", "Giải trí": "Entertainment",
          "Mua sắm khác tại cửa hàng": "Other In-store Shopping", "Mua sắm trực tuyến": "Online Shopping",
          "Mua sắm tại cửa hàng": "In-store Shopping", "Nhà cửa và tiện ích": "Home & Utilities",
          "Sức khỏe và thể thao": "Health & Sports", "Trẻ em và thú cưng": "Kids & Pets",
          "Tạp hóa trực tuyến": "Online Groceries"}
PROV_EN = {"Hà Nội": "Ha Noi", "Đồng Nai": "Dong Nai", "Lâm Đồng": "Lam Dong", "Hưng Yên": "Hung Yen",
           "Hải Phòng": "Hai Phong", "Nghệ An": "Nghe An", "Thành phố Hồ Chí Minh": "HCMC",
           "Cao Bằng": "Cao Bang", "Quảng Ngãi": "Quang Ngai"}

m = pd.read_csv(D + "consumer_financial_health_engagement_2025.csv")
m["month"] = pd.to_datetime(m.analysis_month).dt.month
t = pd.read_csv(D + "consumer_transactions_2025.parquet/consumer_transactions_2025.csv",
                usecols=["consumer_id", "province_city", "spending_category", "spend_amount_vnd",
                         "transaction_channel", "online_transaction_flag", "essential_spending_flag", "transaction_month"])
t["cat"] = t.spending_category.map(CAT_EN)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT + name, dpi=150)
    plt.close(fig)
    print("saved", name)


# ---- Q1: spend = consumers x trips/consumer x ticket, indexed to February ----
mo = t.groupby("transaction_month").agg(spend=("spend_amount_vnd", "sum"), n=("spend_amount_vnd", "size"),
                                        cons=("consumer_id", "nunique"))
mo["ticket"] = mo.spend / mo.n
mo["trips"] = mo.n / mo.cons
idx = mo / mo.loc[2] * 100
fig, ax = plt.subplots(figsize=(8, 5.2))
series = [("spend", "Total spend", ACC, 3), ("trips", "Transactions per active consumer", PRI, 2.2),
          ("cons", "Active consumers", MUTED, 2), ("ticket", "Average ticket", GOOD, 2)]
for col, lab, c, lw in series:
    ax.plot(idx.index, idx[col], marker="o", color=c, lw=lw, label=lab)
    ax.annotate(f"{idx.loc[12, col]:.0f}", (12, idx.loc[12, col]), xytext=(8, {"cons": 6, "ticket": -6}.get(col, 0)), textcoords="offset points",
                va="center", color=c, fontweight="bold")
ax.axhline(100, color="black", lw=0.8)
ax.set_xticks(range(1, 13)); ax.set_xticklabels("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())
ax.set_xlim(0.6, 12.9)
ax.set_ylabel("Index, February (lowest month) = 100")
ax.set_title("December peak = the same customers transacting 2.9x as often", fontweight="bold")
ax.legend(loc="upper left", frameon=False)
save(fig, "v2_t1_q1_decomposition.png")

# ---- Q2: where the discretionary shift goes (value share, stressed minus healthy) ----
tm = t.merge(m[["consumer_id", "month", "financial_health_score"]], left_on=["consumer_id", "transaction_month"],
             right_on=["consumer_id", "month"])
tm["seg"] = np.select([tm.financial_health_score < 40, tm.financial_health_score >= 80], ["S", "H"], "M")
x = tm[tm.seg != "M"]
sh = x.pivot_table(index="cat", columns="seg", values="spend_amount_vnd", aggfunc="sum")
sh = sh / sh.sum() * 100
tk = x.pivot_table(index="cat", columns="seg", values="spend_amount_vnd", aggfunc="mean") / 1e6
ess = t.groupby("cat").essential_spending_flag.first()
d = (sh.S - sh.H).sort_values()
fig, ax = plt.subplots(figsize=(8, 5.6))
cols = [GOOD if ess[c] == 1 else ACC for c in d.index]
ax.barh(d.index, d.values, color=cols)
for i, (c, v) in enumerate(d.items()):
    ax.text(max(v, 0) + 0.4, i, f"{v:+.1f}pp  (ticket {tk.loc[c, 'S']:.1f}M vs {tk.loc[c, 'H']:.1f}M)",
            va="center", ha="left", fontsize=8.5)
ax.axvline(0, color="black", lw=0.8)
ax.set_xlim(-10, 45)
ax.set_xlabel("Share of spend value: stressed months minus healthy months (pp)")
ax.set_title("Stress = big-ticket discretionary splurges (Travel +22pp)", fontweight="bold")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=GOOD, label="Essential"), Patch(color=ACC, label="Discretionary")],
          loc="center right", frameon=False)
ax.grid(axis="y", visible=False)
save(fig, "v2_t1_q2_category_shift.png")

# ---- Q3: channel gap vs national (pp) for qualifying provinces + top/bottom references ----
t["digital"] = (t.transaction_channel != "POS").astype(int)
nat = t.transaction_channel.value_counts(normalize=True) * 100
nat_d = t.digital.mean() * 100
pv = t.groupby("province_city").agg(spend=("spend_amount_vnd", "sum"), dig=("digital", "mean"))
pv["dig"] *= 100
sel = pv[(pv.spend > pv.spend.median()) & (pv.dig < nat_d)].sort_values("spend", ascending=False)
print("qualifying:", sel.index.tolist())
# robustness: online_transaction_flag definition (QR counted as offline)
on = t.groupby("province_city").online_transaction_flag.mean() * 100
nat_on = t.online_transaction_flag.mean() * 100
print(f"online-flag national {nat_on:.2f}%; qualifying under that definition:",
      pv[(pv.spend > pv.spend.median()) & (on < nat_on)].index.tolist(),
      "gaps:", (on[sel.index] - nat_on).round(2).to_dict())
rows = list(sel.index) + ["Thành phố Hồ Chí Minh", "Cao Bằng", "Quảng Ngãi"]
chs = ["POS", "QR Payment", "E-commerce", "Mobile App", "Recurring Payment"]
ct = pd.crosstab(t.province_city, t.transaction_channel, normalize="index")[chs] * 100
gap = ct.loc[rows].sub(nat[chs], axis=1)
gap["Digital total"] = pv.loc[rows, "dig"] - nat_d
share = pv.spend / pv.spend.sum() * 100
labels = [f"{PROV_EN[r]} ({share[r]:.1f}% of spend)" for r in rows]
cmap = LinearSegmentedColormap.from_list("div", [ACC, "#FFFFFF", PRI])
fig, ax = plt.subplots(figsize=(8.6, 5.4))
ax.imshow(gap.values, cmap=cmap, vmin=-2, vmax=2, aspect="auto")
for i in range(gap.shape[0]):
    for j in range(gap.shape[1]):
        ax.text(j, i, f"{gap.values[i, j]:+.2f}", ha="center", va="center", fontsize=9.5,
                fontweight="bold" if j == gap.shape[1] - 1 else "normal")
ax.set_xticks(range(gap.shape[1]))
ax.set_xticklabels(["POS", "QR", "E-com", "Mobile\nApp", "Recurring", "Digital\ntotal"])
ax.set_yticks(range(len(rows))); ax.set_yticklabels(labels, fontsize=9.5)
ax.axhline(len(sel) - 0.5, color="black", lw=1.5)
ax.text(-0.45, len(sel) - 0.55, "below line: references (top spend / most / least digital)", ha="left",
        va="bottom", fontsize=8, color="#555555", style="italic")
ax.grid(False)
ax.set_title(f"Channel mix gap vs national, pp of transactions (national digital {nat_d:.1f}%)",
             fontweight="bold", fontsize=11.5)
save(fig, "v2_t1_q3_channel_gap.png")

# ---- Q4: category map, every bubble labelled ----
c = t.groupby("cat").agg(n=("spend_amount_vnd", "size"), spend=("spend_amount_vnd", "sum"))
c["ticket"] = c.spend / c.n / 1e6
fig, ax = plt.subplots(figsize=(8, 5.4))
top_n, top_s = c.n.idxmax(), c.spend.idxmax()
for k, r in c.iterrows():
    col = GOOD if k == top_n else ACC if k == top_s else MUTED
    ax.scatter(r.n / 1e3, r.ticket, s=r.spend / 1e9 * 3, color=col, alpha=0.85, edgecolor="white")
    ax.annotate(k, (r.n / 1e3, r.ticket), xytext={"Other In-store Shopping": (-30, 12), "Kids & Pets": (0, -18), "Health & Sports": (-20, -20), "Personal Care": (0, -20), "Food & Dining": (30, 8)}.get(k, (0, 10)),
                textcoords="offset points", ha="center", fontsize=8.5,
                fontweight="bold" if k in (top_n, top_s) else "normal")
ax.axhline(t.spend_amount_vnd.mean() / 1e6, color="black", lw=0.8, ls="--")
ax.text(56, t.spend_amount_vnd.mean() / 1e6 + 0.03, "overall avg ticket 1.75M", fontsize=8.5)
ax.set_xlabel("Transactions (thousands)"); ax.set_ylabel("Average ticket (M VND)")
ax.set_ylim(1.05, 3.15)
ax.set_title("Fuel = most frequent habit; Groceries = biggest wallet (bubble = spend)", fontweight="bold", fontsize=11.5)
save(fig, "v2_t1_q4_category.png")

# ---- Q5: FHS by cohort with consumer-cluster bootstrap CI + the two ratios ----
labs = ["15-24", "25-34", "35-44", "45-54", "55-64", "65+"]
m["coh"] = pd.cut(m.age, [0, 24, 34, 44, 54, 64, 200], labels=labs)
rng = np.random.default_rng(0)
res = []
for k in labs:
    g = m[m.coh == k]
    per = g.groupby("consumer_id").financial_health_score.agg(["sum", "size"])
    b = rng.integers(0, len(per), (3000, len(per)))
    bs = per["sum"].values[b].sum(1) / per["size"].values[b].sum(1)   # month-weighted mean, resampling consumers
    res.append((k, g.financial_health_score.mean(), *np.percentile(bs, [2.5, 97.5]),
                g.spend_to_income_ratio.mean(), g.essential_spend_ratio.mean(), g.transaction_count.mean()))
r = pd.DataFrame(res, columns=["coh", "fhs", "lo", "hi", "sti", "ess", "txn"]).set_index("coh")
print(r.round(3).to_string())
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.6), gridspec_kw={"width_ratios": [1, 1.1]})
cc = [ACC if k == "25-34" else PRI for k in labs]
a1.errorbar(range(6), r.fhs, yerr=[r.fhs - r.lo, r.hi - r.fhs], fmt="none", ecolor=MUTED, capsize=4, lw=1.5)
a1.scatter(range(6), r.fhs, color=cc, s=60, zorder=3)
for i, v in enumerate(r.fhs):
    a1.text(i + 0.12, v, f"{v:.1f}", va="center", fontsize=9)
a1.set_xticks(range(6)); a1.set_xticklabels(labs)
a1.set_ylim(60, 70); a1.set_ylabel("Mean FHS (95% CI)")
a1.set_title("FHS: 1.2-pt spread, CIs overlap", fontweight="bold", fontsize=11)
w = 0.38
a2.bar(np.arange(6) - w / 2, r.sti, w, color=cc, label="Spend-to-income")
a2.bar(np.arange(6) + w / 2, r.ess, w, color=[WARN if k == "25-34" else MUTED for k in labs], label="Essential ratio")
for i in range(6):
    a2.text(i - w / 2, r.sti.iloc[i] + 0.01, f"{r.sti.iloc[i]:.3f}", ha="center", fontsize=7.5, rotation=90, va="bottom")
    a2.text(i + w / 2, r.ess.iloc[i] + 0.01, f"{r.ess.iloc[i]:.3f}", ha="center", fontsize=7.5, rotation=90, va="bottom")
a2.axhline(m.spend_to_income_ratio.mean(), color=PRI, ls="--", lw=0.8)
a2.axhline(m.essential_spend_ratio.mean(), color="#555555", ls=":", lw=0.8)
a2.set_xticks(range(6)); a2.set_xticklabels(labs); a2.set_ylim(0, 1.0)
a2.set_title("Ratios (dashed = national)", fontweight="bold", fontsize=11)
a2.legend(frameon=False, fontsize=8.5, loc="upper center", ncol=2)
save(fig, "v2_t1_q5_age.png")
