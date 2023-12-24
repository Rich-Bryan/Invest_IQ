from config import ALPACA_CONFIG
from datetime import datetime, timedelta
from lumibot.backtesting import YahooDataBacktesting
from lumibot.brokers import Alpaca
from lumibot.strategies import Strategy
from lumibot.traders import Trader
import numpy as np
import pandas as pd


class Trend(Strategy):

    def initialize(self):
        signal = None
        start = "2022-01-01"

        self.signal = signal
        self.start = start
        self.sleeptime = "1D"
    # minute bars, make functions    

    def on_trading_iteration(self):
        bars = self.get_historical_prices("QQQ", 22, "day")
        qqq = bars.df
        # qqq = pd.DataFrame(yf.download("QQQ", self.start)['Close'])
        qqq['9-day'] = qqq['close'].rolling(9).mean()
        qqq['21-day'] = qqq['close'].rolling(21).mean()
        qqq['Signal'] = np.where(np.logical_and(qqq['9-day'] > qqq['21-day'],
                                                qqq['9-day'].shift(1) < qqq['21-day'].shift(1)),
                                "BUY", None)
        qqq['Signal'] = np.where(np.logical_and(qqq['9-day'] < qqq['21-day'],
                                                qqq['9-day'].shift(1) > qqq['21-day'].shift(1)),
                                "SELL", qqq['Signal'])
        self.signal = qqq.iloc[-1].Signal

        symbol = "QQQ"
        quantity = 200
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
        strategy = Trend(broker=broker)
        bot = Trader()
        bot.add_strategy(strategy)
        bot.run_all()
    else:
        start = datetime(2022, 4, 15)
        end = datetime(2023, 4, 15)
        Trend.backtest(
            YahooDataBacktesting,
            start,
            end
        )