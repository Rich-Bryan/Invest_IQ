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
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go
import matplotlib.pyplot as plt



import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
import btalib
import pandas as pd


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

# Calculate SMAs
sma_20 = btalib.sma(df['close'], period=20).df
sma_50 = btalib.sma(df['close'], period=50).df

# Create candlestick trace
candlestick = go.Candlestick(
    x=df['timestamp'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='Candlestick'
)

# Create traces for SMAs
sma_20_trace = go.Scatter(
    x=df['timestamp'],
    y=sma_20['sma'],
    mode='lines',
    line=dict(color='blue'),
    name='SMA 20'
)

sma_50_trace = go.Scatter(
    x=df['timestamp'],
    y=sma_50['sma'],
    mode='lines',
    line=dict(color='red'),
    name='SMA 50'
)

# Create the figure and add traces
fig = go.Figure(data=[candlestick, sma_20_trace, sma_50_trace])
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()
