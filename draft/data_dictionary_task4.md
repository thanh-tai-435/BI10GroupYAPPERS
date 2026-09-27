# Data dictionary — task4_features.csv

1 dòng / khách (999). Nguồn: consumer_financial_health_engagement_2025.csv, gộp 12 tháng bằng trung bình. Chỉ dùng tỷ lệ/điểm, không dùng VND tuyệt đối.

| Cột | Ý nghĩa |
|---|---|
| `consumer_id` | Mã khách (khoá, nối với 2 file gốc) |
| `financial_health_score` | TB 12 tháng của `financial_health_score` (file consumer-month), trục health |
| `spend_to_income_ratio` | TB 12 tháng của `spend_to_income_ratio` (file consumer-month), trục health |
| `credit_utilization_ratio` | TB 12 tháng của `credit_utilization_ratio` (file consumer-month), trục health |
| `spending_volatility` | TB 12 tháng của `spending_volatility` (file consumer-month), trục health |
| `engagement_score` | TB 12 tháng của `engagement_score` (file consumer-month), trục engagement |
| `transaction_count` | TB 12 tháng của `transaction_count` (file consumer-month), trục engagement |
| `discretionary_spend_ratio` | TB 12 tháng của `discretionary_spend_ratio` (file consumer-month), trục spending |
| `online_spend_ratio` | TB 12 tháng của `online_spend_ratio` (file consumer-month), trục spending |
| `z_financial_health_score` | `financial_health_score` đã chuẩn hoá z-score (StandardScaler, fit trên 999 khách) — input của k-means |
| `z_spend_to_income_ratio` | `spend_to_income_ratio` đã chuẩn hoá z-score (StandardScaler, fit trên 999 khách) — input của k-means |
| `z_credit_utilization_ratio` | `credit_utilization_ratio` đã chuẩn hoá z-score (StandardScaler, fit trên 999 khách) — input của k-means |
| `z_spending_volatility` | `spending_volatility` đã chuẩn hoá z-score (StandardScaler, fit trên 999 khách) — input của k-means |
| `z_engagement_score` | `engagement_score` đã chuẩn hoá z-score (StandardScaler, fit trên 999 khách) — input của k-means |
| `z_transaction_count` | `transaction_count` đã chuẩn hoá z-score (StandardScaler, fit trên 999 khách) — input của k-means |
| `z_discretionary_spend_ratio` | `discretionary_spend_ratio` đã chuẩn hoá z-score (StandardScaler, fit trên 999 khách) — input của k-means |
| `z_online_spend_ratio` | `online_spend_ratio` đã chuẩn hoá z-score (StandardScaler, fit trên 999 khách) — input của k-means |
| `cluster` | Nhãn cụm k-means (k=4, random_state=42, n_init=25) |
| `segment` | Tên segment nghiệp vụ gán theo cực trị của cụm |
| `rule2x2` | Nhãn kiểm chứng 2x2 health x engagement (chia theo median) — không phải mô hình chính |
| `age` | Tuổi (dùng để mô tả, KHÔNG đưa vào phân cụm) |
| `gender` | Giới tính (mô tả) |
| `occupation` | Nghề (mô tả) |
| `province` | Tỉnh/thành (mô tả) |
