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
from datetime import datetime, timedelta
import btalib
import pandas as pd
from TA import *


trading_client = StockHistoricalDataClient(config.API_KEY, config.SECRET)



request_params = StockBarsRequest(
                        symbol_or_symbols=["SPY"],
                        timeframe=TimeFrame.Day,
                        start="2022-01-01 00:00:00"
            
                 )
bars = trading_client.get_stock_bars(request_params)
df = bars.df

df.reset_index(inplace=True)
print(df)




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

# Create traces for SMAs
sma_20_trace = go.Scatter(
    x=df['timestamp'],
    y=sma_20_values,
    mode='lines',
    line=dict(color='blue'),
    name='SMA 20'
)

sma_50_trace = go.Scatter(
    x=df['timestamp'],
    y=sma_50_values,
    mode='lines',
    line=dict(color='red'),
    name='SMA 50'
)
# Create MACD and Signal line traces
macd_trace = go.Scatter(
    x=df['timestamp'],
    y=macd_line,
    mode='lines',
    line=dict(color='purple'),
    name='MACD'
)

signal_trace = go.Scatter(
    x=df['timestamp'],
    y=signal_line,
    mode='lines',
    line=dict(color='orange'),
    name='Signal Line'
)

histogram_trace = go.Bar(
    x=df['timestamp'],
    y=macd_histogram,
    marker=dict(color=np.where(macd_histogram >= 0, 'green', 'red')),
    name='MACD Histogram'
)

# Adding candlestick trace to the first subplot
fig.add_trace(candlestick, row=1, col=1)
# Adding SMA traces to the first subplot
fig.add_trace(sma_20_trace, row=1, col=1)
fig.add_trace(sma_50_trace, row=1, col=1)

# Adding MACD and Signal Line traces to the second subplot
fig.add_trace(macd_trace, row=2, col=1)
fig.add_trace(signal_trace, row=2, col=1)
# Adding MACD Histogram trace to the second subplot
fig.add_trace(histogram_trace, row=2, col=1)


# Update layout
fig.update_layout(xaxis_rangeslider_visible=False, title='Candlestick with SMA & MACD with Signal Line')
fig.show()




