"""
BI10 Round 01 - Group YAPPERS: deck charts (17 PNGs -> outputs/figures/).
Reproduces the numbers already reported in draft/task{1..5}_findings.md.
Run: PYTHONUTF8=1 py draft/make_charts.py
"""
import sys, os
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

DATA = "BI10_ROUND01_DATASET"
TXN = f"{DATA}/consumer_transactions_2025.parquet/consumer_transactions_2025.csv"
MON = f"{DATA}/consumer_financial_health_engagement_2025.csv"
FEAT = "draft/task4_features.csv"
OUT = "outputs/figures"
SEED = 42
os.makedirs(OUT, exist_ok=True)

# ---- shared style -----------------------------------------------------------
plt.rcParams.update({
    "figure.figsize": (10, 6), "figure.dpi": 150, "savefig.dpi": 150,
    "font.size": 11, "axes.titlesize": 15, "axes.titleweight": "bold",
    "axes.labelsize": 12, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linestyle": "-",
})
# palette (colour-blind-safe-ish, consistent across deck)
C = dict(primary="#2E5EAA", accent="#E4572E", pos="#8AA1C1", neg="#E4572E",
         good="#3C9D6E", warn="#E0A32E", muted="#9AA5B1", ink="#22303F")
SEG4 = ["#2E5EAA", "#E4572E", "#3C9D6E", "#E0A32E"]

def save(fig, name):
    fig.tight_layout()
    p = os.path.join(OUT, name)
    fig.savefig(p, bbox_inches="tight")
    plt.close(fig)
    print("wrote", p)

def barlabels(ax, bars, fmt="{:.0f}", dy=0, fs=10, color="#22303F"):
    for b in bars:
        h = b.get_height()
        ax.annotate(fmt.format(h), (b.get_x() + b.get_width() / 2, h),
                    xytext=(0, 3 + dy), textcoords="offset points",
                    ha="center", va="bottom", fontsize=fs, color=color)

CAT_EN = {
    "Xăng dầu và di chuyển": "Fuel & Transport",
    "Siêu thị và tạp hóa tại cửa hàng": "Groceries (in-store)",
    "Du lịch": "Travel", "Ăn uống": "Food & Dining",
    "Chăm sóc cá nhân": "Personal Care",
    "Dịch vụ trực tuyến khác": "Other Online Services",
    "Giải trí": "Entertainment",
    "Mua sắm khác tại cửa hàng": "Other In-store Shopping",
    "Mua sắm trực tuyến": "Online Shopping",
    "Mua sắm tại cửa hàng": "In-store Shopping",
    "Nhà cửa và tiện ích": "Home & Utilities",
    "Sức khỏe và thể thao": "Health & Sports",
    "Trẻ em và thú cưng": "Kids & Pets",
    "Tạp hóa trực tuyến": "Online Groceries",
}
SEG_EN = {
    "Financially Healthy & Highly Engaged": "Healthy &\nEngaged",
    "Financially Stretched but Highly Engaged": "Stretched &\nEngaged",
    "High-Activity Digital Power Users": "Digital\nPower Users",
    "Low Engagement & Emerging Digital": "Emerging\nDigital",
}
SEG_ORDER = list(SEG_EN)  # canonical order 351/302/258/88

# ---- load -------------------------------------------------------------------
print("loading data...")
mon = pd.read_csv(MON, parse_dates=["analysis_month"])
mon["month"] = mon["analysis_month"].dt.month
txn = pd.read_csv(TXN, usecols=["transaction_month", "spend_amount_vnd",
                                "transaction_channel", "spending_category"])
feat = pd.read_csv(FEAT)

# =============================================================================
# TASK 1
# =============================================================================
# t1_monthly_spend --------------------------------------------------------------
g = txn.groupby("transaction_month")["spend_amount_vnd"].agg(["sum", "count"])
g = g.reindex(range(1, 13))
fig, ax = plt.subplots()
colors = [C["accent"] if m == 12 else C["primary"] for m in g.index]
bars = ax.bar(g.index, g["sum"] / 1e9, color=colors)
ax.set_title("December is the year's spending engine")
ax.set_xlabel("Month"); ax.set_ylabel("Total spend (B VND)")
ax.set_xticks(range(1, 13))
ax.annotate("Dec = 15.0% of annual\n(2.8x the Feb trough)", (0.62, 0.86),
            xycoords="axes fraction", ha="left", color=C["accent"],
            fontsize=10, fontweight="bold")
