
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Employee Attrition Analytics",
    page_icon="👥",
    layout="wide"
)

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("employee_attrition_cleaned.csv")

# Income band
df["Income_Band"] = pd.cut(
    df["MonthlyIncome"],
    bins=[0, 3000, 6000, 10000, float("inf")],
    labels=["Low", "Medium", "High", "Very High"]
)

# -----------------------------
# Title
# -----------------------------
st.title("👥 Employee Attrition Analytics Dashboard")

st.markdown(
    "Analysis of employee attrition patterns across department, "
    "job role, tenure, compensation and workload."
)

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Dashboard Filters")

departments = st.sidebar.multiselect(
    "Department",
    sorted(df["Department"].unique()),
    default=sorted(df["Department"].unique())
)

roles = st.sidebar.multiselect(
    "Job Role",
    sorted(df["JobRole"].unique()),
    default=sorted(df["JobRole"].unique())
)

overtime = st.sidebar.multiselect(
    "Overtime",
    sorted(df["OverTime"].unique()),
    default=sorted(df["OverTime"].unique())
)

income_bands = st.sidebar.multiselect(
    "Income Band",
    ["Low", "Medium", "High", "Very High"],
    default=["Low", "Medium", "High", "Very High"]
)

# -----------------------------
# Filter data
# -----------------------------
filtered = df[
    (df["Department"].isin(departments)) &
    (df["JobRole"].isin(roles)) &
    (df["OverTime"].isin(overtime)) &
    (df["Income_Band"].isin(income_bands))
].copy()

# -----------------------------
# KPIs
# -----------------------------
total = len(filtered)
left = (filtered["Attrition"] == "Yes").sum()
current = (filtered["Attrition"] == "No").sum()

attrition_rate = (left / total * 100) if total else 0

early = filtered[filtered["YearsAtCompany"] <= 2]

early_rate = (
    (early["Attrition"] == "Yes").sum() / len(early) * 100
    if len(early) else 0
)

avg_income = filtered["MonthlyIncome"].mean() if total else 0

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total Employees", f"{total:,}")
col2.metric("Employees Left", f"{left:,}")
col3.metric("Current Employees", f"{current:,}")
col4.metric("Attrition Rate", f"{attrition_rate:.2f}%")
col5.metric("Early-Tenure Attrition", f"{early_rate:.2f}%")
col6.metric("Avg Monthly Income", f"${avg_income:,.0f}")

st.divider()

# -----------------------------
# Department analysis
# -----------------------------
st.subheader("📊 Attrition by Department")

department = (
    filtered.groupby("Department")
    .agg(
        Employees=("EmployeeNumber", "count"),
        Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
    )
    .reset_index()
)

department["Attrition_Rate"] = (
    department["Employees_Left"] /
    department["Employees"] * 100
)

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    department["Department"],
    department["Attrition_Rate"]
)

ax.set_ylabel("Attrition Rate (%)")
ax.set_xlabel("Department")
ax.set_title("Attrition Rate by Department")

plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# Job role
# -----------------------------
st.subheader("💼 Attrition by Job Role")

role = (
    filtered.groupby("JobRole")
    .agg(
        Employees=("EmployeeNumber", "count"),
        Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
    )
    .reset_index()
)

role["Attrition_Rate"] = (
    role["Employees_Left"] /
    role["Employees"] * 100
)

fig, ax = plt.subplots(figsize=(10, 5))

ax.barh(
    role["JobRole"],
    role["Attrition_Rate"]
)

ax.set_xlabel("Attrition Rate (%)")
ax.set_ylabel("Job Role")
ax.set_title("Attrition Rate by Job Role")

plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# Income band
# -----------------------------
st.subheader("💰 Attrition by Income Band")

income = (
    filtered.groupby("Income_Band", observed=True)
    .agg(
        Employees=("EmployeeNumber", "count"),
        Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
    )
    .reset_index()
)

income["Attrition_Rate"] = (
    income["Employees_Left"] /
    income["Employees"] * 100
)

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    income["Income_Band"].astype(str),
    income["Attrition_Rate"]
)

ax.set_ylabel("Attrition Rate (%)")
ax.set_xlabel("Income Band")
ax.set_title("Attrition Rate by Income Band")

plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# Overtime
# -----------------------------
st.subheader("⏰ Attrition by Overtime")

ot = (
    filtered.groupby("OverTime")
    .agg(
        Employees=("EmployeeNumber", "count"),
        Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
    )
    .reset_index()
)

ot["Attrition_Rate"] = (
    ot["Employees_Left"] /
    ot["Employees"] * 100
)

fig, ax = plt.subplots(figsize=(7, 4))

ax.bar(
    ot["OverTime"],
    ot["Attrition_Rate"]
)

ax.set_ylabel("Attrition Rate (%)")
ax.set_xlabel("Overtime")
ax.set_title("Attrition Rate by Overtime")

plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# Tenure
# -----------------------------
st.subheader("📅 Attrition by Tenure")

filtered["Tenure_Band"] = pd.cut(
    filtered["YearsAtCompany"],
    bins=[-1, 2, 5, 10, float("inf")],
    labels=["0–2 years", "3–5 years", "6–10 years", "10+ years"]
)

tenure = (
    filtered.groupby("Tenure_Band", observed=True)
    .agg(
        Employees=("EmployeeNumber", "count"),
        Employees_Left=("Attrition", lambda x: (x == "Yes").sum())
    )
    .reset_index()
)

tenure["Attrition_Rate"] = (
    tenure["Employees_Left"] /
    tenure["Employees"] * 100
)

fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    tenure["Tenure_Band"].astype(str),
    tenure["Attrition_Rate"]
)

ax.set_ylabel("Attrition Rate (%)")
ax.set_xlabel("Tenure")
ax.set_title("Attrition Rate by Tenure")

plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# Data table
# -----------------------------
st.subheader("📋 Filtered Employee Data")

st.dataframe(
    filtered[
        [
            "EmployeeNumber",
            "Age",
            "Department",
            "JobRole",
            "MonthlyIncome",
            "OverTime",
            "YearsAtCompany",
            "Attrition"
        ]
    ],
    use_container_width=True
)

st.caption(
    "Note: Observed associations do not establish causation."
)
