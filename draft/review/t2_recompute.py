"""Independent recomputation of Task 2 slide numbers (slides 9-12).
Run: PYTHONUTF8=1 py draft/review/t2_recompute.py > draft/review/t2_recompute_output.txt
"""
import sys, numpy as np, pandas as pd
from scipy import stats
sys.stdout.reconfigure(encoding="utf-8")
pd.set_option("display.width", 220, "display.max_columns", 30)

MON = "BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv"
TXN = "BI10_ROUND01_DATASET/consumer_transactions_2025.parquet/consumer_transactions_2025.csv"
m = pd.read_csv(MON, parse_dates=["analysis_month"])
m["mo"] = m.analysis_month.dt.month
F, E = "financial_health_score", "engagement_score"
def h(t): print(f"\n===== {t} =====")

h("Panel structure")
nmo = m.groupby("consumer_id").size()
print("months per consumer:", nmo.value_counts().to_dict())
one = nmo[nmo <= 2].index
print("1-2 month consumers: month of their rows:", m[m.consumer_id.isin(one)].mo.value_counts().sort_index().to_dict())
print("their mean FHS", m[m.consumer_id.isin(one)][F].mean().round(2), "txn_count mean", m[m.consumer_id.isin(one)].transaction_count.mean().round(1),
      "vs others", m[~m.consumer_id.isin(one)].transaction_count.mean().round(1))

# ---------------- D1
h("D1 consumer level (mean of available months)")
c = m.groupby("consumer_id").agg(fhs=(F, "mean"), eng=(E, "mean"), age=("age", "first"), occ=("occupation", "first"),
                                 prov=("province_city", "first"), sti=("spend_to_income_ratio", "mean"),
                                 cu=("credit_utilization_ratio", "mean"), n=(F, "size"), fmin=(F, "min"))
s = c.fhs
print(f"n={len(s)} mean {s.mean():.2f} median {s.median():.2f} std {s.std():.2f} IQR {s.quantile(.25):.2f}-{s.quantile(.75):.2f} "
      f"range {s.min():.2f}-{s.max():.2f} skew {s.skew():.3f}")
s12 = c[c.n == 12].fhs
print(f"12-month consumers only n={len(s12)}: mean {s12.mean():.2f} median {s12.median():.2f} std {s12.std():.2f} "
      f"IQR {s12.quantile(.25):.2f}-{s12.quantile(.75):.2f} range {s12.min():.2f}-{s12.max():.2f}")
mm = m[F]
print(f"month level n={len(mm)} mean {mm.mean():.2f} median {mm.median():.2f} std {mm.std():.2f} min {mm.min()} max {mm.max()}")
seg = m.financial_health_segment.value_counts(normalize=True).mul(100).round(1)
print("segments %:", seg.to_dict())
print("consumers mean<40:", (s < 40).sum(), "| consumers with >=1 month <40:", (c.fmin < 40).sum(),
      "| with >=2 months <40:", (m[m[F] < 40].groupby("consumer_id").size() >= 2).sum(),
      "| max stressed months per consumer:", m[m[F] < 40].groupby("consumer_id").size().max())
print("consumers with >=1 month <60 (Watch or worse):", (c.fmin < 60).sum())
mon_mean = m.groupby("mo")[F].mean().round(1)
print("monthly mean FHS:", mon_mean.to_dict())
print("stressed months by calendar month:", m[m[F] < 40].mo.value_counts().sort_index().to_dict())
# within vs between variance
wv = m.groupby("consumer_id")[F].transform(lambda x: x - x.mean())
print(f"within-consumer std {wv[m.consumer_id.map(nmo) == 12].std():.2f}; between-consumer std {s12.std():.2f}")
# month effect vs person effect
dm = m[F] - m.groupby("mo")[F].transform("mean")
print(f"share of month-level FHS variance explained by calendar month: {1 - dm.var() / mm.var():.3f}")
m12 = m[m.consumer_id.map(nmo) == 12]
per = m12[F] - m12.groupby("consumer_id")[F].transform("mean")
print(f"share explained by consumer identity (12-mo panel): {1 - per.var() / m12[F].var():.3f}")

