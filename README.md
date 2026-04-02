# Melbourne Property Prices & Student Populations

## Research Question

How do rental prices differ across Melbourne suburbs with higher concentrations of international students compared with suburbs with lower concentrations?

---

## Repository Structure

* `data/raw/` → Raw datasets (original, unmodified)
* `data/clean/` → Cleaned and merged datasets used for analysis
* `code/` → Python scripts for data processing and analysis
* `output/` → Generated figures and tables
* `requirements.txt` → Required Python packages

---

## Data Sources

1. Property price data: 
ABS data 
* Variable: median weekly rent
* Geography: suburb (SAL)

2. Student population data : 
ABS data
extract 
* % attending university (education variable)
* % non-citizens

International Student Proxy=University Student Share×Non-Citizen Share

Due to the absence of direct suburb-level data on international students, this study constructs a proxy variable by interacting the proportion of university students with the proportion of overseas-born residents using 2021 Census data.


---

## How to Run the Project

### Step 1: Set up environment

```bash
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```

### Step 2: Add raw data

Manually download datasets and place them into:

```
data/raw/
```

Raw ABS General Community Profile Excel files for selected Melbourne suburbs were manually downloaded from the ABS 2021 Census website and stored in data/raw/.

The files are loaded using pandas.read_excel() in code/01_load_data.py.

Example:

df = pd.read_excel("data/raw/caulfield_gcp_sal.xlsx", header=None)

All raw files remain unmodified in the data/raw/ folder.

---

### Step 3: Run scripts in order

```bash
python code/01_load_data.py
python code/02_clean_data.py
python code/03_merge_data.py
python code/04_analysis.py
```

---

## Output

* Clean dataset: `data/clean/merged_dataset.csv`
* Figures: `output/`

---

## Notes / Assumptions

* International Student Proxy=University Student Share×Non-Citizen Share
* Due to the absence of direct suburb-level data on international students, this study constructs a proxy variable by interacting the proportion of university students with the proportion of overseas-born residents using 2021 Census data.

* The treatment variable is the proxy of proportion of international students in each suburb, used to classify suburbs into high and low student population groups. Median rent prices are used as the outcome variable. The analysis is based on 2021 Census data, which provides reliable suburb-level demographic information.

* Median weekly rent values were manually transcribed from the ABS 2021 Census G02 worksheets for each selected suburb and saved in data/raw/manual_rent.csv because the Excel formatting made automated extraction unreliable.

* The scatter plot indicates that there is no strong positive relationship between the concentration of international students and median weekly rent across the selected Melbourne suburbs. While suburbs such as Clayton and Carlton exhibit relatively high international student proxy values, their rental prices are not substantially higher than suburbs with lower proxy values such as Doncaster and Williamstown. This suggests that international student concentration alone may not be a major determinant of rental prices within this sample.






* high_student = 1 if student_share > threshold else 0 
* median_rent= prices (AUD)
* conceptually the question is Pricei​=β0​+β1​⋅HighStudenti​+ϵi​
* Suburbs are matched across datasets using suburb name

---

## Software Used

* Python 3.x
* pandas
* numpy
* matplotlib
* seaborn

---
