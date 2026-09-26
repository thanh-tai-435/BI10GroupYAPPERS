# Phân công 5 người — làm sâu BI10 Round 01 (YAPPERS)

> Hôm nay 26/09. **Deadline nộp: 23:59 ngày 28/09/2026.** Còn ~2 ngày → mục tiêu là *làm sâu và làm chắc* những gì đã có, KHÔNG làm lại từ đầu.
> Deck hiện có 18 slide, giới hạn 22 → còn **4 slide trống**, đã chia sẵn bên dưới (P1, P2, P4, P5 mỗi người +1).

---

## 0. Quy tắc chung (ai cũng phải đọc)

**Luật của đề (sai là mất điểm nặng):**
1. Đây là nghiên cứu *wellbeing*, KHÔNG phải chấm điểm tín dụng. `financial_health_score` không bao giờ được dùng để từ chối tín dụng, giảm hạn mức, tăng lãi, khoá tài khoản. Không viết câu nào gợi ý điều đó.
2. So sánh bằng **tỷ lệ / tỷ trọng**, không so VND tuyệt đối (số liệu tổng hợp bị thổi phồng).
3. Mỗi nhận định phải có **một con số hoặc một chart** đi kèm.

**Setup máy (làm 1 lần, ~15 phút):**
```bash
git pull
# Copy thư mục BI10_ROUND01_DATASET/ vào gốc repo (bị git-ignore, xin file từ P5)
npm install                              # chỉ P5 cần (build deck)
PYTHONUTF8=1 py draft/taskN*.py          # chạy thử task của mình, so với taskN_output.txt
```
- Dùng `py`, **không** dùng `python`. Script nào in tiếng Việt phải có `sys.stdout.reconfigure(encoding="utf-8")`.
- Chỉ dùng 2 file: `consumer_financial_health_engagement_2025.csv` (tháng) và `consumer_transactions_2025.parquet/consumer_transactions_2025.csv` (giao dịch). **Không** dùng 2 file `.gz`.
- Không bỏ 7 khách 15–17 tuổi khi chia nhóm tuổi.

**Quy tắc sửa file (để không conflict git):**
| File | Ai được sửa |
|---|---|
| `draft/taskN*.py`, `taskN_output.txt`, `taskN_findings.md` | Chủ task N |
| `draft/make_charts.py` | Mỗi người **chỉ sửa khối `# TASK N` của mình** |
| `draft/slide_outline.md` | Mỗi người **chỉ sửa các slide mình sở hữu** |
| `draft/build_deck.js`, file `.pptx` | **Chỉ P5** |

- Mỗi người làm trên nhánh riêng: `git checkout -b p1-task1` (p2-task2, …). Xong thì push + báo P5 merge.
- **Đổi bất kỳ con số nào** → sửa luôn trong `findings.md` + `slide_outline.md` và nhắn P5 (vì số đó có thể nằm ở Executive Summary / slide 17–18).
- Sau khi sửa script: chạy lại và lưu output: `PYTHONUTF8=1 py draft/taskN.py > draft/taskN_output.txt`.

**Định nghĩa "xong" cho mỗi hạng mục làm sâu:** có code chạy được + số trong `taskN_output.txt` + 2–4 dòng insight trong `findings.md` + (nếu lên slide) chart PNG trong `outputs/figures/` + bullet trong `slide_outline.md`.

---

## 1. Tổng quan phân công

| Người | Phụ trách | Slide sở hữu | Slide mới |
|---|---|---|---|
| **P1** | Task 1 — EDA + slide Giới thiệu | 4, 5, 6, 7 | +1: Q3 kênh theo tỉnh / độ dốc Q2 |
| **P2** | Task 2 — Financial Health | 8, 9, 10 | +1: Khác biệt theo nghề / tuổi / tỉnh (Q3) |
| **P3** | Task 3 — Engagement | 11, 12, 13 | 0 (làm chart tốt hơn thay vì thêm slide) |
| **P4** | Task 4 — Segmentation + dataset nộp kèm | 14, 15 | +1: Kiểm định & dịch chuyển segment |
| **P5** | Task 5 — Recommendations + ráp deck + nộp bài (Lead tích hợp) | 1, 2, 3, 16, 17, 18 | +1: Tác động & lộ trình triển khai |

