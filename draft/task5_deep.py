"""
Task 5 deep-dive (P5). Run: PYTHONUTF8=1 py draft/task5_deep.py > draft/task5_deep_output.txt
Each '## CELL' block is also one cell of notebooks/task5_recommendations.ipynb (after %run -i draft/task5.py).
SCENARIOS ARE ILLUSTRATIVE ASSUMPTIONS, NOT FORECASTS.
"""
import runpy, sys
sys.stdout.reconfigure(encoding="utf-8")
globals().update(runpy.run_path("draft/task5.py"))
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

## CELL 2
h("Impact scenario - what if Budgeting trims spend-to-income? (illustrative, NOT a forecast)")
b, a = np.polyfit(m.spend_to_income_ratio, m.financial_health_score, 1)
r = m.spend_to_income_ratio.corr(m.financial_health_score)
print(f"Month-level fit: FHS = {a:.1f} {b:+.2f} x spend_to_income  (r = {r:.2f}, n = {len(m):,})")
stretched_ids = set(f.loc[f.segment == "Financially Stretched but Highly Engaged", "consumer_id"])
ms = m[m.consumer_id.isin(stretched_ids)]
rows = []
for cut in (0, .05, .10, .15):
    fhs_new = m.financial_health_score - b * m.spend_to_income_ratio * cut * m.consumer_id.isin(stretched_ids)
    st_new = fhs_new < 40
    rows.append(("Today" if cut == 0 else f"-{int(cut*100)}%", round(float((ms.financial_health_score - b * ms.spend_to_income_ratio * cut).mean()), 1),
                 int(st_new.sum()), int(m.loc[st_new, "consumer_id"].nunique())))
sc = pd.DataFrame(rows, columns=["spend/income change (Stretched 302)", "Stretched mean FHS", "stress months (all 999)", "consumers with a stress month"])
print(sc.to_string(index=False))
base_st = sc.iloc[0, 2]
for i in (1, 2):
    print(f"  {sc.iloc[i,0]}: stress months {base_st} -> {sc.iloc[i,2]} ({100*(sc.iloc[i,2]/base_st-1):+.0f}%)")
print("Caveat: FHS is partly built from spend fields -> slope is mechanical, directional only; validate with an A/B test.")

fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.bar(sc.iloc[:, 0], sc.iloc[:, 2], color=[C["accent"], C["warn"], C["good"], C["good"]])
for rct, v in zip(bars, sc.iloc[:, 2]):
    ax.annotate(f"{v}", (rct.get_x() + rct.get_width()/2, v), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=12)
ax.set_xlabel("Assumed change in spend-to-income for the Stretched segment (302)")
ax.set_ylabel("Consumer-months with FHS < 40 (all 999)")
ax.set_title("Scenario: a 10% spend trim cuts stress months by a third")
save(fig, "t5_impact_scenario.png")

## CELL 3
h("Measurement plan - one KPI per tool, each tested with a randomised holdout")
kpi = pd.DataFrame([
    ("Budgeting tool", "Stretched & Engaged (302)", "spend-to-income ratio; % months FHS<40", "10% random holdout, 3 months"),
    ("Spend alerts", "Crossover (43; 52% of stress months)", "stress months per consumer; discretionary share in alert window", "alert vs no-alert, 2 months"),
    ("Planning reminders", "Power Users (258) + Healthy (351) before Dec", "Nov->Dec slide Healthy->Stretched (base 72.4%)", "reminder in Nov vs holdout"),
    ("Financial education", "Distress tail (67)", "module completion; essential share next month", "opt-in cohort vs matched"),
    ("Digital nudges", "Emerging Digital (88)", "active days / month; category diversity", "nudge vs holdout, 2 months"),
    ("Product suggestions", "Healthy & Engaged (351)", "opt-in savings/loyalty uptake; FHS stable", "offer vs holdout; guardrail: FHS never used for credit"),
], columns=["Tool", "Target", "KPI", "Test design"])
print(kpi.to_string(index=False))

## CELL 4
h("30/60/90-day roadmap")
for k, v in {"Days 0-30": "Launch Budgeting (302) + Spend Alerts (43), timed Sun-Mon & 22-23h (Task 2 timing); set holdouts",
             "Days 31-60": "Planning Reminders before December (Nov->Dec slide 72.4%); Digital Nudges (88)",
             "Days 61-90": "Education (67) + opt-in Product suggestions (351); read A/B results, keep what moves the KPI"}.items():
    print(f"  {k:<11} {v}")
