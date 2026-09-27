"""
Task 4 v2 charts (review proposal). Self-contained: refits the deck's k-means (k=4, seed 42).
Run: PYTHONUTF8=1 py draft/review/t4_charts_v2.py  -> outputs/figures/v2_t4_*.png
"""
import sys, numpy as np, pandas as pd, matplotlib
sys.stdout.reconfigure(encoding="utf-8")
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

MON = "BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv"
TX = "BI10_ROUND01_DATASET/consumer_transactions_2025.parquet/consumer_transactions_2025.csv"
OUT = "outputs/figures/v2_t4_"
F = ["financial_health_score", "spend_to_income_ratio", "credit_utilization_ratio", "spending_volatility",
     "engagement_score", "transaction_count", "discretionary_spend_ratio", "online_spend_ratio"]
ORDER = ["Healthy & Engaged", "Stretched & Engaged", "High-Activity Users", "Occasional Online-First"]
COL = dict(zip(ORDER, ["#2E5EAA", "#E4572E", "#3C9D6E", "#E0A32E"]))
INK, MUTED = "#222222", "#666666"
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": "#e6e6e6", "grid.linewidth": .6, "axes.axisbelow": True,
                     "font.size": 10, "axes.titlesize": 12, "axes.titleweight": "bold",
                     "axes.edgecolor": "#999999", "text.color": INK, "axes.labelcolor": INK})

mon = pd.read_csv(MON); mon["m"] = pd.to_datetime(mon.analysis_month).dt.month
cons = mon.groupby("consumer_id")[F].mean()
X = StandardScaler().fit_transform(cons)
km = KMeans(4, n_init=25, random_state=42).fit(X); lab = km.labels_
prof = cons.groupby(lab)[F].mean()
name = {prof.financial_health_score.idxmax(): ORDER[0], prof.spend_to_income_ratio.idxmax(): ORDER[1],
        prof.transaction_count.idxmax(): ORDER[2], prof.engagement_score.idxmin(): ORDER[3]}
cons["seg"] = pd.Series(lab, index=cons.index).map(name)
assert cons.seg.notna().all() and cons.seg.value_counts()[ORDER].tolist() == [351, 302, 258, 88]
mon["seg"] = mon.consumer_id.map(cons.seg)
n = cons.seg.value_counts()[ORDER]

# ---- 1. k selection: silhouette + what each extra cluster separates
ks = range(2, 9)
sil = [silhouette_score(X, KMeans(k, n_init=10, random_state=42).fit_predict(X)) for k in ks]
fig, ax = plt.subplots(figsize=(6.2, 4.2))
ax.plot(list(ks), sil, color="#2E5EAA", lw=2, marker="o", ms=7, zorder=3)
ax.plot(4, sil[2], "o", ms=13, mfc="none", mec="#E4572E", mew=2, zorder=4)
notes = {2: "k=2: 88 part-year\ncustomers vs the rest", 3: "k=3: + health split\n(healthy vs stretched)",
         4: "k=4: + activity split\n(chosen)"}
for k, t in notes.items():
    ax.annotate(t, (k, sil[k - 2]), xytext=(12, 8 if k != 3 else 14), textcoords="offset points", fontsize=8.5, color=INK)
for k, s in zip(ks, sil):
    ax.annotate(f"{s:.2f}", (k, s), xytext=(0, -15), textcoords="offset points", ha="center", fontsize=8, color=MUTED)
ax.set(xlabel="Number of clusters k", ylabel="Silhouette (higher = better separated)", ylim=(0, .65))
ax.set_title("Each added cluster separates a new business axis", loc="left")
fig.tight_layout(); fig.savefig(OUT + "k_selection.png", dpi=150); plt.close(fig)

# ---- 2. sizes (horizontal, direct-labelled)
fig, ax = plt.subplots(figsize=(5.2, 3.6))
y = np.arange(4)[::-1]
ax.barh(y, n.values, color=[COL[s] for s in ORDER], height=.62)
for yi, s in zip(y, ORDER):
    ax.text(n[s] + 6, yi, f"{n[s]}  ({n[s] / 9.99:.1f}%)", va="center", fontsize=9.5, color=INK)
ax.set_yticks(y, ORDER); ax.set_xlim(0, 500); ax.grid(axis="y", visible=False)
ax.set_xlabel("Consumers (total 999, 100% covered)")
ax.set_title("Segment sizes", loc="left")
fig.tight_layout(); fig.savefig(OUT + "sizes.png", dpi=150); plt.close(fig)

