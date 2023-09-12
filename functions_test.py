import pandas as pd
import numpy as np
import os
import yfinance as yf


# +
# Define the filename for the CSV file

def create_csv():
    filename = 'transactions.csv'

    # Check if the specified CSV file already exists in the current directory
    if not os.path.exists(filename):

        # List of columns to be included in the empty DataFrame.
        # These columns represent various attributes related to financial transactions.
        columns = [
            'user_id',           # Unique identifier for the user
            'operation_id',      # Unique identifier for the operation/transaction
            'timestamp_entry',   # timestamp the transaction was executed
            'timestamp_exit',   # timestamp the transaction was closed
            'ticker',            # Stock or asset symbol
            'operation',         # Type of operation (e.g., buy, sell)
            'current_price',     # Current price of the asset
            'price_purchased',   # Price at which the asset was purchased
            'profitability',     # Profitability of the transaction
            'stop_loss',         # Price level at which to sell to limit a loss
            'take_profit',       # Price level at which to sell to realize a profit
            'status_transaction' # Current status of the transaction (e.g., pending, completed)
        ]

        # Create an empty DataFrame using the specified columns.
        # This will serve as the initial structure for storing transaction data.
        df = pd.DataFrame(columns=columns)

        # Save the empty DataFrame to a CSV file.
        # This creates a new CSV file with the specified structure, ready to store transaction data.
        df.to_csv(filename, index=False)

        # Notify the user that a new CSV file has been created successfully.
        print(f"Empty CSV file '{filename}' with specified columns created and saved successfully!")

    else:
        # If the CSV file already exists, notify the user.
        print(f"CSV file '{filename}' already exists.")
        
    return 



# -

def get_current_price(ticker_symbol):
    """
    Fetch the current closing price of a given stock from Yahoo Finance.
    
    Parameters:
    - ticker_symbol (str): The ticker symbol of the stock for which the price is to be fetched.
    
    Returns:
    - float: The closing price of the stock for the latest trading day.
    """
    
    # Create a Ticker object for the given ticker symbol to fetch its data
    stock = yf.Ticker(ticker_symbol)
    
    # Fetch the historical data for the stock for the latest trading day
    hist = stock.history(period="1d")
    
    # Extract the closing price from the historical data
    closing_price = hist['Close'].iloc[0]
    
    # Return the closing price
    return closing_price


def get_operation_id():
    """
    Read the 'transactions.csv' file and determine the next operation ID based on the number of existing records.
    
    Returns:
    - int: The next operation ID, which is one more than the number of existing records in the CSV file.
    """
    
    # Read the 'transactions.csv' file into a DataFrame
    df = pd.read_csv('transactions.csv')
    
    # Determine the number of existing records (rows) in the DataFrame
    num_records = len(df)
    
    # Return the next operation ID
    return num_records


def get_timestamp():
    import datetime

    current_timestamp = datetime.datetime.now()
    return current_timestamp


def profit_user():
    df = pd.read_csv('transactions.csv')
    
    import datetime

    df['timestamp_entry'] = pd.to_datetime(df['timestamp_entry'])  # Convert this column as well

    # Get the current date
    current_time = datetime.datetime.now()

    # Filter the DataFrame to include only rows where the 'timestamp_entry' is within the last 30 days
    df_last_30_days = df[df['timestamp_entry'] > (current_time - datetime.timedelta(days=30))]

    # Group by 'user_id' and sum the 'profitability' column for each user
    grouped = df_last_30_days.groupby('user_id')['profitability'].prod()

    # Multiply the profitability by user (assuming you want to multiply by user_id)
    #grouped = grouped * grouped.index

    
    grouped.to_csv("ranking_users.csv", index=False)
    
    print(grouped)
    
    return


def view_transactions():
    
    df = pd.read_csv('transactions.csv')
    print(df)
    
    return


