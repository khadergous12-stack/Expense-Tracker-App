def analyze_data(df):
    insights = {}

    category_sum = df.groupby('Category')['Amount'].sum()
    insights['Top Spending Category'] = category_sum.idxmax()

    insights['Average Transaction'] = round(df['Amount'].mean(), 2)

    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()

    insights['Total Income'] = total_income
    insights['Total Expense'] = total_expense
    insights['Savings'] = total_income - total_expense

    return insights