# ---- 3. side-by-side profile heatmap: clustering inputs + profile-only columns
tx = pd.read_csv(TX, usecols=["consumer_id", "transaction_channel", "spend_amount_vnd"])
tx["seg"] = tx.consumer_id.map(cons.seg)
v = tx.groupby(["seg", "transaction_channel"]).spend_amount_vnd.sum().unstack()
nonpos = 1 - v["POS"] / v.sum(1)
nm = mon.groupby("consumer_id").size()
demo = mon.groupby("consumer_id")[["age", "gender"]].first()
stress = mon.groupby("consumer_id").financial_health_score.min().lt(40)
rows = {  # label -> (series by seg, fmt, is_input)
    "Financial health score": (cons.groupby("seg").financial_health_score.mean(), "{:.1f}", 1),
    "Spend / income": (cons.groupby("seg").spend_to_income_ratio.mean(), "{:.2f}", 1),
    "Credit utilization": (cons.groupby("seg").credit_utilization_ratio.mean(), "{:.2f}", 1),
    "Spending volatility": (cons.groupby("seg").spending_volatility.mean(), "{:.2f}", 1),
    "Engagement score": (cons.groupby("seg").engagement_score.mean(), "{:.1f}", 1),
    "Transactions / month": (cons.groupby("seg").transaction_count.mean(), "{:.0f}", 1),
    "Discretionary share": (cons.groupby("seg").discretionary_spend_ratio.mean(), "{:.0%}", 1),
    "Online share": (cons.groupby("seg").online_spend_ratio.mean(), "{:.0%}", 1),
    "Months observed (of 12)": (nm.groupby(cons.seg).mean(), "{:.1f}", 0),
    "Active days / month": (mon.groupby("seg").active_transaction_days.mean(), "{:.1f}", 0),
    "Non-POS share of value": (nonpos, "{:.0%}", 0),
    "Had a stress month (FHS<40)": (stress.groupby(cons.seg).mean(), "{:.1%}", 0),
    "Mean age": (demo.age.groupby(cons.seg).mean(), "{:.0f}", 0),
    "Female": (demo.gender.eq("Nữ").groupby(cons.seg).mean(), "{:.0%}", 0),
}
M = pd.DataFrame({k: s[ORDER] for k, (s, _, _) in rows.items()}).T
Z = M.sub(M.mean(1), axis=0).div(M.std(1), axis=0)
fig, ax = plt.subplots(figsize=(7.4, 6.4))
ax.imshow(Z.values, cmap="RdBu_r", vmin=-1.6, vmax=1.6, aspect="auto")
for i, r in enumerate(M.index):
    for j, s in enumerate(ORDER):
        z = Z.iat[i, j]
        ax.text(j, i, rows[r][1].format(M.iat[i, j]), ha="center", va="center", fontsize=9,
                color="white" if abs(z) > 1.1 else INK, fontweight="bold" if abs(z) > 1.1 else "normal")
SHORT = ["Healthy &\nEngaged", "Stretched &\nEngaged", "High-Activity\nUsers", "Occasional\nOnline-First"]
ax.set_xticks(range(4), [f"{t}\nn={n[s]}" for t, s in zip(SHORT, ORDER)], fontsize=8.5)
ax.set_yticks(range(len(M)), M.index, fontsize=9)
for t, s in zip(ax.get_xticklabels(), ORDER): t.set_color(COL[s]); t.set_fontweight("bold")
ax.axhline(7.5, color=INK, lw=1.2); ax.grid(False)
ax.text(3.62, 3.5, "model inputs", rotation=270, va="center", fontsize=8, color=MUTED)
ax.text(3.62, 10.5, "profile only", rotation=270, va="center", fontsize=8, color=MUTED)
ax.tick_params(length=0); [sp.set_visible(False) for sp in ax.spines.values()]
ax.set_title("Segments side by side (cell = mean; red high, blue low)", loc="left", fontsize=10.5)
fig.tight_layout(); fig.savefig(OUT + "profile_heatmap.png", dpi=150); plt.close(fig)

# ---- 4. PCA, same colours, centroid labels
pca = PCA(2, random_state=42).fit(X); P = pca.transform(X)
fig, ax = plt.subplots(figsize=(6.4, 4.2))
for s in ORDER:
    mk = (cons.seg == s).values
    ax.scatter(P[mk, 0], P[mk, 1], s=10, alpha=.55, color=COL[s], edgecolors="none")
    cx, cy = P[mk].mean(0)
    ax.annotate(f"{s} ({mk.sum()})", (cx, cy), fontsize=8.5, fontweight="bold", color=INK, ha="center",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=COL[s], lw=1.2))
ev = pca.explained_variance_ratio_
ax.set(xlabel=f"PC1 ({ev[0]:.0%}): activity & engagement  -  online / discretionary",
       ylabel=f"PC2 ({ev[1]:.0%}): health  -  spend/income, utilization")
ax.set_title("Part-year customers stand apart; the other three form a continuum", loc="left", fontsize=10.5)
fig.tight_layout(); fig.savefig(OUT + "pca.png", dpi=150); plt.close(fig)

# ---- 5. monthly FHS per full-year segment: the December drop hits everyone
full = mon[mon.seg != ORDER[3]]
t = full.groupby(["m", "seg"]).financial_health_score.mean().unstack()[ORDER[:3]]
fig, ax = plt.subplots(figsize=(6.4, 3.8))
for s in ORDER[:3]:
    ax.plot(t.index, t[s], color=COL[s], lw=2, marker="o", ms=4)
    ax.annotate(s, (12, t.loc[12, s]), xytext=(6, 0), textcoords="offset points", fontsize=8.5, color=INK, va="center")
d = (t.loc[12] - t.loc[11]).round(1)
ax.text(1, 50.5, f"Nov→Dec change: {d.iloc[0]:+.1f} / {d.iloc[1]:+.1f} / {d.iloc[2]:+.1f} pts\n(Healthy / Stretched / High-Activity)",
        fontsize=8.5, color=INK)
ax.set_xticks(range(1, 13), ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
ax.set(ylabel="Mean financial health score", xlim=(.6, 14.8))
ax.set_title("December lowers health in every segment in parallel", loc="left")
fig.tight_layout(); fig.savefig(OUT + "monthly_fhs.png", dpi=150); plt.close(fig)
print("silhouette", [round(s, 3) for s in sil]); print(M.round(3).to_string()); print("Nov->Dec", d.to_dict())
