#! python3
# -*- coding:utf-8 -*-

from pyalgotrade import strategy
from pyalgotrade.bar import Frequency
from ccwt_client.ccwt_feed import Feed

# 构建一个策略
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__instrument = instrument

    def onBars(self, bars):  # 每一个数据都会抵达这里，就像becktest中的next
        bar = bars[self.__instrument]
        self.info(bar.getClose())  # 我们打印输出收盘价

if __name__ == '__main__':
    # 获得回测数据
    feed = Feed(Frequency.MINUTE)
    #feed.loadBars('okex_LIGHTUSDT')
    #feed.loadBars('binance_TRXBTC')
    feed.loadBars('bitmex_XBTUSD')

    # 把策略跑起来
    #myStrategy = MyStrategy(feed, "okex_LIGHTUSDT")
    #myStrategy = MyStrategy(feed, "binance_TRXBTC")
    myStrategy = MyStrategy(feed, "bitmex_XBTUSD")
    myStrategy.run()
