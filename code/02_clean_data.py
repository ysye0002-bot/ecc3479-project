import pandas as pd
import glob
import os


def get_value_exact(df, label):
    first_col = df[0].astype(str).str.strip()
    match = df[first_col == label]

    if match.empty:
        return None

    row = match.iloc[0]
    for value in reversed(row.tolist()):
        num = pd.to_numeric(value, errors="coerce")
        if pd.notna(num):
            return num

    return None


def clean_suburb_name(filepath):
    name = os.path.basename(filepath).replace("_gcp_sal.xlsx", "")
    return name.replace("_", " ").title()


def extract_proxy_metrics(filepath):
    suburb = clean_suburb_name(filepath)

    g01 = pd.read_excel(filepath, sheet_name="G01", header=None)
    g15 = pd.read_excel(filepath, sheet_name="G15", header=None)

    total_persons = get_value_exact(g01, "Total persons")
    australian_citizens = get_value_exact(g01, "Australian citizen")
    university_count = get_value_exact(g15, "Total University or higher education")

    total_persons = pd.to_numeric(total_persons, errors="coerce")
    australian_citizens = pd.to_numeric(australian_citizens, errors="coerce")
    university_count = pd.to_numeric(university_count, errors="coerce")

    non_citizens = total_persons - australian_citizens
    student_share = university_count / total_persons
    non_citizen_share = non_citizens / total_persons
    intl_student_proxy = student_share * non_citizen_share

    return {
        "suburb": suburb,
        "total_persons": total_persons,
        "australian_citizens": australian_citizens,
        "non_citizens": non_citizens,
        "university_count": university_count,
        "student_share": student_share,
        "non_citizen_share": non_citizen_share,
        "intl_student_proxy": intl_student_proxy,
    }


files = [
    f for f in glob.glob("data/raw/*_gcp_sal.xlsx")
    if "vic_gcp_sal.xlsx" not in f.lower()
]

proxy_rows = []
for file in files:
    try:
        proxy_rows.append(extract_proxy_metrics(file))
    except Exception as e:
        print(f"Error processing {file}: {e}")

proxy_df = pd.DataFrame(proxy_rows)

rent_df = pd.read_csv("data/raw/manual_rent.csv")

# standardise suburb names
proxy_df["suburb"] = proxy_df["suburb"].str.strip()
rent_df["suburb"] = rent_df["suburb"].str.strip()

merged = pd.merge(proxy_df, rent_df, on="suburb", how="left")

print("\nFINAL CLEANED DATA:")
print(merged[["suburb", "median_weekly_rent", "intl_student_proxy"]])

merged.to_csv("data/clean/cleaned_abs_suburbs.csv", index=False)
print("\nSaved to data/clean/cleaned_abs_suburbs.csv")