# ---------------- D2
h("D2 correlations (month grain, Pearson + Spearman) and within-consumer")
R = ["spend_to_income_ratio", "credit_utilization_ratio", "spending_volatility", "essential_spend_ratio",
     "discretionary_spend_ratio", E, "online_spend_ratio"]
out = pd.DataFrame({"pearson": m[R].corrwith(m[F]), "spearman": m[R].corrwith(m[F], method="spearman")})
# within-consumer (demeaned) correlation, 12-month consumers only
d = m12[[F] + R] - m12.groupby("consumer_id")[[F] + R].transform("mean")
out["within_consumer"] = d[R].corrwith(d[F])
print(out.round(3).to_string())
X = np.column_stack([np.ones(len(m)), m.spend_to_income_ratio, m.credit_utilization_ratio])
b, *_ = np.linalg.lstsq(X, m[F], rcond=None)
r2 = 1 - ((m[F] - X @ b) ** 2).sum() / ((m[F] - m[F].mean()) ** 2).sum()
print(f"OLS FHS ~ STI + CU: R2 = {r2:.3f}; corr(STI, CU) = {m.spend_to_income_ratio.corr(m.credit_utilization_ratio):.3f}")
X2 = np.column_stack([X, m.spending_volatility, m.essential_spend_ratio, m[E], m.online_spend_ratio])
b2, *_ = np.linalg.lstsq(X2, m[F], rcond=None)
print(f"OLS + volatility, essential, engagement, online: R2 = {1 - ((m[F] - X2 @ b2) ** 2).sum() / ((m[F] - m[F].mean()) ** 2).sum():.3f}")
lo, hi = m[m[F] < 40], m[m[F] >= 80]
print(f"n stressed months {len(lo)} (consumers {lo.consumer_id.nunique()}), healthy months {len(hi)} (consumers {hi.consumer_id.nunique()})")
print(pd.DataFrame({"stressed": lo[R].mean(), "healthy": hi[R].mean(), "all": m[R].mean()}).round(3).to_string())
print(f"engagement stressed vs healthy t-test (Welch) p = {stats.ttest_ind(lo[E], hi[E], equal_var=False).pvalue:.2e}")
c["q"] = pd.qcut(c.sti, 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])
qq = c.groupby("q", observed=True).agg(n=("fhs", "size"), sti=("sti", "mean"), fhs=("fhs", "mean"))
print("consumer-level STI quintiles:\n", qq.round(3).to_string(), "\n drop", round(qq.fhs.iloc[0] - qq.fhs.iloc[-1], 2))
m["q"] = pd.qcut(m.spend_to_income_ratio, 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])
mq = m.groupby("q", observed=True).agg(n=(F, "size"), sti=("spend_to_income_ratio", "mean"), fhs=(F, "mean"),
                                      stressed_pct=(F, lambda x: 100 * (x < 40).mean()), watch_or_worse=(F, lambda x: 100 * (x < 60).mean()))
print("month-level STI quintiles:\n", mq.round(2).to_string())
print("STI where stressed begins: min STI among stressed months", lo.spend_to_income_ratio.min().round(3),
      "| share of months with STI>1 that are <60:", round(100 * (m[m.spend_to_income_ratio > 1][F] < 60).mean(), 1),
      "| n months STI>1:", (m.spend_to_income_ratio > 1).sum())

# ---------------- D3
h("D3 demographics (consumer level)")
rng = np.random.default_rng(42)
def boot(x, n=2000):
    x = x.values; return np.percentile(rng.choice(x, (n, len(x))).mean(1), [2.5, 97.5])
nat = s.mean()
bins = [0, 24, 34, 44, 54, 64, 200]; labs = ["15-24", "25-34", "35-44", "45-54", "55-64", "65+"]
c["coh"] = pd.cut(c.age, bins, labels=labs)
def table(col, minn=1):
    g = c.groupby(col, observed=True).agg(n=("fhs", "size"), fhs=("fhs", "mean"), sti=("sti", "mean"))
    g = g[g.n >= minn]
    g[["lo", "hi"]] = [boot(c.loc[c[col] == k, "fhs"]) for k in g.index]
    g["contains_nat"] = (g.lo <= nat) & (g.hi >= nat)
    return g.sort_values("fhs")
