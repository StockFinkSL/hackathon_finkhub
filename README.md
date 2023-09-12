# Financial-Transaction-Tracker

This repository hosts a Jupyter notebook designed for tracking and managing stock transactions. Utilizing the `yfinance` library, it fetches real-time stock prices from Yahoo Finance, initializes transaction datasets, and provides functionalities to add, view, and update transactions.

## Features

- **Initialize Transaction Dataset:** Automatically creates an empty CSV file (`transactions.csv`) if not present, to store transaction details.
- **Real-time Stock Prices:** Fetches the current closing price of stocks using Yahoo Finance's API.
- **Add Transactions:** Easily add new stock transactions with details like user ID, ticker symbol, stop loss, and take profit values.
- **View All Transactions:** A dedicated function to display all transactions stored in the CSV.
- **Update Transactions:** The notebook checks active transactions and updates their status based on current stock prices, stop loss, and take profit values.

## How to Use

1. Clone the repository.
2. Open the Jupyter notebook.
3. Execute the cells sequentially to utilize the provided functionalities.

## Dependencies

- `pandas`
- `numpy`
- `os`
- `yfinance`

## Contribution

Feel free to fork this repository and contribute. Pull requests are welcome!
