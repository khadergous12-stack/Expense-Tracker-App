import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_data(df):
    os.makedirs("outputs/charts", exist_ok=True)

    sns.set(style="whitegrid")

    # -------------------------------
    # 1. Category-wise Bar Chart
    # -------------------------------
    category_sum = df.groupby('Category')['Amount'].sum().sort_values()

    plt.figure(figsize=(10,6))
    sns.barplot(x=category_sum.values, y=category_sum.index)
    plt.title("Total Spending by Category")
    plt.xlabel("Amount (₹)")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig("outputs/charts/bar_chart.png")
    plt.close()

    # -------------------------------
    # 2. Pie Chart
    # -------------------------------
    expense_df = df[df['Type'] == 'Expense']
    pie_data = expense_df.groupby('Category')['Amount'].sum()

    plt.figure(figsize=(8,8))
    plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140)
    plt.title("Expense Distribution")
    plt.tight_layout()
    plt.savefig("outputs/charts/pie_chart.png")
    plt.close()

    # -------------------------------
    # 3. Monthly Trend
    # -------------------------------
    monthly_expense = df[df['Type'] == 'Expense'].groupby('Month_Num')['Amount'].sum()
    monthly_income = df[df['Type'] == 'Income'].groupby('Month_Num')['Amount'].sum()

    plt.figure(figsize=(12,6))
    monthly_expense.plot(marker='o', label="Expense")
    monthly_income.plot(marker='o', label="Income")
    plt.title("Monthly Income vs Expense")
    plt.xlabel("Month")
    plt.ylabel("Amount (₹)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("outputs/charts/line_chart.png")
    plt.close()

    # -------------------------------
    # 4. Weekday Chart
    # -------------------------------
    plt.figure(figsize=(12,6))
    sns.countplot(
        data=df,
        x='Weekday',
        order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    )
    plt.title("Transactions by Weekday")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/charts/weekday_chart.png")
    plt.close()