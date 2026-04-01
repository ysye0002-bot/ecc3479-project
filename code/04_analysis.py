import pandas as pd

df = pd.read_csv("data/clean/cleaned_abs_suburbs.csv")

print("RAW CLEANED FILE:")
print(df)

df["median_weekly_rent"] = pd.to_numeric(df["median_weekly_rent"], errors="coerce")
df["intl_student_proxy"] = pd.to_numeric(df["intl_student_proxy"], errors="coerce")

print("\nAFTER NUMERIC CONVERSION:")
print(df[["suburb", "median_weekly_rent", "intl_student_proxy"]])

print("\nMISSING VALUE COUNTS:")
print(df[["median_weekly_rent", "intl_student_proxy"]].isna().sum())

proxy_median = df["intl_student_proxy"].median()

high = df[df["intl_student_proxy"] > proxy_median]
low = df[df["intl_student_proxy"] <= proxy_median]

print("\nMedian proxy value:", proxy_median)
print("Average rent, high proxy suburbs:", high["median_weekly_rent"].mean())
print("Average rent, low proxy suburbs:", low["median_weekly_rent"].mean())

print("\nCORRELATION:")
print(df["median_weekly_rent"].corr(df["intl_student_proxy"]))



import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.scatter(df["intl_student_proxy"], df["median_weekly_rent"])

plt.xlabel("International Student Proxy")
plt.ylabel("Median Weekly Rent ($)")
plt.title("Rent vs International Student Concentration")

# add suburb labels
for i, row in df.iterrows():
    plt.text(
        row["intl_student_proxy"],
        row["median_weekly_rent"],
        row["suburb"],
        fontsize=8
    )

plt.tight_layout()

# SAVE TO OUTPUTS
plt.savefig("outputs/figures/rent_vs_student_proxy.png")

# optional: still display it
plt.show()