ax2 = ax.twinx(); ax2.grid(False)
ax2.plot(g.index, g["count"] / 1e3, color=C["ink"], marker="o", lw=2, label="Transactions")
ax2.set_ylabel("Transactions (thousands)")
ax2.legend(loc="upper left", frameon=False)
save(fig, "t1_monthly_spend.png")

# t1_essential_discretionary ---------------------------------------------------
def compo(sub):
    e, d = sub["essential_spend_vnd"].sum(), sub["discretionary_spend_vnd"].sum()
    t = e + d
    return 100 * e / t, 100 * d / t
segs = {"Stressed\n(FHS < 40)": mon[mon.financial_health_score < 40],
        "Healthy\n(FHS >= 80)": mon[mon.financial_health_score >= 80]}
ess = [compo(s)[0] for s in segs.values()]
dis = [compo(s)[1] for s in segs.values()]
fig, ax = plt.subplots(figsize=(8, 6))
x = np.arange(len(segs))
b1 = ax.bar(x, ess, color=C["good"], label="Essential")
b2 = ax.bar(x, dis, bottom=ess, color=C["accent"], label="Discretionary")
for i in range(len(segs)):
    ax.text(i, ess[i] / 2, f"{ess[i]:.1f}%", ha="center", va="center",
            color="white", fontweight="bold")
    ax.text(i, ess[i] + dis[i] / 2, f"{dis[i]:.1f}%", ha="center", va="center",
            color="white", fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(segs.keys())
ax.set_ylabel("Share of spend (%)"); ax.set_ylim(0, 100)
ax.set_title("Financial stress inverts the budget mix")
ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.08))
save(fig, "t1_essential_discretionary.png")

# t1_category_ticket -----------------------------------------------------------
cat = txn.groupby("spending_category")["spend_amount_vnd"].agg(["sum", "count"])
cat["ticket"] = cat["sum"] / cat["count"]
cat.index = [CAT_EN.get(i, i) for i in cat.index]
top_cnt = cat["count"].idxmax(); top_spend = cat["sum"].idxmax()
fig, ax = plt.subplots()
sizes = 60 + 900 * cat["sum"] / cat["sum"].max()
cols = [C["accent"] if i == top_spend else (C["good"] if i == top_cnt else C["muted"])
        for i in cat.index]
ax.scatter(cat["count"] / 1e3, cat["ticket"] / 1e6, s=sizes, c=cols, alpha=0.8,
           edgecolors="white", linewidths=0.8, zorder=3)
for i, r in cat.iterrows():
    if i in (top_cnt, top_spend) or r["count"] > 90e3 or r["ticket"] > 2.6e6:
        ax.annotate(i, (r["count"] / 1e3, r["ticket"] / 1e6), xytext=(6, 6),
                    textcoords="offset points", fontsize=9)
ax.set_xlabel("Transactions (thousands)"); ax.set_ylabel("Avg ticket (M VND)")
ax.set_title("Frequency vs value: Fuel (habit) vs Groceries (basket)")
ax.annotate("bubble size = total spend", (0.98, 0.02), xycoords="axes fraction",
            ha="right", fontsize=9, color=C["muted"])
save(fig, "t1_category_ticket.png")

# t1_age_cohort ----------------------------------------------------------------
bins = [14, 24, 34, 44, 54, 64, 200]
labels = ["15-24", "25-34", "35-44", "45-54", "55-64", "65+"]
mon["cohort"] = pd.cut(mon.age, bins=bins, labels=labels)
coh = mon.groupby("cohort", observed=True).agg(
    fhs=("financial_health_score", "mean"), txn=("transaction_count", "mean"),
    s2i=("spend_to_income_ratio", "mean"))
