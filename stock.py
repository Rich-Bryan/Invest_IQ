import datetime as dt
import numpy as np
import pandas as pd 
import config
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest# Create 
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




class Stock(object):
    def __init__(self, api_key, api_secret, symbol, timeFrame, start_date):
        self.api = StockHistoricalDataClient(api_key, api_secret) 
        self.symbol = symbol
        self.timeFrame = timeFrame
        self.start_date = start_date


    def get_historical_data(self):
        # Fetch historical stock bars data using Alpaca API
        bars = self.api.get_stock_bars(StockBarsRequest(
            symbol_or_symbols=[self.symbol],
            timeframe=self.timeFrame,
            start=self.start_date,
        ))
        df = bars.df
        return df


#testing
if __name__ == "__main__":
    # Replace with your Alpaca API keys and desired symbol
    api_key = config.API_KEY
    api_secret = config.SECRET
    desired_symbol = 'SPY'  # Replace with the desired stock symbol

    #Calculate start and end dates for the last 9 trading days
    end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')

    stock = Stock(api_key,api_secret,desired_symbol,TimeFrame.Day,start_date)

    df = stock.get_historical_data()

    #adding the 100SMA to the data frame
    sma = btalib.sma(df, period = 20)
    sma = btalib.sma(df, period = 50)
    # df['sma100'] = sma['sma']
    # print(df)

    # Defines the plot for each trading symbol
    f, ax = plt.subplots()
    f.suptitle("SPY")


    