def add_new_operation(user_id, ticker, stop_loss, take_profit):
    """
    Add a new operation (transaction) to the 'transactions.csv' file.
    
    Parameters:
    - user_id (int/str): The unique identifier for the user.
    - ticker (str): The ticker symbol of the stock involved in the operation.
    - stop_loss (float): The price level at which to sell the stock to limit a loss.
    - take_profit (float): The price level at which to sell the stock to realize a profit.
    
    Returns:
    - None: The function saves the new operation to the 'transactions.csv' file and does not return any value.
    """
    
    # Initialize an empty list to store the details of the new operation
    row = []
    
    # Append the user ID to the row
    row.append(user_id)
    
    # Generate and append the operation ID to the row
    operation_id = get_operation_id()
    row.append(operation_id)
    
    #timestamp entry
    row.append(get_timestamp())
 
    #timestamp exit
    row.append(np.nan)
    
    
    # Append the ticker symbol to the row
    row.append(ticker)
    
    # Determine the type of operation (long or short) based on the stop loss and take profit values
    # and append it to the row
    if stop_loss < take_profit:
        operation = "long"
    else:
        operation = "short"
    row.append(operation)
    
    # Fetch the current price of the stock and append it to the row
    price = get_current_price(ticker)
    row.append(price)
    
    # The price at which the stock was purchased is assumed to be the current price
    # Append the purchase price to the row
    price_purchased = price
    row.append(price_purchased)
    
    # Initialize the profitability as 0 and append it to the row
    profitability = 0
    row.append(profitability)
    
    # Append the stop loss and take profit values to the row
    row.append(stop_loss)
    row.append(take_profit)
    
    # Initialize the status of the transaction as 1 (e.g., active) and append it to the row
    status_transaction = 1
    row.append(status_transaction)
    
    # Read the existing transactions from the 'transactions.csv' file into a DataFrame
    df = pd.read_csv('transactions.csv')
    
    # Add the new operation (transaction) to the DataFrame
    df.loc[len(df)] = row
    
    # Save the updated DataFrame back to the 'transactions.csv' file
    df.to_csv('transactions.csv', index=False)
    
    # The function does not return any value
    return


# +
def update_dataset():
    
    
    df = pd.read_csv('transactions.csv')
    # getting transactions with status active

    for i in range(len(df)):
        #Active Transaction
        if df.loc[i,"status_transaction"]==1:
            #Long Operations
            if df.loc[i,"operation"]=="long":
                #Get ticker
                ticker = df.loc[i, "ticker"]
                #Get Current price for ticker
                current_price = get_current_price(ticker)
                #Get purchased price 
                purchased_price = df.loc[i, "price_purchased"]
                #Get Profitability
                profitability = round(100*((current_price-purchased_price)/purchased_price),2)
                df.loc[i, "profitability"] = profitability
                #Stop Loss?
                stop_loss = df.loc[i, "stop_loss"]
                # #Take_profit?
                take_profit = df.loc[i, "take_profit"]
                #Update in case
                if current_price<stop_loss:
                    df.loc[i, "status_transaction"] = 0
                    df.loc[i, "timestamp_exit"] = get_timestamp()
                elif current_price>take_profit:
                    df.loc[i, "status_transaction"] = 0
                    df.loc[i, "timestamp_exit"] = get_timestamp()
            elif df.loc[i,"operation"]=="short":
                #Get ticker
                ticker = df.loc[i, "ticker"]
                #Get Current price for ticker
                current_price = get_current_price(ticker)
                #Get purchased price 
                purchased_price = df.loc[i, "price_purchased"]
                #Get Profitability
                profitability = round(100*((purchased_price-current_price)/purchased_price),2)
                df.loc[i, "profitability"] = profitability
                #Stop Loss?
                stop_loss = df.loc[i, "stop_loss"]
                # #Take_profit?
                take_profit = df.loc[i, "take_profit"]
                #Update in case
                if current_price>stop_loss:
                    df.loc[i, "status_transaction"] = 0
                    df.loc[i, "timestamp_exit"] = get_timestamp()
                elif current_price<take_profit:
                    df.loc[i, "status_transaction"] = 0
                    df.loc[i, "timestamp_exit"] = get_timestamp()
    
    
    return
# -








