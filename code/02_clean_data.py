"""
02_clean_data.py
----------------
Reads the five raw ABS Census CSVs, filters to Greater Melbourne
SA2 suburbs, cleans each table, and saves cleaned versions to
data/clean/.

Greater Melbourne filter: SA2_CODE_2021 starting with 201–217.

Outputs (data/clean/):
    cleaned_G02.csv
    cleaned_G09F.csv
    cleaned_G09H.csv
    cleaned_G15.csv
    cleaned_G36.csv
"""

import pandas as pd
import os

RAW_DIR   = "data/raw"
CLEAN_DIR = "data/clean"
os.makedirs(CLEAN_DIR, exist_ok=True)

FILES = {
    "G02":  "2021Census_G02_VIC_SA2.csv",
    "G09F": "2021Census_G09F_VIC_SA2.csv",
    "G09H": "2021Census_G09H_VIC_SA2.csv",
    "G15":  "2021Census_G15_VIC_SA2.csv",
    "G36":  "2021Census_G36_VIC_SA2.csv",
}

# Greater Melbourne: SA2 codes starting with 201–217
MELB_PREFIXES = [str(i) for i in range(201, 218)]

def filter_melbourne(df):
    return df[df["SA2_CODE_2021"].astype(str).str[:3].isin(MELB_PREFIXES)].copy()

def clean_table(df, table_name):
    print(f"Cleaning {table_name}...")

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates()
    print(f"  Dropped {before - len(df)} duplicate rows")

    # Standardise column names
    df.columns = (df.columns
                  .str.strip()
                  .str.lower()
                  .str.replace(" ", "_")
                  .str.replace("-", "_"))

    # Ensure SA2 code is string
    if "sa2_code_2021" in df.columns:
        df["sa2_code_2021"] = df["sa2_code_2021"].astype(str)

    # Fill missing numeric with column median; categorical with mode
    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            df[col] = df[col].fillna(df[col].median())
        else:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])

    print(f"  Final shape: {df.shape}")
    return df


print("=" * 60)
print("02_clean_data.py — Cleaning ABS Census tables")
print("=" * 60)

for table_name, filename in FILES.items():
    filepath = os.path.join(RAW_DIR, filename)
    if not os.path.exists(filepath):
        print(f"\n[MISSING] {filepath} — skipping {table_name}")
        continue

    df = pd.read_csv(filepath)
    df = filter_melbourne(df)
    df = clean_table(df, table_name)

    out_path = os.path.join(CLEAN_DIR, f"cleaned_{table_name}.csv")
    df.to_csv(out_path, index=False)
    print(f"  Saved → {out_path}\n")

print("=" * 60)
print("Cleaning complete.")