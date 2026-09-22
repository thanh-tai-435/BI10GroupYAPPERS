# BI10_ROUND01

## Table of Contents

1. Business context
2. Dataset overview
3. Task 1 - Exploratory data analysis
4. Task 2 - Financial health analysis
5. Task 3 - Customer engagement analysis
6. Task 4 - Customer segmentation
7. Task 5 - Business recommendations
8. Submission guidelines
9. Contact information

---

## Business context

> This case focuses on customer understanding and segmentation, **NOT** credit-risk decision-making.
> `financial_health_score` must not be used as a basis for approving or denying credit, reducing a credit limit, or blocking an account.

ITB, a consumer finance company in Vietnam, provides cards and short-term credit products to retail customers.

The company wants to better understand customer financial wellbeing, spending behavior, and engagement with its transaction channels. It is interested in how these patterns vary across customer groups, how financial health and engagement relate to one another, and whether distinct behavioral patterns can be identified across the customer base.

Using the provided data, participants are expected to identify meaningful customer patterns and segments, explain their business implications, and propose practical actions that can support customer engagement and financial wellbeing.

---

## Dataset overview

Both datasets cover calendar year 2025 and can be linked using `consumer_id`. Monetary values are expressed in VND.

**Datasets provided:**

- **consumer_financial_health_engagement_2025** — consumer-month data, where each row summarizes one customer's activity and financial indicators for a calendar month. Contains monthly financial-health, engagement, and customer-level indicators. Fields such as `financial_health_score`, `engagement_score`, ratio-based measures, and synthetic income, credit, and balance fields are available only at this grain.
- **consumer_transaction_2025** — transaction-level data, where each row represents an individual customer transaction. Provides category, merchant, channel, payment method, amount, and timestamp detail. Use it when monthly aggregates do not retain the detail required for an analysis.

A separate data dictionary is provided with field definitions, data types, units, and valid values.

**Note:** All data is synthetic and does not represent real individuals or actual customer financial records. Synthetic income, credit-limit, and balance values should not be interpreted as realistic absolute amounts. Ratio-based measures are more appropriate for comparisons across customers.

---

## Task 1 - Exploratory Data Analysis

### Objectives

1. Analyze seasonal spending trajectories and decompose drivers behind peak consumption periods.
2. Evaluate spending structure differences (Essential vs. Discretionary) across financial health segments.
3. Identify regional digital channel adoption gaps in high-volume economic hubs.
4. Compare purchasing behaviors across merchant categories using transaction frequency vs. spend volume metrics.
5. Profile demographic financial vulnerability across age cohorts to uncover drivers of low health scores.

### Questions

1. Which month records the highest total spend, and how much does it account for (in VND and as a % of annual spend) compared to the lowest spending month? Is this peak driven primarily by higher transaction count or larger ticket sizes? What does this pattern reveal about consumer spending behavior during peak periods?
2. Compare the proportion of Essential vs. Discretionary spend between financially stressed customers (`financial_health_score < 40`) and healthy customers (`financial_health_score ≥ 80`). What does this spending composition reveal about how financial stress alters a customer's budget allocation?
3. Identify 2 or more provinces/cities that generate high total spend volume but have a lower-than-average digital transaction share. Compare their channel breakdown (POS vs. digital channels) to quantify and explain the nature of their digital adoption gap.
4. Identify the top category by transaction count and the top category by total spend volume. Compare their average ticket sizes (VND per transaction) and explain how consumer usage behavior differs between these two categories.
5. Which age cohort maintains active transaction frequency while recording the lowest average `financial_health_score`? Contrast their spending metrics (essential spend ratio and spend-to-income ratio) with other age cohorts to explain the drivers of their financial vulnerability.

### Deliverables

1. Quantitative analysis answering EDA Questions Q1 through Q5 with exact numbers, percentages, and ratios.
2. Decomposition of spending drivers (transaction volume vs. ticket size; essential vs. discretionary allocation).
3. Identification of top-performing and lagging regional/channel and category segments.
4. Business interpretations explaining consumer behavioral patterns and risk/opportunity drivers behind the data.

---

## Task 2 - Financial Health Analysis

### Task brief

Analyze customer financial health and produce a report covering the required elements.

### Data notes

The consumer-month file is the primary source for this task. The raw transaction file is there to let participants go deeper: merchant- and category-level detail, exact timestamps, and day-of-week/hour patterns that the aggregate file collapses away.

### Constraints

- Use ratio-based fields, not raw VND magnitudes, wherever comparing across customers.
- All claims must be backed by a number or chart; no unsupported assertions.

### Deliverables

1. Distribution of `financial_health_score`.
2. Main factors associated with low health.
3. Differences by occupation, age, and province.
4. Identify customers who are financially stressed but highly engaged; define and apply a clear, reproducible rule to identify this crossover segment.

---

## Task 3 - Customer Engagement Analysis

### Objectives

1. Show how `engagement_score` is spread across the customer base.
2. Show which channels customers use, and how much of their spend is digital.
3. Show how many spending categories a customer typically uses.
4. Show how often and how recently customers transact.
5. Find customers who are financially healthy but not engaged — a group at risk of leaving even though they are good customers. State the score cutoff used to define "high" and "low", since the task does not give one.
6. Use a chart that fits the data for each part, so a reader can see the pattern, not just read numbers.

### Deliverables

