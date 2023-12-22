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
    
class ExponentialMovingAverages(object):
    '''
    On given a OHLCV data frame, calculate corresponding simple moving averages
    '''
    def __init__(self, ohlcv_df, periods):
        #
        self.ohlcv_df = ohlcv_df
        self.periods = periods
        self._ema = {}

    def _calc(self, period, price_source):
        result = None
        #use the ewm() to calc EMA, only need the numeric values 
        result = self.ohlcv_df[price_source].ewm(span=period, adjust=False, ignore_na=True).mean(numeric_only=True)

        return(result)

    def run(self, price_source = 'close'):

        for period in self.periods:
            self._ema[period] = self._calc(period, price_source)

    def get_series(self, period):
        return(self._ema[period])



class MACD(object):
    def __init__(self, ohlcv_df, short_period, long_period, signal_period):
        self.ohlcv_df = ohlcv_df
        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period
        self._macd = {}
        self._signal_line = {}

    def calculate_macd(self, price_source='close'):
        # Calculate short and long EMAs
        ema_short = ExponentialMovingAverages(self.ohlcv_df, [self.short_period])
        ema_short.run(price_source)
        ema_long = ExponentialMovingAverages(self.ohlcv_df, [self.long_period])
        ema_long.run(price_source)

        # Calculate MACD line
        self._macd = ema_short.get_series(self.short_period) - ema_long.get_series(self.long_period)

        # Calculate Signal line (which is an EMA of the MACD line)
        ema_signal = ExponentialMovingAverages(pd.DataFrame(self._macd), [self.signal_period])
        ema_signal.run()
        self._signal_line = ema_signal.get_series(self.signal_period)

    def get_macd_line(self):
        return self._macd

    def get_signal_line(self):
        return self._signal_line




#testing
if __name__ == "__main__":
    # Replace with your Alpaca API keys and desired symbol
    api_key = config.API_KEY
    api_secret = config.SECRET
    desired_symbol = 'SPY'  # Replace with the desired stock symbol

    #Calculate start and end dates for the last 9 trading days
    end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_date = (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d %H:%M:%S')


    trading_client = StockHistoricalDataClient(config.API_KEY, config.SECRET)

    request_params = StockBarsRequest(
                            symbol_or_symbols=["SPY"],
                            timeframe=TimeFrame.Day,
                            start="2022-01-01 00:00:00"
                    )
    bars = trading_client.get_stock_bars(request_params)
    df = bars.df

    # Instantiate the SMAAlpaca class
    periods = [9]
    smas = SimpleMovingAverages(df, periods)
    smas.run()
    s1 = smas.get_series(9)


    print("9 SMA", s1.tail(10))

    E_periods = [9]
    emas = ExponentialMovingAverages(df, E_periods)
    emas.run()
    s2 = emas.get_series(9)

    print("9 eMA", s2.tail(10))


