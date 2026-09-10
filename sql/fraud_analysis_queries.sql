/* =========================================================
   Credit Card Fraud Detection - SQL Analysis
   Dataset: Kaggle "Credit Card Fraud Detection" (284,807 txns)
   Table: transactions(Time, V1..V28, Amount, Class)
   Class: 0 = legitimate, 1 = fraud
   ========================================================= */

-- 1. Overall class balance (fraud is extremely rare)
SELECT
    Class,
    COUNT(*)                                   AS txn_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM transactions), 4) AS pct_of_total
FROM transactions
GROUP BY Class;

-- 2. Fraud rate as a plain ratio (for the "1 in N" resume stat)
SELECT
    (SELECT COUNT(*) FROM transactions)                        AS total_txns,
    (SELECT COUNT(*) FROM transactions WHERE Class = 1)         AS fraud_txns,
    ROUND((SELECT COUNT(*) FROM transactions) * 1.0 /
          (SELECT COUNT(*) FROM transactions WHERE Class = 1), 0) AS one_fraud_per_n_txns;

-- 3. Amount distribution by class (legit vs fraud)
SELECT
    Class,
    COUNT(*)              AS txn_count,
    ROUND(AVG(Amount), 2) AS avg_amount,
    ROUND(MIN(Amount), 2) AS min_amount,
    ROUND(MAX(Amount), 2) AS max_amount,
    ROUND(SUM(Amount), 2) AS total_amount
FROM transactions
GROUP BY Class;

-- 4. Total money at risk vs total money moved
SELECT
    ROUND(SUM(CASE WHEN Class = 1 THEN Amount ELSE 0 END), 2)  AS total_fraud_amount,
    ROUND(SUM(Amount), 2)                                       AS total_amount,
    ROUND(100.0 * SUM(CASE WHEN Class = 1 THEN Amount ELSE 0 END)
          / SUM(Amount), 4)                                     AS pct_value_lost_to_fraud
FROM transactions;

-- 5. Transaction volume by hour of day
--    (Time = seconds elapsed since first transaction in the dataset,
--     dataset spans ~2 days, so Time % 86400 gives seconds-into-day)
SELECT
    CAST((Time % 86400) / 3600 AS INTEGER)      AS hour_of_day,
    COUNT(*)                                     AS txn_count,
    SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END)   AS fraud_count,
    ROUND(100.0 * SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END) / COUNT(*), 4) AS fraud_rate_pct
FROM transactions
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- 6. Hours with the highest fraud RATE (not just count) - flags risky windows
SELECT
    CAST((Time % 86400) / 3600 AS INTEGER)      AS hour_of_day,
    COUNT(*)                                     AS txn_count,
    SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END)   AS fraud_count,
    ROUND(100.0 * SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END) / COUNT(*), 4) AS fraud_rate_pct
FROM transactions
GROUP BY hour_of_day
HAVING COUNT(*) > 100
ORDER BY fraud_rate_pct DESC
LIMIT 10;

-- 7. Amount buckets - where does fraud concentrate?
SELECT
    CASE
        WHEN Amount = 0 THEN '0'
        WHEN Amount <= 10 THEN '0-10'
        WHEN Amount <= 50 THEN '10-50'
        WHEN Amount <= 100 THEN '50-100'
        WHEN Amount <= 500 THEN '100-500'
        WHEN Amount <= 1000 THEN '500-1000'
        ELSE '1000+'
    END AS amount_bucket,
    COUNT(*)                                    AS txn_count,
    SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END)  AS fraud_count,
    ROUND(100.0 * SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END) / COUNT(*), 4) AS fraud_rate_pct
FROM transactions
GROUP BY amount_bucket
ORDER BY MIN(Amount);

-- 8. Top 20 highest-value fraudulent transactions (for a "biggest losses" callout)
SELECT Time, Amount, Class
FROM transactions
WHERE Class = 1
ORDER BY Amount DESC
LIMIT 20;

-- 9. Running/day-level split (dataset covers ~2 days: day 0 and day 1)
SELECT
    CAST(Time / 86400 AS INTEGER)               AS day_number,
    COUNT(*)                                     AS txn_count,
    SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END)   AS fraud_count
FROM transactions
GROUP BY day_number;
