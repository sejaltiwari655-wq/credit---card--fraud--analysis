Credit Card Fraud & Spend Analysis (SQL + Python)

**Dataset:** Kaggle Credit Card Fraud Detection — 284,807 transactions, 492 fraud (0.17%), Sept 2013, European cardholders.

## Objective
Analyze transaction patterns to understand where fraud concentrates (time, amount) and build a baseline model to automatically flag likely fraud — framed as a resume-ready SQL + Python analytics pipeline.

## Structure
```
creditcard_project/
├── data/creditcard.csv          # raw dataset (from Kaggle)
├── creditcard.db                # SQLite DB loaded from the CSV
├── sql/fraud_analysis_queries.sql   # 9 analysis queries (class balance, hourly fraud rate, amount buckets, etc.)
├── scripts/
│   ├── 01_sql_analysis.py       # runs all SQL queries, saves outputs/sql_results.md
│   ├── 02_eda_visuals.py        # EDA charts (class imbalance, amount dist, hourly fraud rate, correlations)
│   └── 03_fraud_model.py        # Logistic Regression + Random Forest baseline, evaluation
└── outputs/
    ├── sql_results.md           # all SQL query results
    ├── model_report.md          # model metrics (ROC-AUC, PR-AUC, confusion matrix)
    └── charts/                  # 7 PNG charts
```

## How to run
```bash
python3 scripts/01_sql_analysis.py     # SQL layer
python3 scripts/02_eda_visuals.py      # EDA charts
python3 scripts/03_fraud_model.py      # modeling + evaluation
```

## Key findings
- **Extreme class imbalance:** only 1 in 579 transactions is fraud (0.17%), but fraud accounts for **0.24% of total transaction value** — small in volume, disproportionately costly per transaction (avg fraud amount ₹122 vs ₹88 legit).
- **Time-of-day risk:** fraud rate spikes at **2 AM (1.71%)** and **4 AM (1.04%)** — far above the ~0.15% baseline during normal daytime hours, suggesting automated/off-hours attack patterns.
- **Amount concentration:** fraud rate is highest on **₹0 transactions (1.48%)** — consistent with card-testing behavior — and elevated again in the **₹500–1000** bracket (0.42%).
- **Top predictive features:** V17, V14, V12, V10 (PCA-anonymized) show the strongest correlation with fraud.

## Model results
| Model | ROC-AUC | PR-AUC | Fraud Recall | Fraud Precision |
|---|---|---|---|---|
| Logistic Regression (balanced) | 0.968 | 0.704 | 88% | 7% |
| **Random Forest (balanced)** | 0.966 | **0.790** | 75% | **87%** |

**Why PR-AUC over accuracy:** with 99.8% of transactions being legitimate, a model predicting "never fraud" scores 99.8% accuracy while catching zero fraud. Precision/recall and PR-AUC are the honest metrics for this problem.

**Takeaway:** Random Forest is the stronger production candidate — it flags fraud with 87% precision (few false alarms) while still catching 3 in 4 fraud cases, a realistic trade-off for a fraud-review queue.

## Resume-ready framing
> Built an end-to-end SQL + Python fraud detection pipeline on 284K+ transactions; identified fraud concentration by time-of-day and amount using SQL, then trained a Random Forest classifier achieving 87% precision / 75% recall on a 0.17%-imbalanced dataset (PR-AUC 0.79).
