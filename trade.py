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


from strategy import SimpleMovingAverages

trading_client = StockHistoricalDataClient(config.API_KEY, config.SECRET)



request_params = StockBarsRequest(
                        symbol_or_symbols=["SPY"],
                        timeframe=TimeFrame.Day,
                        start="2022-01-01 00:00:00"
            
                 )
bars = trading_client.get_stock_bars(request_params)
df = bars.df
print(df)


#show the line graph
df.reset_index(inplace=True)

# #show candle stick grpah
# Create candlestick trace
candlestick = go.Candlestick(
    x=df['timestamp'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='Candlestick'
)

# fig = go.Figure(data=[candlestick])
# fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()

# use the functino from my TA
sma_periods = [9, 50, 100, 200]
smas = SimpleMovingAverages(df, sma_periods)
# Calculate the SMAs
smas.run()


# Create an array to store the calculated SMAs
sma_plots = []

# Create an array to store the calculated SMAs
sma_plots = []

# Iterate through the SMA periods and create Plotly traces
for period in sma_periods:
    sma_data = smas.get_series(period)  # Retrieve SMA data for the current period
    sma_plot = go.Scatter(x=sma_data.index, y=sma_data.values, mode='lines', name=f"SMA {period}")
    sma_plots.append(sma_plot)
#plot the data
#include all the elements from *sma_plots
fig = go.Figure(data=[candlestick , *sma_plots])
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()