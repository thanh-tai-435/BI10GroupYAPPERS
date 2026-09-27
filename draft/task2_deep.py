"""
Task 2 deep-dive (P2). Run: PYTHONUTF8=1 py draft/task2_deep.py > draft/task2_deep_output.txt
Each '## CELL' block is also one cell of notebooks/task2_financial_health.ipynb (after %run -i draft/task2.py).
"""
import runpy, sys
sys.stdout.reconfigure(encoding="utf-8")
globals().update(runpy.run_path("draft/task2.py"))
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
TXN = "BI10_ROUND01_DATASET/consumer_transactions_2025.parquet/consumer_transactions_2025.csv"
rng = np.random.default_rng(42)
def boot_ci(s, n=1000):
    return np.percentile([rng.choice(s.values, len(s)).mean() for _ in range(n)], [2.5, 97.5])

## CELL 2
h("DEEP Q3a - Province: mean FHS with bootstrap 95% CI (provinces with >= 15 consumers)")
nat = cons.fhs.mean()
pv = cons.groupby("province").fhs.agg(["size", "mean"]).query("size >= 15")
pv[["ci_lo", "ci_hi"]] = [boot_ci(cons.loc[cons.province == p, "fhs"]) for p in pv.index]
pv = pv.sort_values("mean")
pv["ci_contains_national"] = (pv.ci_lo <= nat) & (pv.ci_hi >= nat)
print(pv.round(2).to_string())
print(f"National mean {nat:.2f}; provinces whose CI excludes national: {int((~pv.ci_contains_national).sum())}/{len(pv)}")

## CELL 3
h("DEEP Q3b - Occupation grouped by keyword (396 raw titles -> 8 groups)")
# Thứ tự quan trọng: khớp từ khoá đầu tiên. Từ khoá viết thường, có dấu.
OCC = [
    ("Student",            ["sinh viên", "học sinh", "nghiên cứu sinh"]),
    ("Retired / homemaker",["hưu", "nội trợ"]),
    ("Health",             ["thầy thuốc", "bác sĩ", "y tá", "dược", "điều dưỡng", "y sĩ", "nha", "vật lý trị liệu", "hộ sinh", "sinh lý", "y tế"]),
    ("Education",          ["giáo viên", "giảng viên", "giáo", "gia sư", "hiệu trưởng"]),
    ("Engineering / science / IT", ["kiến trúc", "nghiên cứu", "khoa học", "kỹ sư", "kỹ thuật", "lập trình", "phần mềm", "công nghệ", "it ", "dữ liệu", "hệ thống", "mạng"]),
    ("Business / finance", ["kinh doanh", "bán hàng", "kế toán", "tài chính", "ngân hàng", "kiểm toán", "marketing", "chủ", "giám đốc", "quản lý", "thương mại", "đầu tư", "bảo hiểm"]),
    ("Office / public services", ["cán bộ", "thanh tra", "nhân viên", "chuyên viên", "thư ký", "hành chính", "trợ lý", "tư vấn", "luật", "thiết kế", "biên", "phóng viên", "nhà"]),
    ("Manual / trades",    ["họa sĩ", "nghệ", "công nhân", "thợ", "lái", "nông", "bảo vệ", "đầu bếp", "phụ", "vận", "xây", "lao động", "ngư"]),
]
def occ_group(s):
    s = str(s).lower()
    return next((g for g, kws in OCC if any(k in s for k in kws)), "Other")
cons["occ_group"] = cons.occupation.map(occ_group)
og = cons.groupby("occ_group").agg(n=("fhs", "size"), mean_fhs=("fhs", "mean"),
                                   spend_to_income=("spend_to_income_ratio", "mean"),
                                   credit_util=("credit_utilization_ratio", "mean"))
og[["ci_lo", "ci_hi"]] = [boot_ci(cons.loc[cons.occ_group == g, "fhs"]) for g in og.index]
print(og.sort_values("mean_fhs").round(3).to_string())
print(f"Unmapped ('Other'): {int((cons.occ_group == 'Other').sum())} consumers — sample:",
      cons.loc[cons.occ_group == "Other", "occupation"].drop_duplicates().head(12).tolist())
print(f"Spread of group means: {og.mean_fhs.max() - og.mean_fhs.min():.2f} FHS pts")

## CELL 4
h("DEEP Q3c - One chart: province / occupation group / age cohort, mean FHS ± 95% CI")
age_ci = (pd.read_csv("draft/task1_age_ci.csv", index_col=0) if os.path.exists("draft/task1_age_ci.csv") else None)
if age_ci is None:   # P1 chưa chạy -> tự tính
    ac = cons.groupby("cohort", observed=True).fhs
    age_ci = pd.DataFrame({"n": ac.size(), "mean_fhs": ac.mean()})
    age_ci[["ci_lo", "ci_hi"]] = [boot_ci(cons.loc[cons.cohort == k, "fhs"]) for k in age_ci.index]