Tổng sau khi làm: 18 + 4 = **22 slide** (đúng giới hạn). Ai muốn thêm nữa → đưa vào phụ lục trong ZIP, không đưa vào deck.

---

## 2. P1 — Task 1: Exploratory Data Analysis

**Đã có:** `draft/task1_eda.py`, `task1_findings.md`, chart `t1_monthly_spend`, `t1_essential_discretionary`, `t1_category_ticket`, `t1_age_cohort`. Slide 4–7.

**Việc cần làm sâu (theo thứ tự ưu tiên):**

1. **[BẮT BUỘC] Q3 — bảng kênh chi tiết theo tỉnh.** Đề yêu cầu *"compare their channel breakdown (POS vs digital channels)"* cho ≥2 tỉnh. Hiện mới có digital share tổng.
   - Với 5 tỉnh (Hà Nội, Đồng Nai, Lâm Đồng, Hưng Yên, Hải Phòng) + toàn quốc: tỷ trọng **số giao dịch** và **giá trị chi tiêu** theo POS / QR / E-com / Mobile / Recurring.
   - Code gợi ý: `tx.merge(monthly[['consumer_id','province_city']].drop_duplicates(), on='consumer_id')` → `pd.crosstab(province, channel, values=amount, aggfunc='sum', normalize='index')`.
   - Chart: stacked bar 100% ngang (6 thanh). Kết luận giữ nguyên: chênh lệch trong ±0.5pp → địa lý *không* phải đòn bẩy. Đây là nội dung **slide mới**.
2. **Q2 — chứng minh độ dốc, không chỉ 2 đầu.** Chia FHS theo decile (hoặc bin 10 điểm), tính tỷ trọng discretionary từng bin → line chart. Nếu đường giảm đều → "đảo chiều là liên tục, không phải do ngưỡng 40/80". Thêm kiểm tra ngưỡng khác (FHS<45 vs ≥75) để chứng minh độ bền. Đưa vào slide 6 hoặc slide mới.
3. **Q1 — tháng 12 tăng vì category nào?** Tính mức tăng số giao dịch T12 vs T2 theo từng category → top 5 category đóng góp. Kiểm tra caveat "gộp 2 năm vào 2025" bằng cách nhìn timestamp gốc (có năm 2024 không?) và ghi rõ kết quả.
4. **Q4 — bổ sung** % khách có mua Fuel / Groceries, số lần mua trung bình/khách/tháng.
5. **Q5 — chứng minh tuổi là tín hiệu yếu** bằng bootstrap CI 95% của FHS trung bình từng nhóm tuổi (`np.random.choice` 1000 lần). Nếu các CI chồng nhau → nói rõ.

**Slide 4 (Giới thiệu):** rà lại con số dataset (999 khách, 1,852,394 giao dịch, 10,992 consumer-month) và 2 luật (tỷ lệ, wellbeing).

**Giao cho P5:** bullet slide 4–7 + slide mới trong `slide_outline.md`, chart mới đặt tên `t1_*.png`.

---

## 3. P2 — Task 2: Financial Health

**Đã có:** `draft/task2.py`, `task2_findings.md`, chart `t2_fhs_distribution`, `t2_low_health_drivers`, `t2_crossover`. Slide 8–10.

**Việc cần làm sâu:**