fig, ax = plt.subplots()
x = np.arange(len(coh))
cols = [C["accent"] if c == "25-34" else C["pos"] for c in coh.index]
bars = ax.bar(x, coh["txn"], color=cols, label="Avg txns/mo")
barlabels(ax, bars, "{:.0f}")
ax.set_xticks(x); ax.set_xticklabels(coh.index)
ax.set_ylabel("Avg transactions / month"); ax.set_xlabel("Age cohort")
ax.set_title("25-34: active, but the lowest financial health")
ax2 = ax.twinx(); ax2.grid(False)
ax2.plot(x, coh["fhs"], color=C["ink"], marker="o", lw=2, label="Avg FHS")
ax2.set_ylabel("Avg financial health score"); ax2.set_ylim(64, 68)
l1, la1 = ax.get_legend_handles_labels(); l2, la2 = ax2.get_legend_handles_labels()
ax.legend(l1 + l2, la1 + la2, frameon=False, loc="upper right")
save(fig, "t1_age_cohort.png")

# =============================================================================
# TASK 2
# =============================================================================
# t2_fhs_distribution ----------------------------------------------------------
fig, ax = plt.subplots()
fhs = mon["financial_health_score"]
n, bins_, patches = ax.hist(fhs, bins=40, color=C["primary"], edgecolor="white")
for b, p in zip(bins_[:-1], patches):
    if b < 40:
        p.set_facecolor(C["accent"])
ax.axvline(40, color=C["accent"], ls="--", lw=1.5)
ax.axvspan(fhs.min(), 40, color=C["accent"], alpha=0.07)
ax.set_title("Financial health: a tight band around 66; distress is episodic")
ax.set_xlabel("Financial health score (consumer-month)"); ax.set_ylabel("Consumer-months")
ax.annotate("FHS < 40 (stressed):\n95 of 10,992 months (0.9%)", (40, ax.get_ylim()[1] * 0.7),
            xytext=(50, ax.get_ylim()[1] * 0.75), color=C["accent"], fontsize=10,
            fontweight="bold", arrowprops=dict(arrowstyle="->", color=C["accent"]))
save(fig, "t2_fhs_distribution.png")

# t2_low_health_drivers --------------------------------------------------------
RATIOS = ["spend_to_income_ratio", "credit_utilization_ratio", "essential_spend_ratio",
          "discretionary_spend_ratio", "online_spend_ratio", "spending_volatility",
          "category_diversity", "engagement_score", "transaction_recency_days",
          "average_transaction_value_vnd", "active_transaction_days"]
corr = mon[["financial_health_score"] + RATIOS].corr()["financial_health_score"].drop("financial_health_score")
corr = corr.reindex(corr.abs().sort_values().index)  # ascending for barh
fig, ax = plt.subplots()
cols = [C["neg"] if v < 0 else C["good"] for v in corr]
bars = ax.barh(range(len(corr)), corr.values, color=cols)
ax.set_yticks(range(len(corr)))
ax.set_yticklabels([c.replace("_", " ") for c in corr.index])
ax.axvline(0, color=C["ink"], lw=0.8)
for i, v in enumerate(corr.values):
    ax.text(v + (0.02 if v >= 0 else -0.02), i, f"{v:+.2f}",
            va="center", ha="left" if v >= 0 else "right", fontsize=9)
ax.set_xlim(-1.05, 0.75)
ax.set_xlabel("Pearson correlation with financial health score")
ax.set_title("Low health is an overspend story (spend/income, credit-util)")
save(fig, "t2_low_health_drivers.png")

# t2_crossover -----------------------------------------------------------------
eng_p75 = mon.engagement_score.quantile(0.75)
fig, ax = plt.subplots()
ax.scatter(mon.engagement_score, mon.financial_health_score, s=8, alpha=0.15,
           color=C["muted"], zorder=1)
cross = mon[(mon.financial_health_score < 40) & (mon.engagement_score >= eng_p75)]
ax.scatter(cross.engagement_score, cross.financial_health_score, s=28, alpha=0.9,
           color=C["accent"], zorder=3, label="Stressed & engaged")