1. The engagement score distribution, with the share of customers in each engagement segment.
2. A channel adoption breakdown (POS, QR, E-commerce, Mobile App, Recurring), plus the average online spend share.
3. The category diversity range, and how it links to engagement.
4. The recency and frequency ranges, and how they link to engagement.
5. The exact size and profile of the high-health, low-engagement group, plus the cutoff used and why it was chosen over a stricter or looser one.
6. A chart type that fits the data, rather than just any chart.

---

## Task 4 - Customer Segmentation

### Objectives

Develop a data-driven approach to group customers into distinct segments that drive actionable business strategy.

The model can be rule-based and/or clustering (e.g., k-means on scaled ratio features, or a 2×2 health×engagement matrix).

Suggested groups (not mandatory):

- Financially Healthy & Highly Engaged
- Financially Healthy but Disengaged
- Financially Stretched but Highly Engaged
- Low Engagement & Financially Vulnerable
- Emerging Digital Customers
- Essential-Spend-Focused Customers

### Instructions

**1. Data Preprocessing & Feature Engineering**

Prepare data for effective segmentation. Focus on relevant metrics across the following dimensions (metrics are recommended but not compulsory):

- **Customer Demographics:** age, gender, occupation, province_city
- **Financial Health:** Monthly Income, Credit Limit, Credit Utilization, Financial Health Score, Financial Health Segment, Average Transaction, Spending Volatility, etc.
- **Engagement Health:** #Transaction, Active Transaction Days, Engagement Score, etc.
- **Credit Spending Behavior:** Category Diversity, Essential spend ratio, Discretionary spend ratio, Online spend ratio, etc.

**2. Customer Segmentation Model**

- **Feature Selection & Engineering:** Select key metrics and construct additional relevant ratios (optional) to capture both financial health and engagement.
- **Model Selection & Setup:** Choose an appropriate algorithm (e.g., K-Means, GMM, or Rule-Based Matrix) and justify parameters based on data.
- **Implementation & Validation:** Build your rules or model, verify 100% population coverage, and validate cluster quality or rule distributions.
- **Customer Profiling:** Assign business-oriented labels to each customer group.
- **Post-Segmentation Analysis:** Compare group metrics side-by-side to highlight key behavioral differences and provide business recommendations.

**3. Limitations and Future Work**

- Identify technical and operational limitations in the assignment.
- Suggest improvements for future work.

### Deliverables

- **Preprocessed Dataset:** Cleaned and transformed dataset, including all engineered features used in modeling.
- **Customer Segmentation Model:** Clustering model OR rule-based model with a detailed analysis of segment profiles, highlighting key differentiating attributes.
- **Limitations and Future Work:** Critical reflection on data or modeling constraints, potential biases, and suggestions for future enhancements or extensions.

---

## Task 5 - Business Recommendations

### Task brief

Propose non-punitive interventions: budgeting tools, spend alerts, financial-planning reminders, financial-education content, digital-channel nudges, and suitable product suggestions.

### Objectives

- Build a clear, non-punitive action plan that covers all 6 tool types.
- Base every idea on a real finding from the data, not a generic idea.
- State how many customers each idea can reach.
- Rank the ideas by reach and by how strong the driver is.
- Keep one rule at all times: `financial_health_score` must never be used to deny credit, cut a credit limit, or block an account.

### Constraints

Do not propose denying credit on the basis of `financial_health_score`.

### Deliverables

- One clear proposal for each of the 6 tool types, each linked to a real number or column from the data.
- Clear target groups, with exact sizes and percentages.
- A clear statement of the credit-decision rule.

---

## Submission guidelines

### 1. Requirement

- Participants must complete the tasks in accordance with the instructions and requirements provided by ITB Club.
- The submission must clearly demonstrate the data analysis process, reasoning, and conclusions or recommendations of your team.
- All figures, charts, and images used in the submission must be presented clearly and include appropriate sources or captions.
- The content's accuracy and integrity must be ensured by the team's members.

### 2. Deadline

- We will only recognize the latest valid submission received before the deadline.
- After 23:59 on September 28, 2026, the submission form will be closed and no additional or replacement submissions will be accepted.

### 3. Tools

Teams are free to use any tools, software, or platform (Excel, Power BI, Google Colab, ...) throughout the data analysis process.

### 4. Submission format

- Submit 01 slide proposal representing the analysis results, with a maximum of 22 slides (including 01 Executive Summary and 01 Table of Contents).
- File name format: `[TeamName_LeaderName_BI10_R01]`.
- Language: English.
- Use a 16:9 slide format, with a maximum file size of 100 MB.

The slide proposal must include 04 sections:

1. Executive Summary
2. Table of Contents
3. Introduction to the Case
4. Analysis Results for Tasks 1–5

All additional files (if any) must be compressed into one ZIP/RAR file and named: `[TeamName_LeaderName_BI10_R01_data]`.

### Notes!

- All supporting files must be clearly named and usable at the time of evaluation.
- The Team Leader is responsible for submitting the final submission and verifying all information and files before submission. After completing the submission, teams must check for ITB CLUB's confirmation within 24 hours.
- Each team is encouraged to record their screen throughout the entire submission process, including file upload and confirmation of successful submission. The recording will serve as supporting evidence for verification in case of system errors or technical issues.

---

## Contact information

*(No contact details provided in the source document.)*
