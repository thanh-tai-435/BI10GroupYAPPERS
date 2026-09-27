"""
Task 4 deep-dive (P4). Run: PYTHONUTF8=1 py draft/task4_deep.py > draft/task4_deep_output.txt
Each '## CELL' block is also one cell of notebooks/task4_segmentation.ipynb (after %run -i draft/task4.py).
"""
import runpy, sys
sys.stdout.reconfigure(encoding="utf-8")
globals().update(runpy.run_path("draft/task4.py"))
import matplotlib; matplotlib.use("Agg")
## CELL 1
# Việc 1 — Preprocessed Dataset: 8 feature thô + 8 feature z-scale + nhãn + nhân khẩu
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler().fit(cons[feat])            # cùng scaler với task4.py (fit trên 999 khách)
Z = pd.DataFrame(scaler.transform(cons[feat]), index=cons.index, columns=[f"z_{c}" for c in feat])
ds = cons[feat].join(Z).join(cons[["cluster", "segment", "rule2x2"]]).join(demo)
assert len(ds) == 999 and ds.segment.notna().all() and not ds.isnull().any().any()
ds.to_csv("draft/task4_features.csv")
print(ds.shape, "->", "draft/task4_features.csv")

DICT = {
    "consumer_id": "Mã khách (khoá, nối với 2 file gốc)",
    **{c: f"TB 12 tháng của `{c}` (file consumer-month), trục {FEATURES[c]}" for c in feat},
    **{f"z_{c}": f"`{c}` đã chuẩn hoá z-score (StandardScaler, fit trên 999 khách) — input của k-means" for c in feat},
    "cluster": "Nhãn cụm k-means (k=4, random_state=42, n_init=25)",
    "segment": "Tên segment nghiệp vụ gán theo cực trị của cụm",
    "rule2x2": "Nhãn kiểm chứng 2x2 health x engagement (chia theo median) — không phải mô hình chính",
    "age": "Tuổi (dùng để mô tả, KHÔNG đưa vào phân cụm)", "gender": "Giới tính (mô tả)",
    "occupation": "Nghề (mô tả)", "province": "Tỉnh/thành (mô tả)",
}
with open("draft/data_dictionary_task4.md", "w", encoding="utf-8") as f:
    f.write("# Data dictionary — task4_features.csv\n\n1 dòng / khách (999). Nguồn: consumer_financial_health_engagement_2025.csv, "
            "gộp 12 tháng bằng trung bình. Chỉ dùng tỷ lệ/điểm, không dùng VND tuyệt đối.\n\n| Cột | Ý nghĩa |\n|---|---|\n")
    f.writelines(f"| `{k}` | {v} |\n" for k, v in DICT.items())
print("-> draft/data_dictionary_task4.md")

## CELL 2
# Việc 2a — Độ ổn định theo seed: 20 random_state, ARI so với nghiệm gốc (>0.8 = ổn định)
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score as ari
base = cons["cluster"].values
seed_ari = [ari(base, KMeans(K, n_init=10, random_state=s).fit_predict(X)) for s in range(20)]
print(f"ARI theo 20 seed: min {min(seed_ari):.3f} · TB {np.mean(seed_ari):.3f}")

## CELL 3
# Việc 2b — Bootstrap 80% x 50 lần: fit lại trên mẫu con, gán lại cả 999 khách, đo ARI
rng = np.random.default_rng(42)
boot_ari = []
for _ in range(50):
    idx = rng.choice(len(X), int(0.8 * len(X)), replace=False)
    boot_ari.append(ari(base, KMeans(K, n_init=10, random_state=42).fit(X[idx]).predict(X)))
print(f"ARI bootstrap 80%: TB {np.mean(boot_ari):.3f} · 5th pct {np.percentile(boot_ari, 5):.3f}")

## CELL 4
# Việc 2c — So với GMM (gán mềm): ARI k-means vs GMM + % khách 'ở biên' (xác suất cao nhất < 0.6)
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(K, covariance_type="full", n_init=5, random_state=42).fit(X)
g_lab, g_p = gmm.predict(X), gmm.predict_proba(X).max(1)
print(f"ARI k-means vs GMM: {ari(base, g_lab):.3f}")
print(f"Khách ở biên (p<0.6): {(g_p < 0.6).sum()} ({(g_p < 0.6).mean():.1%})")
print(pd.crosstab(cons["segment"], g_lab, rownames=["k-means"], colnames=["GMM"]))

