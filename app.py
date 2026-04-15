import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Expense Tracker", layout="wide")

# -----------------------------
# CLEAN UI
# -----------------------------
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_expenses.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month_Num'] = df['Date'].dt.month
    df['Weekday'] = df['Date'].dt.day_name()
    return df

df = load_data()

# -----------------------------
# TITLE
# -----------------------------
st.title("💰 Expense Tracker Dashboard")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

category_filter = st.sidebar.multiselect(
    "Category",
    df['Category'].unique(),
    default=df['Category'].unique()
)

type_filter = st.sidebar.selectbox(
    "Transaction Type",
    ["All", "Expense", "Income"]
)

filtered_df = df[df['Category'].isin(category_filter)]

if type_filter != "All":
    filtered_df = filtered_df[filtered_df['Type'] == type_filter]

# -----------------------------
# KPI SECTION (UPDATED 🔥)
# -----------------------------
st.markdown("## 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

total_income = filtered_df[filtered_df['Type'] == 'Income']['Amount'].sum()
total_expense = filtered_df[filtered_df['Type'] == 'Expense']['Amount'].sum()
savings = total_income - total_expense

col1.metric("💰 Income", f"₹{total_income:,.0f}")
col2.metric("💸 Expense", f"₹{total_expense:,.0f}")

# 🔥 SMART SAVINGS DISPLAY
if savings < 0:
    col3.metric("💵 Savings", f"₹{savings:,.0f}", delta="Overspending ⚠️")
    st.error("⚠️ You are overspending! Expenses exceed income.")
else:
    col3.metric("💵 Savings", f"₹{savings:,.0f}", delta="Good 👍")
    st.success("✅ Good financial health! You are saving money.")

sns.set_style("whitegrid")

st.markdown("---")

# -----------------------------
# ROW 1 → BAR + PIE (ALIGNED)
# -----------------------------
st.subheader("📊 Spending Analysis")

colA, colB = st.columns(2, gap="large")

FIG_SIZE = (6, 4)

# BAR CHART
with colA:
    category_sum = filtered_df.groupby('Category')['Amount'].sum().sort_values()

    fig1, ax1 = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=category_sum.values, y=category_sum.index, ax=ax1)

    ax1.set_xlabel("Amount (₹)")
    ax1.set_ylabel("Category")

    plt.tight_layout()
    st.pyplot(fig1, use_container_width=True)

# PIE CHART
with colB:
    expense_df = filtered_df[filtered_df['Type'] == 'Expense']
    pie_data = expense_df.groupby('Category')['Amount'].sum()

    fig2, ax2 = plt.subplots(figsize=FIG_SIZE)

    ax2.pie(
        pie_data,
        labels=pie_data.index,
        autopct='%1.1f%%',
        startangle=90
    )

    ax2.axis('equal')

    plt.tight_layout()
    st.pyplot(fig2, use_container_width=True)

st.markdown("---")

# -----------------------------
# ROW 2 → LINE CHART
# -----------------------------
st.subheader("📈 Monthly Income vs Expense")

monthly_expense = filtered_df[filtered_df['Type'] == 'Expense'].groupby('Month_Num')['Amount'].sum()
monthly_income = filtered_df[filtered_df['Type'] == 'Income'].groupby('Month_Num')['Amount'].sum()

fig3, ax3 = plt.subplots(figsize=(10,4))
monthly_expense.plot(marker='o', label='Expense', ax=ax3)
monthly_income.plot(marker='o', label='Income', ax=ax3)

ax3.set_xlabel("Month")
ax3.set_ylabel("Amount (₹)")
ax3.legend()
ax3.grid()

plt.tight_layout()
st.pyplot(fig3)

st.markdown("---")

# -----------------------------
# ROW 3 → WEEKDAY + HEATMAP
# -----------------------------
st.subheader("📅 Weekly & Trend Insights")

colC, colD = st.columns(2, gap="large")

COMMON_SIZE = (6, 4)

# WEEKDAY CHART
with colC:
    st.markdown("#### Transactions by Weekday")

    fig4, ax4 = plt.subplots(figsize=COMMON_SIZE)

    sns.countplot(
        data=filtered_df,
        x='Weekday',
        order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        ax=ax4
    )

    ax4.set_xlabel("Weekday")
    ax4.set_ylabel("Count")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig4, use_container_width=True)
    plt.close(fig4)

# HEATMAP
with colD:
    st.markdown("#### 🔥 Spending Heatmap")

    pivot = filtered_df.pivot_table(
        values="Amount",
        index="Category",
        columns="Month_Num",
        aggfunc="sum",
        fill_value=0
    )

    pivot = pivot.reindex(sorted(pivot.columns), axis=1)

    fig5, ax5 = plt.subplots(figsize=COMMON_SIZE)

    sns.heatmap(
        pivot,
        annot=True,
        fmt=".0f",
        cmap="YlOrRd",
        linewidths=0.5,
        linecolor="gray",
        cbar=False,
        annot_kws={"size": 8},
        ax=ax5
    )

    ax5.set_xlabel("Month")
    ax5.set_ylabel("Category")

    plt.tight_layout()

    st.pyplot(fig5, use_container_width=True)
    plt.close(fig5)

# -----------------------------
# RAW DATA
# -----------------------------
if st.checkbox("📄 Show Data"):
    st.dataframe(filtered_df)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("🚀 Expense Tracker App Dashboard")