def anova(col, minn=1):
    keep = c.groupby(col, observed=True).fhs.transform("size") >= minn
    groups = [x.values for _, x in c[keep].groupby(col, observed=True).fhs]
    f, p = stats.f_oneway(*groups); kw = stats.kruskal(*groups).pvalue
    ss_b = sum(len(g) * (g.mean() - c[keep].fhs.mean()) ** 2 for g in groups); ss_t = ((c[keep].fhs - c[keep].fhs.mean()) ** 2).sum()
    return f"ANOVA p={p:.3g}, Kruskal p={kw:.3g}, eta2={ss_b / ss_t:.3f}, groups={len(groups)}, n={keep.sum()}"
at = table("coh"); print(at.round(2).to_string()); print("age", anova("coh"))
pt = table("prov", 15); print(pt.round(2).to_string())
print(f"provinces n>=15: {len(pt)}; CI contains national {nat:.2f}: {pt.contains_nat.sum()}; excludes: {list(pt.index[~pt.contains_nat])}")
print("province (n>=15)", anova("prov", 15)); print("province (all 34)", anova("prov"))
print("province sizes range", c.prov.value_counts().agg(["min", "max"]).to_dict())
OCC = [  # same keyword map as draft/task2_deep.py, to check the deck numbers
    ("Student", ["sinh viên", "học sinh", "nghiên cứu sinh"]), ("Retired / homemaker", ["hưu", "nội trợ"]),
    ("Health", ["thầy thuốc", "bác sĩ", "y tá", "dược", "điều dưỡng", "y sĩ", "nha", "vật lý trị liệu", "hộ sinh", "sinh lý", "y tế"]),
    ("Education", ["giáo viên", "giảng viên", "giáo", "gia sư", "hiệu trưởng"]),
    ("Engineering / science / IT", ["kiến trúc", "nghiên cứu", "khoa học", "kỹ sư", "kỹ thuật", "lập trình", "phần mềm", "công nghệ", "it ", "dữ liệu", "hệ thống", "mạng"]),
    ("Business / finance", ["kinh doanh", "bán hàng", "kế toán", "tài chính", "ngân hàng", "kiểm toán", "marketing", "chủ", "giám đốc", "quản lý", "thương mại", "đầu tư", "bảo hiểm"]),
    ("Office / public services", ["cán bộ", "thanh tra", "nhân viên", "chuyên viên", "thư ký", "hành chính", "trợ lý", "tư vấn", "luật", "thiết kế", "biên", "phóng viên", "nhà"]),
    ("Manual / trades", ["họa sĩ", "nghệ", "công nhân", "thợ", "lái", "nông", "bảo vệ", "đầu bếp", "phụ", "vận", "xây", "lao động", "ngư"])]
c["og"] = c.occ.str.lower().map(lambda s: next((g for g, k in OCC if any(w in s for w in k)), "Other"))
print("raw occupation titles:", c.occ.nunique(), "| max consumers per title:", c.occ.value_counts().max())
ot = table("og"); print(ot.round(3).to_string()); print("occupation", anova("og", 20))
# does occupation survive controlling for STI?  residualise FHS on STI (consumer level)
bb = np.polyfit(c.sti, c.fhs, 1); c["res"] = c.fhs - np.polyval(bb, c.sti)
print("residual FHS (after STI) by occ group:", c.groupby("og").res.mean().round(2).to_dict())
keep = c.groupby("og").fhs.transform("size") >= 20
print("occupation on residual: ANOVA p=%.3g" % stats.f_oneway(*[x.values for _, x in c[keep].groupby("og").res]).pvalue)
print("province on residual (n>=15): ANOVA p=%.3g" % stats.f_oneway(*[x.values for _, x in c[c.groupby('prov').fhs.transform('size') >= 15].groupby("prov").res]).pvalue)
print("age on residual: ANOVA p=%.3g" % stats.f_oneway(*[x.values for _, x in c.groupby("coh", observed=True).res]).pvalue)
print("keyword-map spot check (random 15 titles -> group):")
for t_, g_ in c[["occ", "og"]].drop_duplicates("occ").sample(15, random_state=1).values: print("   ", t_, "->", g_)
print("gender:", c.join(m.groupby("consumer_id").gender.first()).groupby("gender").fhs.agg(["size", "mean"]).round(2).to_dict())

