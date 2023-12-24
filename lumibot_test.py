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
from config import ALPACA_CONFIG
from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader


trading_client = StockHistoricalDataClient(config.API_KEY, config.SECRET)

request_params = StockBarsRequest(
                        symbol_or_symbols=["SPY"],
                        timeframe=TimeFrame.Day,
                        start="2022-01-01 00:00:00"

                 )
bars = trading_client.get_stock_bars(request_params)
df = bars.df

df.reset_index(inplace=True)


fig = make_subplots(rows=2, cols=1)

# Create candlestick trace
candlestick = go.Candlestick(
    x=df['timestamp'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='Candlestick'
)

# Calculate SMAs
# Instantiate the SMA class for 20 and 50 periods
sma_20 = SimpleMovingAverages(df, [20])
sma_20.run()
sma_20_values = sma_20.get_series(20)

sma_50 = SimpleMovingAverages(df, [50])
sma_50.run()
sma_50_values = sma_50.get_series(50)

# MACD calculation
macd_indicator = MACD(df, 12, 26, 9)
macd_indicator.calculate_macd()
macd_line = macd_indicator.get_macd_line()
signal_line = macd_indicator.get_signal_line()
macd_histogram = macd_indicator.get_macd_histogram()


class MyStrategy(Strategy):
    # Custom parameters
    parameters = {
        "symbol": "SPY",
        "quantity": 75,
        "side": "buy"
    }

    def initialize(self, symbol=""):
        # Will make on_trading_iteration() run every 180 minutes
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        symbol = self.parameters["symbol"]
        quantity = self.parameters["quantity"]
        side = self.parameters["side"]

        bars = self.get_historical_prices("SPY", 100, "day")
        df = bars.df

        # Then, to get the DataFrame of SPY data
        df = bars.df
        # Calculate MACD values
        short_period = 12
        long_period = 26
        signal_period = 9

        # Calculate Short and Long EMAs
        df['ShortEMA'] = df['close'].ewm(span=short_period, adjust=False).mean()
        df['LongEMA'] = df['close'].ewm(span=long_period, adjust=False).mean()
        df['LongEMA'] = df['close'].ewm(span=200, adjust=False).mean()

        # Calculate MACD line
        df['MACD'] = df['ShortEMA'] - df['LongEMA']

        # Calculate Signal line (9-day EMA of MACD)
        df['Signal_Line'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()

        # Calculate MACD Histogram
        df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']

        # Check for crossover - Buy when MACD crosses above Signal line
        if df['Signal_Line'].iloc[-1] > df['MACD'].iloc[-1]:
            # Generate buy signal
            order = self.create_order(symbol, quantity, "buy")
            self.submit_order(order)
        # Check for crossover - Sell when MACD crosses below Signal line
        elif df['Signal_Line'].iloc[-1] < df['MACD'].iloc[-1]:
            # Generate sell signal
            order = self.create_order(symbol, quantity, "sell")
            self.submit_order(order)

if __name__ == "__main__":
    trade = False
    if trade:
        broker = Alpaca(ALPACA_CONFIG)
        strategy = MyStrategy(broker=broker)
        trader = Trader()
        trader.add_strategy(strategy)
        trader.run_all()
    else:
        start = datetime(2022, 1, 1)
        end = datetime(2023, 10, 31)
        MyStrategy.backtest(
            YahooDataBacktesting,
            start,
            end
        )