ax.axhline(40, color=C["ink"], ls="--", lw=1)
ax.axvline(eng_p75, color=C["ink"], ls="--", lw=1)
ax.add_patch(Rectangle((eng_p75, 0), mon.engagement_score.max() - eng_p75, 40,
                       fill=False, edgecolor=C["accent"], lw=2, zorder=2))
ax.set_xlabel("Engagement score"); ax.set_ylabel("Financial health score")
ax.set_title("Crossover: stressed BUT highly engaged")
ax.annotate(f"FHS < 40 & engagement >= {eng_p75:.1f}\n43 consumers = 52% of all stress",
            (eng_p75, 40), xytext=(-160, 25), textcoords="offset points",
            color=C["accent"], fontsize=10, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=C["accent"]))
ax.legend(frameon=False, loc="lower left")
save(fig, "t2_crossover.png")

# =============================================================================
# TASK 3
# =============================================================================
# t3_engagement_dist -----------------------------------------------------------
fig, (ax, axb) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [2, 1]})
ax.hist(mon.engagement_score, bins=40, color=C["primary"], edgecolor="white")
ax.set_title("Engagement is saturated high (thin low tail)")
ax.set_xlabel("Engagement score (consumer-month)"); ax.set_ylabel("Consumer-months")
seg = mon["engagement_segment"].value_counts()
seg_map = {"Tương tác rất cao": "Very high", "Tương tác cao": "High",
           "Tương tác trung bình": "Medium", "Tương tác thấp": "Low"}
order = ["Tương tác rất cao", "Tương tác cao", "Tương tác trung bình", "Tương tác thấp"]
seg = seg.reindex([o for o in order if o in seg.index])
shares = 100 * seg / seg.sum()
segcol = {"Very high": C["good"], "High": C["primary"], "Medium": C["warn"], "Low": C["accent"]}
bottom = 0
for name, sh in zip(seg.index, shares):
    en = seg_map.get(name, name)
    axb.bar(0, sh, bottom=bottom, color=segcol[en], width=0.5, label=f"{en} ({sh:.1f}%)")
    if sh > 3:
        axb.text(0, bottom + sh / 2, f"{en}\n{sh:.1f}%", ha="center", va="center",
                 color="white", fontweight="bold", fontsize=9)
    bottom += sh
axb.set_ylim(0, 100); axb.set_xlim(-0.5, 0.5); axb.set_xticks([])
axb.set_ylabel("Share of consumer-months (%)"); axb.set_title("Segment shares")
axb.legend(frameon=False, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=2)
save(fig, "t3_engagement_dist.png")

# t3_channel_mix ---------------------------------------------------------------
ch = txn["transaction_channel"].value_counts()
shares = 100 * ch / ch.sum()
fig, ax = plt.subplots()
cols = [C["muted"] if k == "POS" else C["primary"] for k in ch.index]
bars = ax.bar(range(len(ch)), shares.values, color=cols)
barlabels(ax, bars, "{:.1f}%")
ax.set_xticks(range(len(ch))); ax.set_xticklabels(ch.index, rotation=15, ha="right")
ax.set_ylabel("Share of transactions (%)")
ax.set_title("Channel mix: POS owns the base, QR the second rail")
ax.annotate("Digital = 41.2% of trips\n(only 21% of spend value)", (0.97, 0.9),
            xycoords="axes fraction", ha="right", fontsize=10, color=C["ink"])
save(fig, "t3_channel_mix.png")

# t3_diversity_vs_engagement ---------------------------------------------------
con = mon.groupby("consumer_id").agg(div=("category_diversity", "mean"),
                                     eng=("engagement_score", "mean"))
r = con["div"].corr(con["eng"])
fig, ax = plt.subplots()
ax.scatter(con["div"], con["eng"], s=18, alpha=0.4, color=C["primary"], edgecolors="none")
m, b = np.polyfit(con["div"], con["eng"], 1)
xs = np.array([con["div"].min(), con["div"].max()])
ax.plot(xs, m * xs + b, color=C["accent"], lw=2)
ax.set_xlabel("Category diversity (consumer avg)"); ax.set_ylabel("Engagement score (consumer avg)")
ax.set_title("Category diversity is the cleanest engagement signal")
ax.annotate(f"r = {r:.2f}", (0.05, 0.9), xycoords="axes fraction", fontsize=14,
            fontweight="bold", color=C["accent"])
