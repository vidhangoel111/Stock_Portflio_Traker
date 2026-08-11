import csv
import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = "portfolio.csv"


def create_file():
    """Create the CSV file with headers if it does not exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Ticker", "Quantity", "Purchase Price"])


def add_stock():
    """Add a stock holding to the portfolio."""
    ticker = input("Enter stock symbol (e.g. AAPL): ").strip().upper()

    try:
        quantity = int(input("Enter quantity: "))
        purchase_price = float(input("Enter purchase price per share: "))

        if quantity <= 0 or purchase_price <= 0:
            print("Quantity and price must be greater than 0.")
            return

        # Check that the ticker is valid.
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")

        if history.empty:
            print("Could not find this stock symbol.")
            return

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([ticker, quantity, purchase_price])

        print(f"{ticker} added successfully.")

    except ValueError:
        print("Please enter valid numeric values.")


def load_portfolio():
    """Read the CSV file and return a Pandas DataFrame."""
    try:
        df = pd.read_csv(FILE_NAME)

        if df.empty:
            print("Portfolio is empty.")
            return None

        return df

    except FileNotFoundError:
        print("Portfolio file not found.")
        return None


def show_portfolio():
    """Display portfolio holdings with current prices and values."""
    df = load_portfolio()

    if df is None:
        return

    current_prices = []
    current_values = []

    print("\nFetching current prices...\n")

    for ticker in df["Ticker"]:
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="1d")

            if history.empty:
                price = 0
            else:
                price = float(history["Close"].iloc[-1])

        except Exception:
            price = 0

        current_prices.append(price)

    df["Current Price"] = current_prices
    df["Investment"] = df["Quantity"] * df["Purchase Price"]
    df["Current Value"] = df["Quantity"] * df["Current Price"]

    current_values = df["Current Value"].tolist()

    print(df.to_string(index=False))

    total_investment = df["Investment"].sum()
    total_value = df["Current Value"].sum()
    profit_loss = total_value - total_investment

    print("\n----- Portfolio Summary -----")
    print(f"Total Investment : ${total_investment:.2f}")
    print(f"Current Value    : ${total_value:.2f}")
    print(f"Profit/Loss      : ${profit_loss:.2f}")


def show_chart():
    """Display a pie chart showing portfolio distribution."""
    df = load_portfolio()

    if df is None:
        return

    values = []

    for ticker, quantity in zip(df["Ticker"], df["Quantity"]):
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="1d")

            if history.empty:
                price = 0
            else:
                price = float(history["Close"].iloc[-1])

            values.append(quantity * price)

        except Exception:
            values.append(0)

    valid = [value > 0 for value in values]
    chart_df = df[valid].copy()
    chart_values = [value for value in values if value > 0]

    if not chart_values:
        print("No valid stock data available for chart.")
        return

    plt.figure(figsize=(7, 7))
    plt.pie(
        chart_values,
        labels=chart_df["Ticker"],
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Portfolio Distribution")
    plt.show()


def main():
    """Run the main menu."""
    create_file()

    while True:
        print("\n==============================")
        print("   STOCK PORTFOLIO TRACKER")
        print("==============================")
        print("1. Add Stock")
        print("2. View Portfolio")
        print("3. Show Portfolio Chart")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_stock()
        elif choice == "2":
            show_portfolio()
        elif choice == "3":
            show_chart()
        elif choice == "4":
            print("Thank you for using the Stock Portfolio Tracker.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
