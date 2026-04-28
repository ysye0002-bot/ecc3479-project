# Codebook: Melbourne Suburb Dataset
Main analysis dataset: `data/clean/cleaned_abs_suburbs.csv`

| Variable | Description |
|---|---|
| `suburb` | Melbourne suburb name |
| `total_persons` | Total persons in the suburb from ABS 2021 Census |
| `australian_citizens` | Number of Australian citizens |
| `non_citizens` | Total persons minus Australian citizens |
| `university_count` | Number of people attending university or higher education |
| `median_weekly_rent` | Median weekly rent in (AUD per week) |
| `student_share` | Proportion of residents attending university (`university_count / total_persons`) |
| `non_citizen_share` | Proportion of non-citizens (`non_citizens / total_persons`) |
| `intl_student_proxy` | Proxy for international student concentration (`student_share × non_citizen_share`) |

## Notes

Direct suburb-level international student data was not available, so this project uses `intl_student_proxy` as an approximate measure of international student concentration.
This proxy captures areas with both high student populations and high non-citizen shares, which are more likely to reflect concentrations of international students.

Median weekly rent values were manually transcribed into `data/raw/manual_rent.csv`.