save(fig, "t3_diversity_vs_engagement.png")

# t3_health_vs_engagement_quadrant ---------------------------------------------
fig, ax = plt.subplots()
dorm = feat[(feat.financial_health_score >= 70) & (feat.engagement_score < 70)]
other = feat.drop(dorm.index)
ax.scatter(other.engagement_score, other.financial_health_score, s=16, alpha=0.4,
           color=C["muted"], edgecolors="none")
ax.scatter(dorm.engagement_score, dorm.financial_health_score, s=45, alpha=0.9,
           color=C["accent"], edgecolors="white", linewidths=0.6,
           label=f"High-health / low-engagement ({len(dorm)})")
ax.axhline(70, color=C["ink"], ls="--", lw=1); ax.axvline(70, color=C["ink"], ls="--", lw=1)
ax.set_xlabel("Engagement score (consumer avg)"); ax.set_ylabel("Financial health score (consumer avg)")
ax.set_title("Health x engagement: the 25 healthy-but-dormant customers")
ax.legend(frameon=False, loc="lower left")
save(fig, "t3_health_vs_engagement_quadrant.png")

# =============================================================================
# TASK 4
# =============================================================================
# t4_segment_sizes -------------------------------------------------------------
sz = feat["segment"].value_counts().reindex(SEG_ORDER)
fig, ax = plt.subplots()
bars = ax.bar([SEG_EN[s] for s in SEG_ORDER], sz.values, color=SEG4)
for b, n in zip(bars, sz.values):
    ax.annotate(f"{n}\n{100*n/999:.1f}%", (b.get_x() + b.get_width() / 2, n),
                xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                fontsize=10, fontweight="bold")
ax.set_ylabel("Consumers"); ax.set_title("Four behavioural segments (999 consumers)")
ax.set_ylim(0, sz.max() * 1.15)
save(fig, "t4_segment_sizes.png")

# t4_segment_profiles (z-scored heatmap) ---------------------------------------
FEATS = ["financial_health_score", "spend_to_income_ratio", "credit_utilization_ratio",
         "spending_volatility", "engagement_score", "transaction_count",
         "discretionary_spend_ratio", "online_spend_ratio"]
FEAT_LBL = ["Financial health", "Spend / income", "Credit utilization", "Volatility",
            "Engagement", "Txns / month", "Discretionary ratio", "Online ratio"]
prof = feat.groupby("segment")[FEATS].mean().reindex(SEG_ORDER)
z = (prof - prof.mean()) / prof.std()
fig, ax = plt.subplots(figsize=(11, 6))
im = ax.imshow(z.values.T, cmap="RdBu_r", aspect="auto", vmin=-1.6, vmax=1.6)
ax.set_xticks(range(len(SEG_ORDER)))
ax.set_xticklabels([SEG_EN[s] for s in SEG_ORDER])
ax.set_yticks(range(len(FEATS))); ax.set_yticklabels(FEAT_LBL)
for i in range(len(SEG_ORDER)):
    for j in range(len(FEATS)):
        ax.text(i, j, f"{prof.values[i, j]:.2f}", ha="center", va="center",
                color="black", fontsize=9)
ax.set_title("Segment profiles (cell = raw mean; colour = z-score across segments)")
fig.colorbar(im, ax=ax, shrink=0.7, label="z-score (relative to segment means)")
ax.grid(False)
save(fig, "t4_segment_profiles.png")

# t4_silhouette (recompute elbow + silhouette, k=2..8) -------------------------
X = StandardScaler().fit_transform(feat[FEATS].values)
ks = range(2, 9); inertia, sil = [], []
for k in ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(X)
    inertia.append(km.inertia_); sil.append(silhouette_score(X, km.labels_))
