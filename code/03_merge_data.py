import pandas as pd

# Load datasets
abs_df = pd.read_csv("data/clean/cleaned_abs_suburbs.csv")
rent_df = pd.read_csv("data/raw/manual_rent.csv")

# Clean suburb names
abs_df["suburb"] = abs_df["suburb"].str.strip().str.lower()
rent_df["suburb"] = rent_df["suburb"].str.strip().str.lower()

# Merge
merged_df = pd.merge(abs_df, rent_df, on="suburb", how="inner")

# Preview
print("\nMERGED DATA:")
print(merged_df.head())

# Save
merged_df.to_csv("data/clean/merged_dataset.csv", index=False)

print("\nSaved to data/clean/merged_dataset.csv")