1. **[BẮT BUỘC] Deliverable 3 — "Differences by occupation, age, province" chưa có slide riêng.** Làm **slide mới**:
   - **Tỉnh:** dot plot FHS trung bình ± CI 95% cho các tỉnh ≥15 khách, có đường trung bình toàn quốc.
   - **Nghề:** 396 nghề × tối đa 10 khách → không dùng được thô. Gom thành ~6–8 nhóm nghề bằng từ khoá tiếng Việt (vd. "sinh viên/học sinh", "kinh doanh/buôn bán", "nhân viên/văn phòng", "công nhân/lao động", "giáo viên/bác sĩ/kỹ sư", "hưu trí", "khác"). Viết dict mapping rõ ràng trong code để tái lập được. Sau đó so FHS + spend_to_income theo nhóm.
   - **Tuổi:** dùng lại bảng 6 nhóm tuổi (lấy CI từ P1 nếu có, thống nhất số với P1).
   - Kết luận mong đợi: nhân khẩu học chênh ít → nhắm theo tỷ lệ hành vi. Nói thẳng nếu có nhóm nghề nào khác biệt thật.
2. **Dùng file giao dịch như đề gợi ý (day-of-week / giờ).** So sánh tháng stressed (FHS<40) vs healthy (FHS≥80): tỷ trọng chi tiêu theo thứ trong tuần và theo giờ, tỷ trọng category discretionary. Nếu thấy pattern (vd. stress chi nhiều cuối tuần / đêm khuya) → đó là **thời điểm gửi Spend Alert** cho P5.
3. **Crossover — bảng độ nhạy của luật.** Tính số khách / số tháng / % tổng stress episode khi đổi ngưỡng: FHS <35/<40/<45 × engagement ≥p70/p75/p80. Chứng minh 43 khách là lựa chọn hợp lý, không phải ngẫu nhiên. Đưa bảng nhỏ vào slide 10.
4. **Q2 — thêm kiểm chứng ngoài tương quan:** so sánh FHS theo quintile của spend_to_income (bar chart) — trực quan hơn con số r = −0.90.

**Lưu ý:** giữ caveat "FHS và các tỷ lệ dùng chung trường chi tiêu → định hướng, không phải nhân quả".

**Giao cho P5:** bullet slide 8–10 + slide mới; báo P5 nếu con số 43 / 52% thay đổi (nằm ở slide 2, 16, 17, 18).

---

## 4. P3 — Task 3: Customer Engagement

**Đã có:** `draft/task3.py`, `task3_findings.md`, chart `t3_engagement_dist`, `t3_channel_mix`, `t3_diversity_vs_engagement`, `t3_health_vs_engagement_quadrant`. Slide 11–13.

Task 3 có yêu cầu riêng: *"chart phải phù hợp với dữ liệu"* (Objective 6) → P3 tập trung **chất lượng chart + đủ từng deliverable**, không thêm slide.

**Việc cần làm sâu:**

1. **Deliverable 1:** ghi rõ % khách trong **từng** engagement segment (không chỉ "99% high/very high") — thêm vào chart phân phối (histogram + nhãn % từng nhóm).
2. **Deliverable 2:** nêu rõ con số **"average online spend share"** (trung bình `online_spend_ratio` cấp khách) trên slide 11. Thêm: kênh theo nhóm tuổi hoặc theo segment của P4 (lấy nhãn từ `task4_features.csv`) → ai là người dùng QR / Mobile.
3. **Deliverable 3:** thêm histogram phân phối category diversity (khoảng 2–14) bên cạnh scatter. Kiểm tra r = +0.94 có bị kéo bởi nhóm đuôi nhỏ không: tính lại r chỉ trên khách có diversity ≥ 8.
4. **Deliverable 4:** làm **heatmap Recency × Frequency** (bin recency × bin số ngày hoạt động, màu = engagement trung bình). Chart này "phù hợp dữ liệu" hơn bảng số.
5. **Deliverable 5 (Q5):** làm **bảng độ nhạy cutoff** — số khách khi FHS ≥ 65/70/75 × engagement < 60/65/70/75. Đề hỏi rõ *"tại sao chọn cutoff này thay vì chặt hơn / lỏng hơn"* → bảng này là câu trả lời. Đưa lên slide 13.
6. **Viết 1 dòng "vì sao chọn loại chart này"** cho mỗi chart trong `task3_findings.md` (vd. histogram vì biến liên tục, lệch trái). P5 có thể đưa vào speaker note.

