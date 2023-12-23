from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import requests
from datetime import datetime
import config
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import alpaca_trade_api as tradeapi
import pandas as pd
from TA import *
from strategy import my_strat

def test():
    trading_client = StockHistoricalDataClient(config.API_KEY, config.SECRET)

    request_params = StockBarsRequest(
        symbol_or_symbols=["SPY"],
        timeframe=TimeFrame.Day,
        start="2022-01-01 00:00:00"
    )

    bars = trading_client.get_stock_bars(request_params)
    df = bars.df

    # Initialize your strategy with the historical data
    strategy = my_strat(df)

    # Generate buy/sell signals using your strategy
    strategy.generate_signals()

    # Retrieve buy/sell signals from the strategy
    buy_signals = strategy.get_buy_signals()
    sell_signals = strategy.get_sell_signals()
     # Simulate backtesting by creating a new DataFrame to track positions
    positions = pd.DataFrame(index=df.index)
    positions['Buy_Signal'] = buy_signals
    positions['Sell_Signal'] = sell_signals

    print(positions)
    # Save positions DataFrame to a CSV file
    positions.to_csv('backtesting.csv', na_rep='NaN')



if __name__ == "__main__":
    test()
