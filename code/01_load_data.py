import pandas as pd
import glob

files = glob.glob("data/raw/*_gcp_sal.xlsx")

print("FILES FOUND:")
print(files)

for file in files:
    print("\nFILE:", file)
    df = pd.read_excel(file, sheet_name="G01", header=None)
    print(df.head(10))