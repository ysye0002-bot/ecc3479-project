
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

All data is sourced from the Australian Bureau of Statistics (ABS) 2021 Census.

Required files (to be placed in data/raw/):

2021Census_G02_VIC_SA2.csv → Median rent and household size
2021Census_G15_VIC_SA2.csv → University attendance
2021Census_G09F_VIC_SA2.csv → Country of birth (non-citizens proxy)
2021Census_G36_VIC_SA2.csv → Dwelling structure

Additional file included in this repository:

manual_rent.csv → Precompiled median rent values (used due to extraction issues from ABS tables)

Because suburb-level international student data is unavailable directly, the proxy is defined as:

International Student Proxy = (University Student Share) × (Non-Citizen Share)

This proxy captures suburbs with both high tertiary attendance and larger overseas-born non-citizen populations.

## Dwelling size
Source: * `2021Census_G36_VIC_SA2.csv` — Dwelling structure by suburb (ABS 2021)

## Methodology

Suburbs are grouped into:

High international student concentration
Low international student concentration

Basic difference-in-means and OLS regression:

Price_i = β₀ + β₁ HighStudent_i + ε_i

Expanded Econometric Model Sequence:

The file (04_analysis.py) estimates five progressively richer models:

Model 1 (M1): Baseline

Tests the raw bivariate association between the proxy and rent.

Model 2 (M2): Component Decomposition

Separately estimates:

University attendance share
Overseas-born non-citizen share

Model 3 (M3): Preferred Specification

Adds location controls through Melbourne ring dummies:

Inner ring
Middle ring
Outer ring

This controls for CBD proximity and major location bias.

Model 4 (M4): Non-Linearity Test

Adds a quadratic proxy term to test whether effects vary at different concentrations.

Model 5 (M5): Interaction / Heterogeneity

Tests whether proxy effects differ across suburb rings.

Interpretation of Model Progression
M1 (R² = 0.51): Proxy alone explains substantial rent variation
M3 (R² = 0.52): Ring dummies add little explanatory power
Interpretation: The proxy already captures much of Melbourne’s CBD gradient because high-student suburbs are disproportionately inner-city
M4 (R² = 0.64): Significant improvement suggests non-linear effects
Conclusion: Student concentration influences rent, but effects are not purely linear and may intensify or diminish depending on suburb type


---

# How to Reproduce the Full Pipeline

## 1. Set up environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Add raw data

Download the required ABS Census files and place them in:

data/raw/

Ensure filenames match exactly.

## 2. Run the pipeline
python code/01_load_data.py
python code/02_clean_data.py
python code/03_merge_data.py
python code/04_analysis.py

## 3. Outputs

After running:

Clean dataset:
data/clean/merged_dataset.csv
Regression outputs:
outputs/regression_results.csv
outputs/model_comparisons.csv
Figures:
outputs/figures/
outputs/regression_diagnostics.png


## Optional Analysis Files

* These are supplementary and not required for core replication:

EDA_analysis_expanded.ipynb → Exploratory data analysis
Primary_Econometrics_analysis.ipynb → Extended regression analysis
04_analysis.py → Preferred streamlined reproducible model sequence


## Key Findings
* The international student proxy is positively associated with rental prices in baseline models
* Much of this relationship overlaps with inner-city location effects
* Location controls only marginally improve explanatory power
* Non-linear modelling substantially improves fit
* Some traditionally high-student suburbs do not uniformly exhibit the highest rents
* The relationship between student populations and rent is more complex than simple supply-demand assumptions suggest

  
## Assumptions & Limitations
* International student presence is approximated using a proxy
* Proxy validity depends on overlap between university attendance and non-citizen populations
* Suburb-level matching may introduce classification noise
* Census data is cross-sectional (2021 only)
* Omitted variables remain possible (income, amenities, housing stock quality)

Software Used:

Python 3.x
pandas
numpy
matplotlib
seaborn
statsmodels
Summary

This project moves beyond simple suburb comparisons by implementing a structured econometric sequence that:

Measures baseline rent differences
Tests proxy validity
Controls for geographic confounding
Evaluates non-linear effects
Assesses structural heterogeneity

Overall, Melbourne rental prices appear related to international student concentration, but this relationship is strongly intertwined with broader urban geography and is unlikely to be purely causal.

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

## Reproducing the Analysis

1. Place all raw CSVs into `data/`
2. Run `EDA_analysis_expanded.ipynb` top to bottom
3. Run `Primary_Econometrics_analysis.ipynb` top to bottom — this writes `data/clean/merged_dataset.csv` and all outputs automatically

# ## Reproducing the Robustness workbook

### Run order

1. `code/data_cleaning.ipynb` — reads raw ABS data, outputs `data/clean/cleaned_abs_suburbs_expanded.csv`
2. `code/primary_analysis.ipynb` — reads clean data, outputs primary results
3. `code/robustness_checks.ipynb` — reads clean data, outputs robustness table and figures to `outputs/`

### Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

### Key outputs

- `outputs/robustness_table.csv` — full robustness table
- `outputs/figures/robustness_forest_plot.png` — forest plot
- `outputs/figures/influence_diagnostics.png` — Cook's D and DFBETA
- `outputs/figures/jackknife_plot.png` — jackknife stability plot
>>>>>>> a861645 (Update robustness notebook, output diagnostics, and README)
