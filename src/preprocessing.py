import pandas as pd
import os

def clean_data(df):
    os.makedirs("data", exist_ok=True)

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df = df.dropna()

    # Convert data types
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = pd.to_numeric(df['Amount'])

    # Standardize text
    df['Category'] = df['Category'].str.strip().str.title()
    df['Type'] = df['Type'].str.strip().str.title()

    # Feature Engineering
    df['Month'] = df['Date'].dt.month_name()
    df['Month_Num'] = df['Date'].dt.month
    df['Weekday'] = df['Date'].dt.day_name()

    # Save cleaned data
    df.to_csv("data/cleaned_expenses.csv", index=False)

    return df