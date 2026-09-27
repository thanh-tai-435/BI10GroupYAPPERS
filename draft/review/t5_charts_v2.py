# v2 Task 5 charts. Run: PYTHONUTF8=1 py draft/review/t5_charts_v2.py
# Every plotted number is computed here from the raw monthly file + draft/task4_features.csv.
import sys; sys.stdout.reconfigure(encoding="utf-8")
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
C = dict(primary="#2E5EAA", accent="#E4572E", good="#3C9D6E", warn="#E0A32E", muted="#9AA5B1", ink="#22303F")
plt.rcParams.update({"font.size": 11, "axes.titlesize": 14, "axes.titleweight": "bold", "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.alpha": .25})
M = pd.read_csv("BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv")
F = pd.read_csv("draft/task4_features.csv").set_index("consumer_id")
seg = F.segment.str.split().str[1].map({"Healthy": "Healthy", "Stretched": "Stretched", "Digital": "Power", "Engagement": "Emerging"})
p75 = M.engagement_score.quantile(.75)
X = M[(M.financial_health_score < 40) & (M.engagement_score >= p75)].consumer_id.nunique()
D = int(((F.financial_health_score < 70) & (F.engagement_score < 70)).sum())
n = seg.value_counts(); assert (n.Healthy, n.Stretched, n.Power, n.Emerging, X, D) == (351, 302, 258, 88, 43, 67)
r = lambda a, b: abs(M[a].corr(M[b]))
F_, E_ = "financial_health_score", "engagement_score"
T = pd.DataFrame([  # tool, reach, trigger column, outcome, track
    ("Budgeting", n.Stretched, "spend_to_income_ratio", F_, "Wellbeing"),
    ("Spend alerts", X, "credit_utilization_ratio", F_, "Wellbeing"),
    ("Planning reminders", n.Power, "spending_volatility", F_, "Wellbeing"),
    ("Education", D, "discretionary_spend_ratio", F_, "Wellbeing"),
    ("Digital nudges", n.Emerging, "category_diversity", E_, "Growth"),
    ("Product suggestions", n.Healthy, "credit_utilization_ratio", E_, "Growth"),
], columns=["tool", "reach", "trigger", "outcome", "track"])
T["driver"] = [r(t, o) for t, o in zip(T.trigger, T.outcome)]
T["score"] = T.reach * T.driver
T = T.sort_values(["track", "score"], ascending=[False, False]).reset_index(drop=True)
print(T.round(3).to_string())
assert list(T.tool) == ["Budgeting", "Planning reminders", "Spend alerts", "Education", "Product suggestions", "Digital nudges"]

# --- chart 1: priority map whose axes ARE the score inputs --------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
xs = np.linspace(20, 400, 200)
for k in (50, 100, 200, 300):
    ax.plot(xs, k / xs, color=C["muted"], lw=.8, ls="--", zorder=1)
    ax.text(400, k / 400, f" score {k}", color=C["muted"], fontsize=8, va="center")
for _, t in T.iterrows():
    col = C["accent"] if t.track == "Wellbeing" else C["primary"]
    ax.scatter(t.reach, t.driver, s=160, color=col, edgecolor="white", zorder=3)
    rank = _ + 1
    ax.annotate(f"#{rank} {t.tool}\n{t.reach} x {t.driver:.2f} = {t.score:.0f}", (t.reach, t.driver),
                xytext=(-8 if t.reach > 330 else 8, 8), ha="right" if t.reach > 330 else "left",
                textcoords="offset points", fontsize=9, fontweight="bold", color=C["ink"])
ax.set(xlim=(0, 460), ylim=(0, 1.02), xlabel="Reach = consumers in target group (of 999)",
       ylabel="Driver strength = |r| of trigger column with outcome\n(month level, n = 10,992)")
ax.set_title("Priority score = reach x driver strength (wellbeing track first)")
ax.scatter([], [], color=C["accent"], label="Wellbeing (outcome = FHS)")
ax.scatter([], [], color=C["primary"], label="Growth (outcome = engagement)")
ax.legend(frameon=False, loc="lower right")
fig.tight_layout(); fig.savefig("outputs/figures/v2_t5_priority_score.png", dpi=150, bbox_inches="tight")

# --- chart 2: impact scenario, honest framing + slope sensitivity ------------------------------
isS = M.consumer_id.map(seg).eq("Stretched")
b_all = np.polyfit(M.spend_to_income_ratio, M.financial_health_score, 1)[0]
b_seg = np.polyfit(M.loc[isS, "spend_to_income_ratio"], M.loc[isS, "financial_health_score"], 1)[0]
cuts = [0, .05, .10, .15]
sim = lambda b: [int((M.financial_health_score - b * M.spend_to_income_ratio * c * isS < 40).sum()) for c in cuts]
pooled, within = sim(b_all), sim(b_seg)
print("pooled slope", round(b_all, 2), pooled, "| within-Stretched slope", round(b_seg, 2), within)
assert pooled == [95, 80, 65, 49]
fig, ax = plt.subplots(figsize=(10, 5.5)); x = np.arange(4); w = .38
b1 = ax.bar(x - w/2, pooled, w, color=C["primary"], label=f"All-customer slope ({b_all:.1f} FHS pts per 1.0 STI)")
b2 = ax.bar(x + w/2, within, w, color=C["muted"], label=f"Stretched-only slope ({b_seg:.1f})")
for bars in (b1, b2):
    for rc in bars:
        ax.annotate(f"{int(rc.get_height())}", (rc.get_x() + rc.get_width()/2, rc.get_height()), xytext=(0, 3),
                    textcoords="offset points", ha="center", fontsize=10)
ax.axhline(95 - 86, color=C["accent"], ls=":", lw=1.2, label="Floor: 9 stress months outside the Stretched 302")
ax.set_xticks(x, ["Today", "-5%", "-10%", "-15%"])
ax.set(xlabel="Assumed cut in spend-to-income, Stretched segment only (302)", ylabel="Months with FHS < 40 (all 999)", ylim=(0, 110))
ax.set_title("What-if, not a forecast: a 10% trim implies 95 -> 65-68 stress months")
ax.legend(frameon=False)
fig.tight_layout(); fig.savefig("outputs/figures/v2_t5_impact_scenario.png", dpi=150, bbox_inches="tight")
print("saved v2_t5_priority_score.png, v2_t5_impact_scenario.png")
