# Melbourne Property Prices & Student Populations

## Research Question

How do rental prices differ across Melbourne suburbs with higher concentrations of international students compared with suburbs with lower concentrations?

---

## Repository Structure

* `data/raw/` → Raw datasets (original, unmodified)
* `data/clean/` → Cleaned and merged datasets used for analysis
* `code/` → Python scripts for data processing and analysis
* `outputs/` → Generated figures and tables
* `requirements.txt` → Required Python packages

---

## Data Sources

### 1. Property Price Data

* Source: ABS 2021 Census
* Variable: Median weekly rent
* Geography: Suburb (SAL)

### 2. Student Population Data

* Source: ABS 2021 Census
* Variables extracted:

  * Share attending university
  * Share of non-citizens

### International Student Proxy

[
\text{International Student Proxy} = \text{University Student Share} \times \text{Non-Citizen Share}
]

Due to the absence of direct suburb-level data on international students, this study constructs a proxy variable by interacting the proportion of university students with the proportion of non-citizens.

---

## How to Run the Project

### Step 1: Set up environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Step 2: Add raw data

Manually download datasets and place them into:

```
data/raw/
```

* ABS General Community Profile (GCP) Excel files for selected Melbourne suburbs were downloaded from the ABS 2021 Census website
* Files are loaded using `pandas.read_excel()` in `code/01_load_data.py`

Example:

```python
df = pd.read_excel("data/raw/caulfield_gcp_sal.xlsx", header=None)
```

* All raw files remain unmodified in `data/raw/`

* Median rent values were manually transcribed into:

```
data/raw/manual_rent.csv
```

because automated extraction from Excel was unreliable.

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
* Figures: `outputs/figures/`

---

## Methodology

* Treatment variable: International student proxy
* Outcome variable: Median weekly rent

Suburbs are split into:

* High international student concentration
* Low international student concentration

Conceptually:

[
Price_i = \beta_0 + \beta_1 \cdot HighStudent_i + \epsilon_i
]

---

## Key Findings

* There is **no strong positive relationship** between international student concentration and rental prices
* Suburbs like Clayton and Carlton have high student proxy values but do not have significantly higher rents
* Some lower-proxy suburbs (e.g., Doncaster, Williamstown) have comparable rent levels
* correlation is negative (-0.2)

This suggests that international student concentration alone is not a major determinant of rental prices in this sample.

---

## Assumptions & Notes

* Proxy assumes international students are:

  * more likely to attend university
  * more likely to be non-citizens

* Suburbs are matched across datasets using suburb names

* Analysis is based on 2021 Census data

---

## Software Used

* Python 3.x
* pandas
* numpy
* matplotlib
* seaborn