EN = {"Thành phố Hồ Chí Minh": "HCMC", "Hà Nội": "Ha Noi", "Đồng Nai": "Dong Nai", "Lâm Đồng": "Lam Dong", "Hưng Yên": "Hung Yen",
      "Hải Phòng": "Hai Phong", "Cần Thơ": "Can Tho", "Đà Nẵng": "Da Nang", "Nghệ An": "Nghe An", "Quảng Ngãi": "Quang Ngai",
      "Thanh Hóa": "Thanh Hoa", "Khánh Hòa": "Khanh Hoa", "Gia Lai": "Gia Lai", "Đắk Lắk": "Dak Lak", "An Giang": "An Giang",
      "Tây Ninh": "Tay Ninh", "Đồng Tháp": "Dong Thap", "Vĩnh Long": "Vinh Long", "Ninh Bình": "Ninh Binh", "Phú Thọ": "Phu Tho",
      "Bắc Ninh": "Bac Ninh", "Quảng Ninh": "Quang Ninh", "Huế": "Hue", "Cà Mau": "Ca Mau", "Lào Cai": "Lao Cai",
      "Thái Nguyên": "Thai Nguyen", "Tuyên Quang": "Tuyen Quang", "Quảng Trị": "Quang Tri", "Sơn La": "Son La",
      "Lạng Sơn": "Lang Son", "Cao Bằng": "Cao Bang", "Điện Biên": "Dien Bien", "Lai Châu": "Lai Chau", "Hà Tĩnh": "Ha Tinh"}
panels = [("Province (n ≥ 15)", pv.rename(index=lambda s: EN.get(s, s))[["mean", "ci_lo", "ci_hi"]].rename(columns={"mean": "m"})),
          ("Occupation group", og.sort_values("mean_fhs").rename(index=lambda g: f"{g} (n={og.loc[g, 'n']})")[["mean_fhs", "ci_lo", "ci_hi"]].rename(columns={"mean_fhs": "m"})),
          ("Age cohort", age_ci[["mean_fhs", "ci_lo", "ci_hi"]].rename(columns={"mean_fhs": "m"}))]
fig, axes = plt.subplots(1, 3, figsize=(15, 6.5), sharex=True)
for ax, (t, d) in zip(axes, panels):
    y = np.arange(len(d))
    ax.errorbar(d.m, y, xerr=[d.m - d.ci_lo, d.ci_hi - d.m], fmt="o", color=C["primary"], ecolor=C["muted"], capsize=3)
    ax.axvline(nat, color=C["accent"], ls="--", lw=1.2)
    ax.set_yticks(y, d.index.astype(str), fontsize=9); ax.set_title(t, fontsize=13); ax.grid(axis="y", visible=False)
axes[0].set_xlabel("Mean FHS (95% CI)"); axes[1].set_xlabel("Mean FHS (95% CI)"); axes[2].set_xlabel("Mean FHS (95% CI)")
axes[2].text(nat, len(age_ci) - .4, f" national {nat:.1f}", color=C["accent"], fontsize=9)
fig.suptitle("Province and age barely move health; occupation spreads ~6 pts, tracking spend-to-income",
             fontsize=14, fontweight="bold")
save(fig, "t2_demographics.png")

## CELL 5
h("DEEP transactions - WHEN do stressed months spend? (day-of-week, hour, discretionary share)")
tx = pd.read_csv(TXN, usecols=["consumer_id", "transaction_month", "transaction_day_of_week", "transaction_hour",
                               "spend_amount_vnd", "essential_spending_flag"])
