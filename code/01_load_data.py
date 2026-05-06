"""
01_load_data.py
---------------
Loads the five raw ABS Census 2021 CSV files and prints a basic
inventory (shape, columns, head) so you can confirm the raw data
looks correct before cleaning.

Expected files in data/raw/:
    2021Census_G02_VIC_SA2.csv   — median rent, household size
    2021Census_G09F_VIC_SA2.csv  — country of birth (persons): Australia-born total
    2021Census_G09H_VIC_SA2.csv  — country of birth (persons): grand total
    2021Census_G15_VIC_SA2.csv   — type of educational institution
    2021Census_G36_VIC_SA2.csv   — dwelling structure
"""

import pandas as pd
import os

RAW_DIR = "data/raw"

FILES = {
    "G02":  "2021Census_G02_VIC_SA2.csv",
    "G09F": "2021Census_G09F_VIC_SA2.csv",
    "G09H": "2021Census_G09H_VIC_SA2.csv",
    "G15":  "2021Census_G15_VIC_SA2.csv",
    "G36":  "2021Census_G36_VIC_SA2.csv",
}

print("=" * 60)
print("01_load_data.py — Raw file inventory")
print("=" * 60)

for table, filename in FILES.items():
    filepath = os.path.join(RAW_DIR, filename)
    if not os.path.exists(filepath):
        print(f"\n[MISSING] {filename}")
        continue

    df = pd.read_csv(filepath)
    print(f"\n[{table}] {filename}")
    print(f"  Shape:   {df.shape}")
    print(f"  Columns: {list(df.columns[:6])} ...")
    print(f"  Head:\n{df.head(3)}\n")

print("=" * 60)
print("Load check complete.")