## CELL 5
# Việc 2d — PCA 2D tô màu segment (chart cho slide mới)
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
pca = PCA(2, random_state=42).fit(X); P2 = pca.transform(X)
fig, ax = plt.subplots(figsize=(9, 6))
for s in cons["segment"].unique():
    m = (cons["segment"] == s).values
    ax.scatter(P2[m, 0], P2[m, 1], s=12, alpha=.7, label=f"{s} ({m.sum()})")
ax.set(xlabel=f"PC1 ({pca.explained_variance_ratio_[0]:.0%} variance)",
       ylabel=f"PC2 ({pca.explained_variance_ratio_[1]:.0%} variance)",
       title="Four segments in PCA space (8 z-scaled features, 999 consumers)")
ax.legend(fontsize=8, loc="best"); fig.tight_layout()
fig.savefig("outputs/figures/t4_pca.png", dpi=150); plt.show()

## CELL 6
# Việc 3 — Dịch chuyển segment theo tháng: gán MỖI consumer-month vào centroid gần nhất (cùng scaler)
mon = mon.sort_values(["consumer_id", "analysis_month"])
name = dict(zip(cons["cluster"], cons["segment"]))
mon["seg"] = pd.Series(km.predict(scaler.transform(mon[feat])), index=mon.index).map(name)
mon["seg_next"] = mon.groupby("consumer_id")["seg"].shift(-1)
tr = mon.dropna(subset=["seg_next"])
print("Ma trận chuyển tháng t -> t+1 (% theo hàng):")
print((100 * pd.crosstab(tr.seg, tr.seg_next, normalize="index")).round(1))
H, S = "Financially Healthy & Highly Engaged", "Financially Stretched but Highly Engaged"
mon["m"] = pd.to_datetime(mon["analysis_month"]).dt.month
h = tr.assign(m=mon.loc[tr.index, "m"]).query("seg == @H")
slide = h.groupby("m")["seg_next"].apply(lambda s: (s == S).mean() * 100).round(1)
print("\n% tháng Healthy trượt sang Stretched ở tháng kế tiếp, theo tháng xuất phát:")
print(slide.to_string())
print(f"-> TB cả năm {slide.mean():.1f}% | T10->T11 {slide.get(10, np.nan)}% | T11->T12 {slide.get(11, np.nan)}%")

## CELL 7
# Việc 4 — Hồ sơ nhân khẩu từng segment (kiểm tra segment có trùng nhân khẩu học không)
bins = [14, 17, 24, 34, 44, 54, 64, 120]
labs = ["15-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]   # giữ 7 khách 15–17 tuổi
ds["age_grp"] = pd.cut(ds.age, bins, labels=labs)
print("Tuổi TB:\n", ds.groupby("segment").age.agg(["mean", "median"]).round(1))
print("\n% giới tính:\n", (100 * pd.crosstab(ds.segment, ds.gender, normalize="index")).round(1))
print("\n% nhóm tuổi:\n", (100 * pd.crosstab(ds.segment, ds.age_grp, normalize="index")).round(1))
print("\nTop 3 tỉnh mỗi segment:")
for s, g in ds.groupby("segment"):
    print(f"  {s}: " + ", ".join(f"{p} {v:.0%}" for p, v in g.province.value_counts(normalize=True).head(3).items()))
from scipy.stats import chi2_contingency
for col in ["gender", "age_grp"]:
    p = chi2_contingency(pd.crosstab(ds.segment, ds[col]))[1]
    print(f"Chi-square segment x {col}: p = {p:.3f}  ({'có liên quan' if p < .05 else 'không khác biệt có ý nghĩa'})")

## CELL 8
# Việc 5 — Ánh xạ sang 6 tên gợi ý của đề: 2x2 rule + 2 nhóm đề gợi ý nằm ở đâu
print((pd.crosstab(cons["segment"], cons["rule2x2"], margins=True)))
ess = cons["discretionary_spend_ratio"] < 0.40            # 'Essential-Spend-Focused': essential > 60%
print(f"\nEssential-focused (discretionary < 40%): {ess.sum()} khách")
print(cons.loc[ess, "segment"].value_counts())
hd = (cons.financial_health_score >= 70) & (cons.engagement_score < 70)   # cutoff của P3 (kiểm lại với P3)
print(f"\nHealthy but Disengaged (FHS>=70 & engagement<70): {hd.sum()} khách")
print(cons.loc[hd, "segment"].value_counts())
