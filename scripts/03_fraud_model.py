"""
Baseline fraud detection model.
Handles severe class imbalance correctly (accuracy is meaningless here -
use precision/recall/F1/ROC-AUC/PR-AUC instead).
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score,
    roc_curve, precision_recall_curve, average_precision_score
)

CHART_DIR = "/home/claude/creditcard_project/outputs/charts"
REPORT_PATH = "/home/claude/creditcard_project/outputs/model_report.md"

df = pd.read_csv("/home/claude/creditcard_project/data/creditcard.csv")

X = df.drop(columns=["Class"])
y = df["Class"]

# Scale Time and Amount (V1-V28 are already PCA-scaled)
scaler = StandardScaler()
X[["Time", "Amount"]] = scaler.fit_transform(X[["Time", "Amount"]])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

report_lines = ["# Fraud Detection Model Report\n"]
report_lines.append(f"Train size: {len(X_train):,} | Test size: {len(X_test):,}")
report_lines.append(f"Fraud in train: {y_train.sum()} | Fraud in test: {y_test.sum()}\n")

models = {
    "Logistic Regression (class_weight=balanced)": LogisticRegression(
        max_iter=1000, class_weight="balanced", random_state=42
    ),
    "Random Forest (class_weight=balanced)": RandomForestClassifier(
        n_estimators=200, class_weight="balanced", max_depth=12,
        random_state=42, n_jobs=-1
    ),
}

results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    roc_auc = roc_auc_score(y_test, y_proba)
    pr_auc = average_precision_score(y_test, y_proba)
    cm = confusion_matrix(y_test, y_pred)
    report_txt = classification_report(y_test, y_pred, target_names=["Legit", "Fraud"])

    results[name] = {"y_proba": y_proba, "roc_auc": roc_auc, "pr_auc": pr_auc}

    print(f"\n===== {name} =====")
    print(f"ROC-AUC: {roc_auc:.4f} | PR-AUC: {pr_auc:.4f}")
    print("Confusion matrix (rows=actual, cols=predicted):")
    print(cm)
    print(report_txt)

    report_lines.append(f"\n## {name}\n")
    report_lines.append(f"- ROC-AUC: **{roc_auc:.4f}**")
    report_lines.append(f"- PR-AUC (average precision): **{pr_auc:.4f}**\n")
    report_lines.append("Confusion matrix (rows = actual, cols = predicted):\n")
    report_lines.append(f"```\n{cm}\n```\n")
    report_lines.append(f"```\n{report_txt}\n```\n")

# ROC curve comparison
fig, ax = plt.subplots(figsize=(6, 6))
for name, res in results.items():
    fpr, tpr, _ = roc_curve(y_test, res["y_proba"])
    ax.plot(fpr, tpr, label=f"{name.split(' (')[0]} (AUC={res['roc_auc']:.3f})")
ax.plot([0, 1], [0, 1], "k--", linewidth=0.8)
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.set_title("ROC Curve — Fraud Detection Models")
ax.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/06_roc_curve.png", dpi=150)
plt.close()

# Precision-Recall curve comparison (more informative than ROC for rare-class problems)
fig, ax = plt.subplots(figsize=(6, 6))
for name, res in results.items():
    precision, recall, _ = precision_recall_curve(y_test, res["y_proba"])
    ax.plot(recall, precision, label=f"{name.split(' (')[0]} (AP={res['pr_auc']:.3f})")
ax.set_xlabel("Recall")
ax.set_ylabel("Precision")
ax.set_title("Precision-Recall Curve — Fraud Detection Models")
ax.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/07_precision_recall_curve.png", dpi=150)
plt.close()

with open(REPORT_PATH, "w") as f:
    f.write("\n".join(report_lines))

print(f"\nSaved model report to {REPORT_PATH}")
print("Saved ROC and PR curve charts to", CHART_DIR)