**Giao cho P5:** bullet slide 11–13 (có thể thay chart), không thêm slide.

---

## 5. P4 — Task 4: Customer Segmentation

**Đã có:** `draft/task4.py` (k-means k=4, silhouette 0.251, 999/999), `task4_features.csv`, chart `t4_segment_sizes`, `t4_segment_profiles`, `t4_silhouette`. Slide 14–15.

**Việc cần làm sâu:**

1. **[BẮT BUỘC] Deliverable "Preprocessed Dataset".** Xuất file sạch cho ZIP nộp kèm:
   - `task4_features.csv`: 1 dòng/khách, 8 feature thô + 8 feature đã z-scale + nhãn segment + các cột nhân khẩu (để minh bạch).
   - Kèm `data_dictionary_task4.md`: tên cột, ý nghĩa, công thức, đơn vị. Gửi cả hai cho P5.
2. **Kiểm định độ bền (slide mới):**
   - Chạy k-means với 20 `random_state` khác nhau → Adjusted Rand Index (`sklearn.metrics.adjusted_rand_score`) so với nghiệm gốc. ARI > 0.8 = ổn định.
   - Bootstrap 80% mẫu × 50 lần → % khách giữ nguyên segment.
   - So với GMM (`sklearn.mixture.GaussianMixture`, k=4): ARI giữa 2 mô hình + tỷ lệ khách có xác suất thành viên < 0.6 (= "khách ở biên").
   - Chart: PCA 2D scatter tô màu theo segment (`sklearn.decomposition.PCA`).
3. **Dịch chuyển segment theo tháng (giá trị cao cho Task 5):** gán mỗi dòng consumer-month vào centroid gần nhất (dùng cùng scaler) → ma trận chuyển tiếp tháng t → t+1. Trả lời: bao nhiêu % khách Healthy trượt sang Stretched trong tháng 11–12? Đây là bằng chứng cho "stress theo đợt" và cho Planning Reminder trước tháng 12.
4. **Hồ sơ nhân khẩu từng segment** (tuổi, giới, top tỉnh) → chứng minh segment không trùng nhân khẩu học → công bằng. Đồng bộ số giới tính (56.6% vs 49.4%) với P5.
5. **Ánh xạ sang tên gợi ý của đề** (Healthy & Engaged, Stretched but Engaged, Emerging Digital, …): bảng 1 dòng giải thích vì sao "Healthy but Disengaged" và "Essential-Spend-Focused" không thành cụm riêng (nhóm 25 khách của P3 nằm ở segment nào?).
6. **Limitations & Future Work:** đã có trong findings — đảm bảo có ít nhất 3 bullet trên slide 15 hoặc slide mới.

**Giao cho P5:** bullet slide 14–15 + slide mới, file dataset + dictionary.

---

## 6. P5 — Task 5 + ráp deck + nộp bài

**Đã có:** `draft/task5.py`, `task5_findings.md`, chart `t5_priority_ranking`, `t5_target_sizes`, `build_deck.js`, `YAPPERS_BI10_R01.pptx`. Slide 1–3, 16–18.

