#STEP 1
import yfinance as yf
import pandas as pd

def get_option_chain_data(instrument_name: str, expiry_date: str, side: str) -> pd.DataFrame:
    """
    Fetches option chain data for a specified instrument, expiry date, and option side (PE or CE).

    Parameters:
    - instrument_name: str : Name of the instrument (e.g., 'NIFTY' or 'BANKNIFTY')
    - expiry_date: str : Expiry date of the options in 'YYYY-MM-DD' format.
    - side: str : Type of option ('PE' for put options or 'CE' for call options)

    Returns:
    - pd.DataFrame : Dataframe with columns - instrument_name, strike_price, side, and bid/ask.
    """
    
    # Map instrument names to Yahoo Finance tickers
    ticker_map = {
        "NIFTY": "^NSEI",  # NIFTY on Yahoo Finance
        "BANKNIFTY": "^NSEBANK"  # BANKNIFTY on Yahoo Finance
    }
    
    # Validate input
    if instrument_name not in ticker_map:
        raise ValueError("Instrument not supported. Choose either 'NIFTY' or 'BANKNIFTY'.")
    if side not in ["PE", "CE"]:
        raise ValueError("Side must be 'PE' for Put or 'CE' for Call.")

    # Get the ticker symbol
    ticker_symbol = ticker_map[instrument_name]
    
    # Fetch option chain
    stock = yf.Ticker(ticker_symbol)
    options_chain = stock.option_chain(expiry_date)
    
    # Select the appropriate option data based on the side
    options_df = options_chain.puts if side == "PE" else options_chain.calls

    # Prepare result DataFrame with highest bid for puts or highest ask for calls
    if side == "PE":
        # Put options - highest bid for each strike price
        result_df = options_df[['strike', 'bid']].rename(columns={'bid': 'highest_bid'})
    else:
        # Call options - highest ask for each strike price
        result_df = options_df[['strike', 'ask']].rename(columns={'ask': 'highest_ask'})

    # Add required columns and format final DataFrame
    result_df['instrument_name'] = instrument_name
    result_df['side'] = side
    result_df = result_df.rename(columns={'strike': 'strike_price'})
    result_df = result_df[['instrument_name', 'strike_price', 'side', 'highest_bid' if side == "PE" else 'highest_ask']]
    
    return result_df
#STEP 2
import requests

# Placeholder: Lot sizes for NIFTY and BANKNIFTY
LOT_SIZES = {
    "NIFTY": 50,
    "BANKNIFTY": 25
}

def get_margin_requirement(instrument_name: str, strike_price: float, side: str) -> float:
    """
    Placeholder function to simulate margin requirement API call.

    Parameters:
    - instrument_name: str : Name of the instrument
    - strike_price: float : Strike price of the option
    - side: str : Option type ("PE" or "CE")

    Returns:
    - float : Calculated margin requirement for the option
    """
    # Simulated margin requirement (you should replace this with actual API logic)
    # Example URL: "https://api.example.com/margin"
    response = 10000  # Placeholder response for margin requirement
    return response

def calculate_margin_and_premium(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates margin required and premium earned for each option in the DataFrame.

    Parameters:
    - data: pd.DataFrame : DataFrame returned by get_option_chain_data.

    Returns:
    - pd.DataFrame : Original DataFrame with additional columns for margin_required and premium_earned.
    """
    data = data.copy()  # Work on a copy to avoid modifying original DataFrame
    
    # Calculate margin required for each row
    data['margin_required'] = data.apply(lambda row: get_margin_requirement(
        row['instrument_name'], row['strike_price'], row['side']
    ), axis=1)

    # Calculate premium earned: price (bid/ask) * lot size
    data['premium_earned'] = data.apply(lambda row: 
        row['highest_bid' if row['side'] == 'PE' else 'highest_ask'] * LOT_SIZES[row['instrument_name']],
        axis=1
    )
    return data





