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
import plotly
import plotly.graph_objects as go
import matplotlib.pyplot as plt

import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
from stock import Stock

class SimpleMovingAverages(object):
    '''
    On given a OHLCV data frame, calculate corresponding simple moving averages
    '''
    def __init__(self, ohlcv_df, periods):
        self.ohlcv_df = ohlcv_df
        self.periods = periods
        self._sma = {}

    def _calc(self, period, price_source):
        result = None
        result = self.ohlcv_df[price_source].rolling(window=period).mean()
        return result
        
    def run(self, price_source = 'close'):
        '''
        Calculate all the simple moving averages as a dict
        '''
        for period in self.periods:
            self._sma[period] = self._calc(period, price_source)
    
    def get_series(self, period):
        return(self._sma[period])
    




class MACD(object):
    def __init__(self, ohlcv_df, periods):
        pass

#testing
if __name__ == "__main__":
    # Replace with your Alpaca API keys and desired symbol
    api_key = config.API_KEY
    api_secret = config.SECRET
    desired_symbol = 'SPY'  # Replace with the desired stock symbol

    #Calculate start and end dates for the last 9 trading days
    end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_date = (datetime.now() - timedelta(days=9)).strftime('%Y-%m-%d %H:%M:%S')


    trading_client = StockHistoricalDataClient(config.API_KEY, config.SECRET)

    request_params = StockBarsRequest(
                            symbol_or_symbols=["SPY"],
                            timeframe=TimeFrame.Day,
                            start="2022-01-01 00:00:00"
                    )
    bars = trading_client.get_stock_bars(request_params)
    df = bars.df

    # Instantiate the SMAAlpaca class
    periods = [100]
    smas = SimpleMovingAverages(df, periods)
    smas.run()
    s1 = smas.get_series(100)
    print("9 SMA", s1.index)
    print("9 SMA", s1.head(15))
    print("9 SMA", s1.tail(10))



