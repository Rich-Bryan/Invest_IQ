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


class my_strat():
    def __init__(self, ohlcv_df):
        self.ohlcv_df = ohlcv_df
        self.macd = None
        self.buy_signals = []
        self.sell_signals = []

    def generate_signals(self, short_period=12, long_period=26, signal_period=9):
        macd = MACD(self.ohlcv_df, short_period, long_period, signal_period)
        macd.calculate_macd()
        self.macd = macd

        macd_line = macd.get_macd_line()
        signal_line = macd.get_signal_line()

        self.buy_signals = [np.nan] * len(self.ohlcv_df)
        self.sell_signals = [np.nan] * len(self.ohlcv_df)

        flag = -1
        for i in range(len(self.ohlcv_df)):
             #check for sell signal
            if macd_line[i] > signal_line[i]:
                self.sell_signals[i] = np.nan
                if flag != 1:
                    self.buy_signals[i] = self.ohlcv_df['close'][i]
                    flag = 1
                else:
                    self.buy_signals[i] = np.nan
            #check for buy signal
            elif macd_line[i] < signal_line[i]:
                self.buy_signals[i] = np.nan
                if flag != 0:
                    self.sell_signals[i] = self.ohlcv_df['close'][i]
                    flag = 0
                else:
                    self.sell_signals[i] = np.nan
            else:
                self.buy_signals[i] = np.nan
                self.sell_signals[i] = np.nan

    def get_buy_signals(self):
        return self.buy_signals

    def get_sell_signals(self):
        return self.sell_signals