# ---------------- D4
h("D4 crossover")
p75 = m[E].quantile(.75); print(f"engagement p75 over all 10,992 consumer-months (pandas linear) = {p75:.4f}")
print("p75 at consumer level (mean engagement):", round(c.eng.quantile(.75), 2))
cx = m[(m[F] < 40) & (m[E] >= p75)]
print(f"crossover months {len(cx)}, consumers {cx.consumer_id.nunique()} ({100 * cx.consumer_id.nunique() / 999:.1f}% of 999), "
      f"share of stress months {100 * len(cx) / len(lo):.1f}%, share of stressed consumers {100 * cx.consumer_id.nunique() / lo.consumer_id.nunique():.1f}%")
print("engagement values at the boundary (81.3-81.5):", m[E][(m[E] >= 81.3) & (m[E] <= 81.5)].value_counts().sort_index().to_dict())
for f in (35, 40, 45):
    st = m[m[F] < f]
    print(f"FHS<{f}: " + " | ".join(f"p{int(q*100)}={m[E].quantile(q):.1f}: {st[st[E] >= m[E].quantile(q)].consumer_id.nunique()} cons, "
                                    f"{100 * (st[E] >= m[E].quantile(q)).mean():.1f}% months" for q in (.7, .75, .8)))
# base rate: if engagement independent of stress, 25% of stress months would be >= p75
print(f"expected share under independence 25%; binomial p (>= {len(cx)} of {len(lo)}): {stats.binomtest(len(cx), len(lo), .25, alternative='greater').pvalue:.2e}")
prof = pd.DataFrame({"crossover": cx[R + [F, "transaction_count"]].mean(), "all": m[R + [F, "transaction_count"]].mean()})
print(prof.round(3).to_string())
print("crossover months by calendar month:", cx.mo.value_counts().sort_index().to_dict())
print("crossover consumers: # months in total panel:", m[m.consumer_id.isin(cx.consumer_id)].groupby("consumer_id").size().value_counts().to_dict())
print("crossover consumers' other-month mean FHS:", m[m.consumer_id.isin(cx.consumer_id) & ~m.index.isin(cx.index)][F].mean().round(1))
# Leading signal: month before a crossover month
prev = m.set_index(["consumer_id", "mo"])
keys = [(a, b - 1) for a, b in zip(cx.consumer_id, cx.mo) if (a, b - 1) in prev.index]
pv_ = prev.loc[keys]
print(f"month BEFORE crossover (n={len(pv_)}): FHS {pv_[F].mean():.1f}, STI {pv_.spend_to_income_ratio.mean():.2f}, CU {pv_.credit_utilization_ratio.mean():.2f}, "
      f"flag next_month_low_health {pv_.next_month_low_health_flag.mean():.2f}")
print(f"all months: STI>1 share {100*(m.spend_to_income_ratio>1).mean():.1f}%; stressed months with STI>1: {100*(lo.spend_to_income_ratio>1).mean():.1f}%")

h("D4 timing (transactions joined to month on consumer_id + month)")
tx = pd.read_csv(TXN, usecols=["consumer_id", "activity_datetime", "transaction_month", "transaction_day_of_week",
                               "transaction_hour", "spend_amount_vnd", "spending_category", "essential_spending_flag", "transaction_channel"])
print("rows", len(tx))
smp = tx.sample(2000, random_state=0); dt = pd.to_datetime(smp.activity_datetime)
print("dow 0=Monday check:", (dt.dt.dayofweek == smp.transaction_day_of_week).mean(), "| hour check:", (dt.dt.hour == smp.transaction_hour).mean(),
      "| month check:", (dt.dt.month == smp.transaction_month).mean())
