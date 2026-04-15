import pandas as pd
import numpy as np
import os

def generate_data():
    np.random.seed(42)

    os.makedirs("data", exist_ok=True)

    dates = pd.date_range(start="2024-01-01", periods=300)

    categories = ["Food", "Travel", "Rent", "Shopping", "Bills", "Entertainment"]
    payment_modes = ["Cash", "UPI", "Card"]

    data = {
        "Date": np.random.choice(dates, 300),
        "Category": np.random.choice(categories, 300),
        "Amount": np.random.randint(100, 5000, 300),
        "Payment_Mode": np.random.choice(payment_modes, 300),
        "Type": np.random.choice(["Expense", "Income"], 300, p=[0.8, 0.2])
    }

    df = pd.DataFrame(data)
    df.to_csv("data/expenses.csv", index=False)

    return df