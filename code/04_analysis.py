"""
04_analysis.py
--------------
Runs the full econometric analysis on data/clean/cleaned_abs_suburbs_expanded.csv.

Produces:
    - Regression table (5 OLS models, HC3 robust SEs)
    - Scatterplot: rent vs student proxy
    - Log-log scatterplot with trend line
    - Residual diagnostics for Model 3

Outputs saved to outputs/figures/.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs("outputs/figures", exist_ok=True)

print("=" * 60)
print("04_analysis.py — Econometric analysis")
print("=" * 60)

# ===== Load merged data =====
df = pd.read_csv("data/clean/cleaned_abs_suburbs_expanded.csv")

# ===== Variable construction =====
# Log transforms
df = df[df['intl_student_proxy'] > 0].copy()
df['log_rent']  = np.log(df['median_weekly_rent'])
df['log_proxy'] = np.log(df['intl_student_proxy'])
df['log_uni']   = np.log(df['uni_share'].clip(lower=1e-6))
df['log_os']    = np.log(df['overseas_share'].clip(lower=1e-6))
df['proxy_sq']  = df['log_proxy'] ** 2

# Location ring dummies from SA4 (first 3 digits of SA2 code)
df['sa4'] = df['sa2_code_2021'].astype(str).str[:3].astype(int)
inner_sa4  = [201, 202, 203]
middle_sa4 = [204, 205]
df['D_inner']  = df['sa4'].isin(inner_sa4).astype(int)
df['D_middle'] = df['sa4'].isin(middle_sa4).astype(int)
df['ring'] = df['sa4'].map(
    {**{k:'Inner'  for k in inner_sa4},
     **{k:'Middle' for k in middle_sa4},
     **{k:'Outer'  for k in [206,207,208,209]}}
).fillna('Outer')

# High overseas dummy for interaction (split at median)
med_os = df['overseas_share'].median()
df['D_high_os']      = (df['overseas_share'] > med_os).astype(int)
df['proxy_x_highos'] = df['log_proxy'] * df['D_high_os']

df_log = df.dropna(subset=["log_rent", "log_proxy"]).reset_index(drop=True)
print(f"Sample (linear): n = {len(df)}")
print(f"Sample (log):    n = {len(df_log)}\n")

# ===== OLS with HC3 robust standard errors =====
def ols_hc3(y, X, names):
    from scipy import stats
    n, k = X.shape
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ b
    h = np.einsum("ij,jk,ik->i", X, np.linalg.inv(X.T @ X), X)
    e2 = (resid / (1 - h)) ** 2
    meat  = (X * e2[:, None]).T @ X
    bread = np.linalg.inv(X.T @ X)
    V     = bread @ meat @ bread
    se    = np.sqrt(np.diag(V))
    tstat = b / se
    pval  = 2 * (1 - stats.t.cdf(np.abs(tstat), df=n - k))
    ss_res = resid @ resid
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2     = 1 - ss_res / ss_tot
    r2_adj = 1 - (1 - r2) * (n - 1) / (n - k)
    return dict(names=names, coef=b, se=se, pval=pval,
                r2=r2, r2_adj=r2_adj, n=n)

y     = df_log["log_rent"].values
ones  = np.ones(len(df_log))

# M1: proxy only
m1 = ols_hc3(y,
    np.column_stack([df_log["log_proxy"], ones]),
    ["log_proxy", "Intercept"])

# M2: components only
m2 = ols_hc3(y,
    np.column_stack([df_log["log_uni"], df_log["log_os"], ones]),
    ["log_uni", "log_os", "Intercept"])

# M3: proxy + rings [preferred]
m3 = ols_hc3(y,
    np.column_stack([df_log["log_proxy"], df_log["D_inner"],
                     df_log["D_middle"], ones]),
    ["log_proxy", "D_inner", "D_middle", "Intercept"])

# M4: proxy + rings + quadratic
m4 = ols_hc3(y,
    np.column_stack([df_log["log_proxy"], df_log["proxy_sq"],
                     df_log["D_inner"], df_log["D_middle"], ones]),
    ["log_proxy", "proxy_sq", "D_inner", "D_middle", "Intercept"])

# M5: proxy + rings + interaction
m5 = ols_hc3(y,
    np.column_stack([df_log["log_proxy"], df_log["D_high_os"],
                     df_log["proxy_x_highos"],
                     df_log["D_inner"], df_log["D_middle"], ones]),
    ["log_proxy", "D_high_os", "proxy_x_highos",
     "D_inner", "D_middle", "Intercept"])

# ===== Regression table =====
def stars(p):
    if p < 0.01: return "***"
    if p < 0.05: return "**"
    if p < 0.10: return "*"
    return ""

MODELS = [m1, m2, m3, m4, m5]
LABELS = ["(1) Proxy\nonly", "(2) Components\nonly",
          "(3) Proxy+Rings\n[KEY]", "(4) +Quadratic", "(5) +Interaction"]
VARNAMES = [
    ("log_proxy",       "ln(Proxy)"),
    ("proxy_sq",        "[ln(Proxy)]²"),
    ("D_high_os",       "D: High overseas"),
    ("proxy_x_highos",  "ln(Proxy) × D_high_os"),
    ("log_uni",         "ln(Uni share)"),
    ("log_os",          "ln(Overseas share)"),
    ("D_inner",         "D: Inner ring"),
    ("D_middle",        "D: Middle ring"),
    ("Intercept",       "Intercept"),
]

NW = 26; CW = 18
div = "-" * (NW + CW * len(MODELS))
print(div)
print("REGRESSION TABLE — Dependent variable: ln(Median Weekly Rent)")
print("HC3 robust standard errors in parentheses")
print("Sample: Greater Melbourne SA2 suburbs, ABS Census 2021")
print(div)
print(f'{"":^{NW}}' + "".join(f"{l:^{CW}}" for l in LABELS))
print(div)

for var, label in VARNAMES:
    row_b = f"{label:<{NW}}"
    row_s = f'{"":^{NW}}'
    for m in MODELS:
        if var in m["names"]:
            idx = m["names"].index(var)
            b  = m["coef"][idx]
            se = m["se"][idx]
            p  = m["pval"][idx]
            row_b += f"{b:+.4f}{stars(p):<3}".center(CW)
            row_s += f"({se:.4f})".center(CW)
        else:
            row_b += "—".center(CW)
            row_s += "".center(CW)
    print(row_b)
    print(row_s)

print(div)
print(f'{"N":<{NW}}' + "".join(str(m["n"]).center(CW) for m in MODELS))
print(f'{"R²":<{NW}}' + "".join(f'{m["r2"]:.4f}'.center(CW) for m in MODELS))
print(f'{"Adj. R²":<{NW}}' + "".join(f'{m["r2_adj"]:.4f}'.center(CW) for m in MODELS))
print(div)
print("* p<0.10  ** p<0.05  *** p<0.01")
print("Baseline ring: Outer Melbourne (SA4 209–217).")
print("D_high_os = 1 if overseas_share > median across suburbs.\n")

# ===== Figure 1: Scatterplot (levels) =====
fig, ax = plt.subplots(figsize=(10, 7))
ax.scatter(df["intl_student_proxy"], df["median_weekly_rent"], alpha=0.4, s=15)
m_lin, b_lin = np.polyfit(df["intl_student_proxy"], df["median_weekly_rent"], 1)
x_line = np.linspace(df["intl_student_proxy"].min(), df["intl_student_proxy"].max(), 100)
ax.plot(x_line, m_lin * x_line + b_lin, color="red", linewidth=1.5,
        linestyle="--", label=f"Trend (slope={m_lin:.1f})")
ax.legend()
ax.set_xlabel("International Student Proxy")
ax.set_ylabel("Median Weekly Rent (AUD)")
ax.set_title(f"Rent vs International Student Concentration (n={len(df)})")
plt.tight_layout()
plt.savefig("outputs/figures/rent_vs_student_proxy.png", dpi=300, bbox_inches="tight")
# plt.show()
print("Saved outputs/figures/rent_vs_student_proxy.png")

# ===== Figure 2: Log-log scatterplot =====
fig, ax = plt.subplots(figsize=(9, 6))
ax.scatter(df_log["log_proxy"], df_log["log_rent"], alpha=0.3, s=15)
m2_fit, b2_fit = np.polyfit(df_log["log_proxy"], df_log["log_rent"], 1)
x2 = np.linspace(df_log["log_proxy"].min(), df_log["log_proxy"].max(), 100)
ax.plot(x2, m2_fit * x2 + b2_fit, color="red", linewidth=1.5,
        linestyle="--", label=f"Trend (slope={m2_fit:.3f})")
ax.legend()
corr_log = df_log["log_proxy"].corr(df_log["log_rent"])
ax.set_xlabel("ln(International Student Proxy)")
ax.set_ylabel("ln(Median Weekly Rent)")
ax.set_title(f"Log-Log: Rent vs Student Proxy  (r={corr_log:.3f}, n={len(df_log)})")
plt.tight_layout()
plt.savefig("outputs/figures/rent_vs_proxy_loglog.png", dpi=300, bbox_inches="tight")
# plt.show()
print("Saved outputs/figures/rent_vs_proxy_loglog.png")

# ===== Figure 3: Residual plot (Model 3) =====
# Recompute fitted values and residuals for M3
X3 = np.column_stack([df_log["log_proxy"], df_log["D_inner"],
                      df_log["D_middle"], np.ones(len(df_log))])
fitted_m3 = X3 @ m3["coef"]
resid_m3  = df_log["log_rent"].values - fitted_m3

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(fitted_m3, resid_m3, alpha=0.4, s=15)
ax.axhline(0, color="red", linewidth=1, linestyle="--")
ax.set_xlabel("Fitted values — ln(Rent)")
ax.set_ylabel("Residuals")
ax.set_title("Model 3: Residuals vs Fitted")
plt.tight_layout()
plt.savefig("outputs/figures/residuals_m3.png", dpi=300, bbox_inches="tight")
# plt.show()
print("Saved outputs/figures/residuals_m3.png")

print("\n" + "=" * 60)
print("Analysis complete.")
