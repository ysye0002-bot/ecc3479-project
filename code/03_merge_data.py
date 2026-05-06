"""
03_merge_data.py
----------------
Merges the five cleaned ABS tables on SA2_CODE_2021 and constructs
the key analysis variables:

    uni_share          = university students / all education attendees  (G15)
    overseas_share     = (total persons - Australia-born) / total persons  (G09F + G09H)
    intl_student_proxy = uni_share * overseas_share
    apt_share          = flats & apartments / total occupied dwellings  (G36)
    avg_hh_size        = average household size  (G02)
    median_weekly_rent = median weekly rent AUD  (G02)

Also constructs ring dummies and the D_high_os interaction dummy used
in the econometric analysis.

Output: data/clean/merged_dataset.csv
"""

import pandas as pd
import numpy as np
import os

CLEAN_DIR = "data/clean"

print("=" * 60)
print("03_merge_data.py — Merging and constructing variables")
print("=" * 60)

# ===== Load cleaned tables =====
g02  = pd.read_csv(os.path.join(CLEAN_DIR, "cleaned_G02.csv"))
g09f = pd.read_csv(os.path.join(CLEAN_DIR, "cleaned_G09F.csv"))
g09h = pd.read_csv(os.path.join(CLEAN_DIR, "cleaned_G09H.csv"))
g15  = pd.read_csv(os.path.join(CLEAN_DIR, "cleaned_G15.csv"))
# g36  = pd.read_csv(os.path.join(CLEAN_DIR, "cleaned_G36.csv"))  # Not available

# ===== Build variables =====

# University share (G15)
g15["uni_share"] = (
    g15["tert_uni_other_high_edu_tot_p"]
    / g15["tot_p"].replace(0, np.nan)
)

# Overseas-born share (G09F + G09H)
# p_australia_tot = Australia-born persons (G09F)
# p_tot_tot       = all persons, all countries (G09H)
g09 = g09f[["sa2_code_2021", "p_australia_tot"]].merge(
    g09h[["sa2_code_2021", "p_tot_tot"]], on="sa2_code_2021", how="inner"
)
g09["overseas_share"] = (
    (g09["p_tot_tot"] - g09["p_australia_tot"])
    / g09["p_tot_tot"].replace(0, np.nan)
)

# Apartment share (G36) - commented out as file not available
# g36["apt_share"] = (
#     g36["opds_flt_apart_tot_dwgs"]
#     / g36["opds_tot_opds_dwellings"].replace(0, np.nan)
# )

# ===== Merge all tables =====
df = (
    g02[["sa2_code_2021", "median_rent_weekly", "average_household_size"]]
    .merge(g15[["sa2_code_2021", "uni_share"]], on="sa2_code_2021", how="inner")
    .merge(g09[["sa2_code_2021", "overseas_share"]], on="sa2_code_2021", how="inner")
    # .merge(g36[["sa2_code_2021", "apt_share"]], on="sa2_code_2021", how="inner")
)

df.rename(columns={
    "median_rent_weekly":      "median_weekly_rent",
    "average_household_size":  "avg_hh_size"
}, inplace=True)

# ===== Derived variables =====
df["intl_student_proxy"] = df["uni_share"] * df["overseas_share"]
df["log_rent"]           = np.log(df["median_weekly_rent"])
df["log_proxy"]          = np.log(df["intl_student_proxy"].replace(0, np.nan))
df["log_uni"]            = np.log(df["uni_share"].replace(0, np.nan))
df["log_os"]             = np.log(df["overseas_share"].replace(0, np.nan))
df["proxy_sq"]           = df["log_proxy"] ** 2

# Location ring dummies (based on SA4: first 3 digits of SA2 code)
sa4 = df["sa2_code_2021"].astype(str).str[:3].astype(int)
df["D_inner"]  = (sa4 == 206).astype(int)   # Inner Melbourne SA4
df["D_middle"] = (sa4.isin([207, 208])).astype(int)  # Middle Melbourne SA4s

# High overseas dummy and interaction
df["D_high_os"]       = (df["overseas_share"] > df["overseas_share"].median()).astype(int)
df["proxy_x_highos"]  = df["log_proxy"] * df["D_high_os"]

# ===== Drop rows with missing key variables =====
key_vars = ["median_weekly_rent", "intl_student_proxy", "log_proxy",
            "avg_hh_size"]  # removed apt_share
before = len(df)
df = df.dropna(subset=key_vars)
df = df[df["median_weekly_rent"] > 0].reset_index(drop=True)
print(f"Dropped {before - len(df)} rows with missing values.")
print(f"Final sample: n = {len(df)}")

# ===== Save =====
out_path = os.path.join(CLEAN_DIR, "merged_dataset.csv")
df.to_csv(out_path, index=False)
print(f"Saved → {out_path}")

print("\nVariable summary:")
print(df[["median_weekly_rent", "intl_student_proxy",
          "avg_hh_size"]].describe().round(3))

print("=" * 60)
print("Merge complete.")