**A. Làm sâu Task 5:**
1. **Slide mới "Tác động dự kiến & lộ trình":**
   - Ước tính kịch bản: hồi quy đơn `FHS ~ spend_to_income` (cấp tháng). Nếu Budgeting giúp 302 khách giảm spend/income 5% / 10% → FHS tăng bao nhiêu, bao nhiêu tháng thoát khỏi FHS<40? Ghi rõ là *kịch bản giả định*, không phải dự báo.
   - Mỗi công cụ 1 **KPI đo lường** (vd. Alerts → % tháng stress giảm; Nudges → category diversity tăng) và cách đo: **A/B test** (nhóm đối chứng ngẫu nhiên).
   - Lộ trình 30/60/90 ngày: pha 1 Budgeting + Alerts, pha 2 Reminders (trước tháng 12), pha 3 còn lại.
2. **Cập nhật 6 đề xuất** với input mới từ đồng đội: giờ/ngày gửi alert (P2), tỷ lệ trượt segment tháng 11–12 (P4), khách dùng QR/Mobile (P3).
3. Giữ nguyên **luật tín dụng tuyệt đối** trên slide 17 — đọc lại toàn deck, xoá mọi câu có thể hiểu là dùng FHS cho quyết định tín dụng.

**B. Ráp deck (người duy nhất sửa `build_deck.js`):**
1. Merge nhánh của P1–P4, chạy lại toàn bộ:
   ```bash
   for n in 1_eda 2 3 4 5; do PYTHONUTF8=1 py draft/task$n.py > draft/task${n%%_*}_output.txt; done
   PYTHONUTF8=1 py draft/make_charts.py
   node draft/build_deck.js
   "/c/Program Files/LibreOffice/program/soffice.exe" --headless --convert-to pdf --outdir draft/ draft/YAPPERS_BI10_R01.pptx
   pdftoppm -png -r 100 draft/YAPPERS_BI10_R01.pdf draft/slide
   ```
2. Thêm 4 slide mới đúng vị trí: sau slide 7 (P1), sau slide 10 (P2), sau slide 15 (P4), trước Closing (P5). Cập nhật Table of Contents (slide 3).
3. **Soát nhất quán số:** mọi con số trên slide 2 (Executive Summary) và 16–18 phải khớp với findings mới nhất.
4. QA hình: xem từng PNG, không chữ tràn, không chart bị méo, font đọc được, **≤22 slide, 16:9, tiếng Anh**, mọi chart có caption/nguồn.

**C. Nộp bài:**
- Đổi tên deck: `YAPPERS_<TênLeader>_BI10_R01.pptx`.
- ZIP phụ: `YAPPERS_<TênLeader>_BI10_R01_data.zip` gồm `draft/*.py`, `*_output.txt`, `*_findings.md`, `task4_features.csv` + dictionary, `outputs/figures/`.
- Nộp trước **20:00 ngày 28/09** (để dư 4 tiếng phòng sự cố).

---

## 7. Lịch làm việc

| Mốc | Việc | Ai |
|---|---|---|
| **26/09 tối** | Setup, chạy lại script của mình, đọc findings + slide outline của mình | Tất cả |
| **27/09 12:00** | Xong phần phân tích làm sâu, push code + output | P1–P4 |
| **27/09 18:00** | Xong chart + cập nhật findings + bullet slide trong outline | P1–P4 |
| **27/09 23:00** | Deck v2 (22 slide) + PDF gửi nhóm | P5 |
| **28/09 12:00** | Review chéo: P1↔P2, P3↔P4 soát số & logic; P5 soát toàn deck + luật tín dụng | Tất cả |
| **28/09 18:00** | Đóng băng nội dung, build bản cuối | P5 |
| **28/09 20:00** | Nộp bài | P5 |

**Checklist review chéo (người review tick từng ô):**
- [ ] Mỗi bullet có số hoặc chart
- [ ] Không so VND tuyệt đối giữa khách
- [ ] Không câu nào gợi ý dùng FHS cho tín dụng
- [ ] Số trên slide = số trong `taskN_output.txt`
- [ ] Chart có tiêu đề, trục, đơn vị, nguồn
- [ ] Caveat đặt đúng chỗ (dữ liệu tổng hợp, mẫu nhỏ)
