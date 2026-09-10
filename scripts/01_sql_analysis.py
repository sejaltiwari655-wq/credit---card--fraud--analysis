"""
Run the SQL analysis queries against creditcard.db and print/save results.
"""
import sqlite3
import pandas as pd
import re

pd.set_option("display.width", 120)

DB_PATH = "/home/claude/creditcard_project/creditcard.db"
SQL_PATH = "/home/claude/creditcard_project/sql/fraud_analysis_queries.sql"
OUT_PATH = "/home/claude/creditcard_project/outputs/sql_results.md"

with open(SQL_PATH, "r") as f:
    raw = f.read()

# Split into individual statements, keeping the comment above each as its title
blocks = re.split(r"\n(?=-- \d+\.)", raw)

conn = sqlite3.connect(DB_PATH)

report_lines = ["# SQL Analysis Results\n"]

for block in blocks:
    block = block.strip()
    if not block or not block.startswith("--"):
        continue
    title_match = re.match(r"-- (\d+\..+)", block)
    title = title_match.group(1) if title_match else "Query"
    # extract the SQL (drop comment lines starting with --)
    sql_lines = [l for l in block.split("\n") if not l.strip().startswith("--")]
    query = "\n".join(sql_lines).strip()
    if not query:
        continue
    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"Skipping ({title}): {e}")
        continue
    print(f"\n=== {title} ===")
    print(df.to_string(index=False))
    report_lines.append(f"\n## {title}\n")
    report_lines.append(df.to_markdown(index=False))
    report_lines.append("\n")

conn.close()

with open(OUT_PATH, "w") as f:
    f.write("\n".join(report_lines))

print(f"\nSaved full report to {OUT_PATH}")