mm = mon[["consumer_id", "month", "financial_health_score"]].rename(columns={"month": "transaction_month"})
t = tx.merge(mm, on=["consumer_id", "transaction_month"], how="inner")
t["state"] = np.select([t.financial_health_score < 40, t.financial_health_score >= 80], ["stressed", "healthy"], "mid")
t = t[t.state != "mid"]
print(t.groupby("state").size().rename("transactions").to_string())
dow = pd.crosstab(t.transaction_day_of_week, t.state, values=t.spend_amount_vnd, aggfunc="sum", normalize="columns") * 100
dow.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]   # 0 = Monday (đã kiểm với activity_datetime)
print("\nShare of spend by day of week (%):\n", dow.round(1).to_string())
print(f"Sun+Mon share: stressed {dow.loc[['Sun','Mon'],'stressed'].sum():.1f}% vs healthy {dow.loc[['Sun','Mon'],'healthy'].sum():.1f}%")
t["hour_band"] = pd.cut(t.transaction_hour, [-1, 5, 11, 17, 21, 23], labels=["00-05", "06-11", "12-17", "18-21", "22-23"])
hb = pd.crosstab(t.hour_band, t.state, values=t.spend_amount_vnd, aggfunc="sum", normalize="columns") * 100
print("\nShare of spend by hour band (%):\n", hb.round(1).to_string())
hb["diff_pp"] = hb.stressed - hb.healthy
peak_band = hb.diff_pp.idxmax()
print(f"-> Biggest over-index for stressed months: {peak_band} ({hb.diff_pp.max():+.1f}pp of VALUE) -> candidate Spend-Alert timing")
hc = pd.crosstab(t.hour_band, t.state, normalize="columns") * 100
print("Share of TRANSACTION COUNT by hour band (%) — robustness:\n", hc.round(1).to_string())
late = t[t.state == "stressed"].groupby(["consumer_id", "transaction_month"]).apply(
    lambda d: d.loc[d.transaction_hour >= 22, "spend_amount_vnd"].sum() / d.spend_amount_vnd.sum())
print(f"Per stressed month: median 22-23h value share {100*late.median():.1f}% | months > 20%: {(late > .2).sum()}/{len(late)}")
print("-> Not MORE late-night transactions (count gap small) but BIGGER late-night tickets, in most stressed months.")
ess = t.groupby("state").apply(lambda d: 100 * (1 - d.loc[d.essential_spending_flag.astype(bool), 'spend_amount_vnd'].sum() / d.spend_amount_vnd.sum()))
print("Discretionary share (txn-level):", ess.round(1).to_dict())

fig, ax = plt.subplots(figsize=(10, 5.5))
w = .38; x = np.arange(len(hb))
ax.bar(x - w/2, hb.healthy, w, color=C["good"], label="Healthy months (FHS ≥ 80)")
ax.bar(x + w/2, hb.stressed, w, color=C["accent"], label="Stressed months (FHS < 40)")
ax.set_xticks(x, hb.index.astype(str)); ax.set_ylabel("% of month's spend"); ax.set_xlabel("Hour of day")
ax.set_title("Stressed months: big late-night tickets (22-23h) carry 3x the spend share"); ax.legend(frameon=False)
save(fig, "t2_timing.png")

## CELL 6
h("DEEP Q4 - Crossover rule sensitivity (FHS cutoff x engagement percentile)")
stress_all = {}
rows = []
for f in (35, 40, 45):
    st = mon[mon.financial_health_score < f]
    for q in (.70, .75, .80):
        e = mon.engagement_score.quantile(q)
        cx = st[st.engagement_score >= e]
        rows.append((f"FHS<{f}", f"eng>=p{int(q*100)} ({e:.1f})", cx.consumer_id.nunique(), len(cx),
                     round(100 * len(cx) / max(len(st), 1), 1)))
sens = pd.DataFrame(rows, columns=["health", "engagement", "consumers", "months", "%_of_stress_months"])
print(sens.to_string(index=False))

## CELL 7
h("DEEP Q2 - FHS by spend_to_income quintile (visual version of r = -0.90)")
cons["sti_q"] = pd.qcut(cons.spend_to_income_ratio, 5, labels=["Q1 lowest", "Q2", "Q3", "Q4", "Q5 highest"])
qq = cons.groupby("sti_q", observed=True).agg(n=("fhs", "size"), sti=("spend_to_income_ratio", "mean"), fhs=("fhs", "mean"))
print(qq.round(3).to_string())
print(f"Q1 -> Q5 FHS drop: {qq.fhs.iloc[0] - qq.fhs.iloc[-1]:.1f} pts "
      f"(vs age spread {cons.groupby('cohort', observed=True).fhs.mean().agg(lambda s: s.max() - s.min()):.1f} pts)")
fig, ax = plt.subplots(figsize=(9, 5.5))
b = ax.bar(qq.index.astype(str), qq.fhs, color=[C["good"], C["good"], C["warn"], C["accent"], C["accent"]])
for r, s in zip(b, qq.sti):
    ax.annotate(f"{r.get_height():.1f}\n(spend/inc {s:.2f})", (r.get_x() + r.get_width()/2, r.get_height()),
                xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9)
ax.set_ylim(50, 78); ax.set_ylabel("Mean FHS (consumer level)"); ax.set_xlabel("Spend-to-income quintile")
ax.set_title("Health falls step by step as spend-to-income rises")
save(fig, "t2_sti_quintile.png")
