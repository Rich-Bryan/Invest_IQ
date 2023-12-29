from config import ALPACA_CONFIG
from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader
import numpy as np
import pandas as pd


class MACDStrategy(Strategy):

    def initialize(self):
        signal = None
        start = "2022-01-01"

        self.signal = signal
        self.start = start
        self.sleeptime = "1D"

    def on_trading_iteration(self):
        bars = self.get_historical_prices("SPY", 27, "day")
        df = bars.df

        short_period = 12
        long_period = 26
        signal_period = 9

        df['ShortEMA'] = df['close'].ewm(span=short_period, adjust=False).mean()
        df['LongEMA'] = df['close'].ewm(span=long_period, adjust=False).mean()
        df['MACD'] = df['ShortEMA'] - df['LongEMA']
        df['Signal_Line'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()

        df['Signal'] = np.where(
            (df['MACD'] > df['Signal_Line']) & (df['MACD'].shift(1) < df['Signal_Line'].shift(1)),
            "BUY", None
        )
        df['Signal'] = np.where(
            (df['MACD'] < df['Signal_Line']) & (df['MACD'].shift(1) > df['Signal_Line'].shift(1)),
            "SELL", df['Signal']
        )

        self.signal = df.iloc[-1].Signal

        symbol = "SPY"  # Change symbol if needed
        quantity = 1000  # Change quantity if needed

        if self.signal == 'BUY':
            pos = self.get_position(symbol)
            if pos is not None:
                self.sell_all()
                
            order = self.create_order(symbol, quantity, "buy")
            self.submit_order(order)
        

        elif self.signal == 'SELL':
            pos = self.get_position(symbol)
            if pos is not None:
                self.sell_all()
                
            order = self.create_order(symbol, quantity, "sell")
            self.submit_order(order)


    

if __name__ == "__main__":
    trade = False
    if trade:
        broker = Alpaca(ALPACA_CONFIG)
        strategy = MACDStrategy(broker=broker)
        bot = Trader()
        bot.add_strategy(strategy)
        bot.run_all()
    else:
        start = datetime(2023, 1, 15)
        end = datetime(2023, 12, 15)
        MACDStrategy.backtest(
            YahooDataBacktesting,
            start,
            end
        )
