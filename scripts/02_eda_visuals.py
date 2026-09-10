"""
EDA + visualizations for the Credit Card Fraud dataset.
Saves charts to outputs/charts/
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_theme(style="whitegrid")
CHART_DIR = "/home/claude/creditcard_project/outputs/charts"

df = pd.read_csv("/home/claude/creditcard_project/data/creditcard.csv")
df["hour_of_day"] = ((df["Time"] % 86400) // 3600).astype(int)

# 1. Class imbalance bar chart (log scale so the fraud bar is visible at all)
fig, ax = plt.subplots(figsize=(6, 5))
counts = df["Class"].value_counts().sort_index()
bars = ax.bar(["Legitimate (0)", "Fraud (1)"], counts.values, color=["#4C72B0", "#C44E52"])
ax.set_yscale("log")
ax.set_ylabel("Transaction count (log scale)")
ax.set_title("Class Imbalance: Legitimate vs Fraudulent Transactions")
for bar, val in zip(bars, counts.values):
    ax.text(bar.get_x() + bar.get_width() / 2, val, f"{val:,}", ha="center", va="bottom")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/01_class_imbalance.png", dpi=150)
plt.close()

# 2. Transaction amount distribution: fraud vs legit (log-scaled amount)
fig, ax = plt.subplots(figsize=(7, 5))
for cls, label, color in [(0, "Legitimate", "#4C72B0"), (1, "Fraud", "#C44E52")]:
    subset = df[df["Class"] == cls]["Amount"]
    subset_log = np.log1p(subset)
    sns.kdeplot(subset_log, label=label, fill=True, alpha=0.4, ax=ax, color=color)
ax.set_xlabel("log(1 + Transaction Amount)")
ax.set_title("Transaction Amount Distribution: Fraud vs Legitimate")
ax.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/02_amount_distribution.png", dpi=150)
plt.close()

# 3. Fraud rate by hour of day
hourly = df.groupby("hour_of_day")["Class"].agg(["count", "sum"])
hourly["fraud_rate_pct"] = 100 * hourly["sum"] / hourly["count"]

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(hourly.index, hourly["count"], color="#8FBCE6", label="Total transactions")
ax1.set_xlabel("Hour of day")
ax1.set_ylabel("Total transactions", color="#4C72B0")
ax1.set_xticks(range(0, 24))

ax2 = ax1.twinx()
ax2.plot(hourly.index, hourly["fraud_rate_pct"], color="#C44E52", marker="o", linewidth=2, label="Fraud rate (%)")
ax2.set_ylabel("Fraud rate (%)", color="#C44E52")
ax1.set_title("Transaction Volume & Fraud Rate by Hour of Day")
fig.tight_layout()
plt.savefig(f"{CHART_DIR}/03_fraud_rate_by_hour.png", dpi=150)
plt.close()

# 4. Correlation heatmap of V1-V28 with Class (top correlated features)
corr = df.drop(columns=["Time", "hour_of_day"]).corr()["Class"].drop("Class").sort_values()
top_corr = pd.concat([corr.head(7), corr.tail(7)])

fig, ax = plt.subplots(figsize=(7, 6))
colors = ["#C44E52" if v < 0 else "#4C72B0" for v in top_corr.values]
ax.barh(top_corr.index, top_corr.values, color=colors)
ax.set_title("Features Most Correlated with Fraud (Class)")
ax.set_xlabel("Correlation coefficient")
ax.axvline(0, color="black", linewidth=0.8)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/04_top_correlated_features.png", dpi=150)
plt.close()

# 5. Amount vs Class boxplot (capped for readability)
fig, ax = plt.subplots(figsize=(6, 5))
plot_df = df.copy()
plot_df["Amount_capped"] = plot_df["Amount"].clip(upper=500)
sns.boxplot(data=plot_df, x="Class", y="Amount_capped", hue="Class",
            palette={0: "#4C72B0", 1: "#C44E52"}, legend=False, ax=ax)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Legitimate", "Fraud"])
ax.set_ylabel("Transaction Amount (capped at 500)")
ax.set_title("Transaction Amount Spread: Fraud vs Legitimate")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/05_amount_boxplot.png", dpi=150)
plt.close()

print("Saved 5 charts to", CHART_DIR)
print("\nTop correlated features with fraud:")
print(top_corr)
