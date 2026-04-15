from src.data_generator import generate_data
from src.preprocessing import clean_data
from src.analysis import analyze_data
from src.visualization import visualize_data

def main():
    print("\n🚀 Expense Tracker App Started...\n")

    # Step 1: Generate Data
    df = generate_data()
    print("✅ Synthetic Data Generated")

    # Step 2: Clean Data
    df = clean_data(df)
    print("✅ Data Cleaned")

    # Step 3: Analyze Data
    insights = analyze_data(df)
    print("✅ Analysis Completed")

    # Step 4: Visualization
    visualize_data(df)
    print("✅ Visualizations Generated")

    # Step 5: Print Insights
    print("\n📊 FINAL INSIGHTS:")
    for k, v in insights.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()