j = tx.merge(m[["consumer_id", "mo", F]].rename(columns={"mo": "transaction_month"}), on=["consumer_id", "transaction_month"], how="left")
print("txn rows without a consumer-month:", j[F].isna().sum())
j["st"] = np.select([j[F] < 40, j[F] >= 80], ["stressed", "healthy"], "mid")
j["mid"] = j.st  # keep
v = lambda d, col: pd.crosstab(d[col], d.st, values=d.spend_amount_vnd, aggfunc="sum", normalize="columns") * 100
j["late"] = j.transaction_hour >= 22
print("value share 22-23h (%):", v(j, "late").loc[True].round(1).to_dict())
print("count share 22-23h (%):", (pd.crosstab(j.late, j.st, normalize="columns") * 100).loc[True].round(1).to_dict())
dow = v(j, "transaction_day_of_week"); print("value share by DOW (0=Mon):\n", dow.round(1).to_string())
print("Sun+Mon value share:", (dow.loc[6] + dow.loc[0]).round(1).to_dict(), "| uniform = 28.6")
print("Sun+Mon count share:", (pd.crosstab(j.transaction_day_of_week, j.st, normalize="columns").loc[[0, 6]].sum() * 100).round(1).to_dict())
# per-month view for stressed months (unit = consumer-month, avoids a few big months dominating)
g = j[j.st != "mid"].groupby(["consumer_id", "transaction_month", "st"])
pm = pd.DataFrame({"late": g.apply(lambda d: d.loc[d.late, "spend_amount_vnd"].sum() / d.spend_amount_vnd.sum()),
                   "sunmon": g.apply(lambda d: d.loc[d.transaction_day_of_week.isin([0, 6]), "spend_amount_vnd"].sum() / d.spend_amount_vnd.sum())}).reset_index()
print("per-month medians:\n", pm.groupby("st")[["late", "sunmon"]].median().mul(100).round(1).to_string())
print("Mann-Whitney late share stressed vs healthy months p =", f"{stats.mannwhitneyu(pm[pm.st=='stressed'].late, pm[pm.st=='healthy'].late).pvalue:.2e}")
print("stressed months with late share > 20%:", (pm[pm.st == "stressed"].late > .2).sum(), "/", (pm.st == "stressed").sum())
# ticket size late vs not
tk = j[j.st != "mid"].groupby(["st", "late"]).spend_amount_vnd.median().unstack()
print("median ticket (VND) by late:\n", tk.to_string())
print("ratio late/non-late median ticket:", (tk[True] / tk[False]).round(2).to_dict())
# what categories carry the stressed late-night value?
lt = j[(j.st == "stressed") & j.late]
print("stressed 22-23h value by category (top 6 %):", (lt.groupby("spending_category").spend_amount_vnd.sum() / lt.spend_amount_vnd.sum() * 100).nlargest(6).round(1).to_dict())
lh = j[(j.st == "healthy") & j.late]
print("healthy 22-23h value by category (top 6 %):", (lh.groupby("spending_category").spend_amount_vnd.sum() / lh.spend_amount_vnd.sum() * 100).nlargest(6).round(1).to_dict())
print("discretionary value share (txn flag):", (100 - v(j, "essential_spending_flag").loc[1]).round(1).to_dict())
print("channel value share:\n", v(j, "transaction_channel").round(1).to_string())
# all months: is late value share monotone in FHS band?
j["band"] = pd.cut(j[F], [-1, 40, 60, 80, 101], right=False, labels=["<40", "40-60", "60-80", ">=80"])
bl = j.groupby("band", observed=True).apply(lambda d: 100 * d.loc[d.late, "spend_amount_vnd"].sum() / d.spend_amount_vnd.sum())
print("late value share by FHS band:", bl.round(1).to_dict())
bl2 = j.groupby("band", observed=True).apply(lambda d: 100 * d.loc[d.transaction_day_of_week.isin([0, 6]), "spend_amount_vnd"].sum() / d.spend_amount_vnd.sum())
print("Sun+Mon value share by FHS band:", bl2.round(1).to_dict())