fig, ax = plt.subplots()
ax.plot(list(ks), inertia, marker="o", color=C["primary"], label="Inertia (elbow)")
ax.set_xlabel("k (number of clusters)"); ax.set_ylabel("Inertia", color=C["primary"])
ax.tick_params(axis="y", labelcolor=C["primary"])
ax2 = ax.twinx(); ax2.grid(False)
ax2.plot(list(ks), sil, marker="s", color=C["accent"], label="Silhouette")
ax2.set_ylabel("Silhouette score", color=C["accent"])
ax2.tick_params(axis="y", labelcolor=C["accent"])
ax.axvline(4, color=C["good"], ls="--", lw=1.5)
ax.annotate("k = 4 chosen\n(elbow + best silhouette in 4-6)", (4, inertia[2]),
            xytext=(20, 20), textcoords="offset points", color=C["good"],
            fontweight="bold", fontsize=10, arrowprops=dict(arrowstyle="->", color=C["good"]))
ax.set_title("Choosing k: elbow (inertia) + silhouette")
save(fig, "t4_silhouette.png")

# =============================================================================
# TASK 5
# =============================================================================
tools = pd.DataFrame([
    ("1 Budgeting", "Stretched & Engaged", 302, 0.90, "Wellbeing"),
    ("2 Spend alerts", "Stressed-Engaged crossover", 43, 0.86, "Wellbeing"),
    ("3 Planning reminders", "Digital Power Users", 258, 0.50, "Wellbeing"),
    ("4 Education", "Distress tail", 67, 0.48, "Wellbeing"),
    ("5 Digital nudges", "Emerging Digital", 88, 0.94, "Growth"),
    ("6 Product suggestions", "Healthy & Engaged", 351, 0.15, "Growth"),
], columns=["tool", "target", "reach", "driver", "track"])

# t5_priority_ranking (reach x driver strength bubble) -------------------------
fig, ax = plt.subplots()
for track, col in [("Wellbeing", C["accent"]), ("Growth", C["primary"])]:
    d = tools[tools.track == track]
    ax.scatter(d.reach, d.driver, s=80 + 3 * d.reach, color=col, alpha=0.7,
               edgecolors="white", linewidths=1, label=track, zorder=3)
for _, r in tools.iterrows():
    left = r.reach > 240  # keep right-side labels inside the axes
    ax.annotate(r.tool, (r.reach, r.driver),
                xytext=(-10 if left else 8, 8), textcoords="offset points",
                ha="right" if left else "left", fontsize=9, fontweight="bold")
ax.set_xlim(10, 400)
ax.set_xlabel("Reach (consumers targeted)")
ax.set_ylabel("Driver strength (|corr| with FHS, or key signal)")
ax.set_title("Tool prioritization: reach x driver strength")
ax.legend(frameon=False, title="Track", loc="center", bbox_to_anchor=(0.46, 0.78))
ax.annotate("bubble size ~ reach", (0.02, 0.02), xycoords="axes fraction",
            fontsize=9, color=C["muted"])
save(fig, "t5_priority_ranking.png")

# t5_target_sizes --------------------------------------------------------------
ts = tools.sort_values("reach", ascending=False)
fig, ax = plt.subplots()
cols = [C["accent"] if t == "Wellbeing" else C["primary"] for t in ts.track]
bars = ax.bar(range(len(ts)), ts.reach, color=cols)
for b, n in zip(bars, ts.reach):
    ax.annotate(f"{n}\n{100*n/999:.1f}%", (b.get_x() + b.get_width() / 2, n),
                xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                fontsize=10, fontweight="bold")
ax.set_xticks(range(len(ts)))
ax.set_xticklabels([f"{t}\n->{tg}" for t, tg in zip(ts.tool, ts.target)],
                   rotation=20, ha="right", fontsize=8)
ax.set_ylabel("Target group size (consumers)")
ax.set_ylim(0, ts.reach.max() * 1.18)
ax.set_title("Target group size per tool")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=C["accent"], label="Wellbeing"),
                   Patch(color=C["primary"], label="Growth")], frameon=False)
save(fig, "t5_target_sizes.png")

print("\nDONE. Files in", OUT)
