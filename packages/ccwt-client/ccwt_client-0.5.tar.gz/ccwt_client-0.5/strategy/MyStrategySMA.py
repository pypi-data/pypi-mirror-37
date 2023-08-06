#! python3
# -*- coding:utf-8 -*-

from pyalgotrade import strategy
from pyalgotrade.bar import Frequency
from ccwt_client.ccwt_feed import Feed
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi



# 构建一个策略
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.__sma_rsi = ma.SMA(self.__rsi, 15)
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 2)
        self.__instrument = instrument

    def onBars(self, bars):  # 每一个数据都会抵达这里
        bar = bars[self.__instrument]
        self.info("%s %s %s" % (bar.getClose(), self.__sma[-1], self.__sma_rsi[-1]))  # 我们打印输出收盘价与两分钟均线值

if __name__ == '__main__':
    # 获得回测数据
    feed = Feed(Frequency.SECOND)
    feed.loadBars('bitmex_BCHZ18')

    # 把策略跑起来
    myStrategy = MyStrategy(feed, "bitmex_BCHZ18")
    myStrategy.run()
