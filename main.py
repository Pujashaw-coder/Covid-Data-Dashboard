import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "covid_data.csv")

def ensure_file():
    os.makedirs(DATA_FOLDER, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        pd.DataFrame(columns=["Date", "City", "New_Cases", "Recoveries", "Deaths"]).to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE, parse_dates=["Date"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def add_daily_report():
    date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    date = pd.to_datetime(date_input) if date_input else pd.to_datetime("today")
    city = input("Enter city name: ")
    new_cases = int(input("Enter number of new cases: "))
    recoveries = int(input("Enter number of recoveries: "))
    deaths = int(input("Enter number of deaths: "))

    df = load_data()
    new_entry = pd.DataFrame([[date, city, new_cases, recoveries, deaths]],
                             columns=["Date", "City", "New_Cases", "Recoveries", "Deaths"])
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    print("Data added successfully.")

def show_summary():
    df = load_data()
    if df.empty:
        print("No data available.")
        return

    total = df.groupby("City")[["New_Cases", "Recoveries", "Deaths"]].sum()
    total["Active_Cases"] = total["New_Cases"] - total["Recoveries"] - total["Deaths"]
    print("\n--- City-wise Summary ---")
    print(total.sort_values("Active_Cases", ascending=False))

def plot_trends():
    df = load_data()
    if df.empty:
        print("No data available.")
        return

    city = input("Enter city to plot trends: ")
    city_data = df[df["City"].str.lower() == city.lower()].sort_values("Date")
    if city_data.empty:
        print("No data for this city.")
        return

    plt.plot(city_data["Date"], city_data["New_Cases"], label="New Cases", marker='o')
    plt.plot(city_data["Date"], city_data["Recoveries"], label="Recoveries", marker='o')
    plt.plot(city_data["Date"], city_data["Deaths"], label="Deaths", marker='o')
    plt.title(f"COVID Trends for {city}")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def identify_hotspots():
    df = load_data()
    if df.empty:
        print("No data available.")
        return

    recent = df[df["Date"] >= pd.to_datetime("today") - pd.Timedelta(days=7)]
    grouped = recent.groupby("City")["New_Cases"].sum()
    hotspots = grouped[grouped > 100]
    print("\n--- Hotspot Cities (Last 7 Days > 100 cases) ---")
    print(hotspots.sort_values(ascending=False))

def import_csv():
    path = input("Enter path to CSV file to import: ")
    try:
        new_df = pd.read_csv(path, parse_dates=["Date"])
        df = pd.concat([load_data(), new_df], ignore_index=True)
        save_data(df)
        print("Data imported successfully.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    ensure_file()
    while True:
        print("\nCOVID Data Dashboard")
        print("1. Add Daily Report")
        print("2. Show Summary")
        print("3. Plot Trends")
        print("4. Identify Hotspots")
        print("5. Import Data from CSV")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_daily_report()
        elif choice == "2":
            show_summary()
        elif choice == "3":
            plot_trends()
        elif choice == "4":
            identify_hotspots()
        elif choice == "5":
            import_csv()
        elif choice == "6":
            print("Exiting the dashboard.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
