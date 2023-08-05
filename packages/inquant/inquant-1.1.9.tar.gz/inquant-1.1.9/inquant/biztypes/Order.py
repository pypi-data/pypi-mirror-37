# -*- coding: utf-8 -*- 

from datetime import  *  
from inquant.biztypes.StrategyEnums import *

class Order(object):
    """委托"""

    def __init__(self):
        """策略编号"""
        self.StrategyID = ""
        """委托ID"""
        self.OrderID = ""
        """股票代码或合约代码"""
        self.Symbol = ""
        """交易所"""
        self.Exchange = Exchange.UnKnow
        """委托方向"""
        self.OrderSide = OrderSide.Buy
        """开仓还是平仓 (期货中使用) 非期货为None"""
        self.Offset = Offset.UnKnow
        """委托数量"""
        self.Quantity = 0
        """委托价格"""
        self.Price = 0.0
        """成交数量"""
        self.Filled = 0
        """成交金额"""
        self.FilledPx = 0.0
        """委托时间"""
        self.OrderTime = datetime.now()
        """委托状态"""
        self.Status = OrderStatus.UnKnow
        """委托类型"""
        self.OrderType = OrderType.LMT
        """交易日"""
        self.TradeDate = datetime.now()
        """成交时间"""
        self.FilledTime = datetime.now()
        """委托备注"""
        self.Note = ""

        
