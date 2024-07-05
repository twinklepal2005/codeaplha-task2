import requests
import pandas as pd
from datetime import datetime

class StockPortfolio:
    def __init__(self, api_key):
        self.api_key = api_key
        self.stocks = {}

    def add_stock(self, symbol, shares):
        if symbol in self.stocks:
            self.stocks[symbol]['shares'] += shares
        else:
            self.stocks[symbol] = {'shares': shares, 'prices': []}
        print(f"Added {shares} shares of {symbol}.")

    def remove_stock(self, symbol, shares):
        if symbol in self.stocks:
            if self.stocks[symbol]['shares'] > shares:
                self.stocks[symbol]['shares'] -= shares
                print(f"Removed {shares} shares of {symbol}.")
            elif self.stocks[symbol]['shares'] == shares:
                del self.stocks[symbol]
                print(f"Removed all shares of {symbol}.")
            else:
                print(f"Cannot remove {shares} shares. Only {self.stocks[symbol]['shares']} shares available.")
        else:
            print(f"{symbol} not in portfolio.")

    def get_stock_data(self, symbol):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={self.api_key}'
        response = requests.get(url)
        data = response.json()
        if "Time Series (1min)" in data:
            latest_data = data["Time Series (1min)"]
            latest_time = sorted(latest_data.keys())[-1]
            price = float(latest_data[latest_time]['4. close'])
            open_price = float(latest_data[latest_time]['1. open'])
            high_price = float(latest_data[latest_time]['2. high'])
            low_price = float(latest_data[latest_time]['3. low'])
            volume = int(latest_data[latest_time]['5. volume'])
            return price, open_price, high_price, low_price, volume
        else:
            print(f"Failed to retrieve data for {symbol}.")
            return None, None, None, None, None

    def update_prices(self):
        for symbol in self.stocks:
            price, open_price, high_price, low_price, volume = self.get_stock_data(symbol)
            if price:
                self.stocks[symbol]['prices'].append({
                    'time': datetime.now(),
                    'price': price,
                    'open': open_price,
                    'high': high_price,
                    'low': low_price,
                    'volume': volume
                })

    def display_portfolio(self):
        print("Current Portfolio:")
        for symbol, details in self.stocks.items():
            latest_price = details['prices'][-1]['price'] if details['prices'] else 'N/A'
            print(f"Stock: {symbol}, Shares: {details['shares']}, Latest Price: {latest_price}")

    def display_performance(self):
        print("Portfolio Performance:")
        total_value = 0
        for symbol, details in self.stocks.items():
            if details['prices']:
                initial_price = details['prices'][0]['price']
                latest_price = details['prices'][-1]['price']
                performance = (latest_price - initial_price) / initial_price * 100
                stock_value = latest_price * details['shares']
                total_value += stock_value
                print(f"Stock: {symbol}, Initial Price: {initial_price}, Latest Price: {latest_price}, Performance: {performance:.2f}%, Current Value: {stock_value:.2f}")
            else:
                print(f"Stock: {symbol} has no price data.")
        print(f"Total Portfolio Value: {total_value:.2f}")

    def display_stock_details(self, symbol):
        if symbol in self.stocks and self.stocks[symbol]['prices']:
            print(f"Details for {symbol}:")
            for record in self.stocks[symbol]['prices']:
                print(f"Time: {record['time']}, Price: {record['price']}, Open: {record['open']}, High: {record['high']}, Low: {record['low']}, Volume: {record['volume']}")
        else:
            print(f"No data available for {symbol}.")

def main():
    api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'
    portfolio = StockPortfolio(api_key)

    while True:
        print("\n1. Add Stock")
        print("2. Remove Stock")
        print("3. Update Prices")
        print("4. Display Portfolio")
        print("5. Display Performance")
        print("6. Display Stock Details")
        print("7. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.add_stock(symbol, shares)
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.remove_stock(symbol, shares)
        elif choice == '3':
            portfolio.update_prices()
        elif choice == '4':
            portfolio.display_portfolio()
        elif choice == '5':
            portfolio.display_performance()
        elif choice == '6':
            symbol = input("Enter stock symbol: ").upper()
            portfolio.display_stock_details(symbol)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
