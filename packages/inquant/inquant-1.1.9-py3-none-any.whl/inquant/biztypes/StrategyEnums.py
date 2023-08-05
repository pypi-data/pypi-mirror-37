# -*- coding: utf-8 -*- 

from enum import IntEnum

class OrderType(IntEnum):
        """限价"""
        LMT = 0
        """市价"""
        MKT = 1

class OrderStatus(IntEnum):
        """ 未知""" 
        UnKnow = -1
        """ 未发（下单指令还未发送到下游）"""
        NotSent = 0
        """ 1 已发（下单指令已发送给下游）"""
        Sended = 1
        """ 2 已报（下单指令已报给交易所）"""
        Accepted = 2
        """ 部分成交 """
        PartiallyFilled = 3
        """ 4 已撤（可能已经部分成交，要看看filled字段）"""
        Cancelled = 4
        """ 5 全部成交 """
        Filled = 5
        """ 6 已拒绝 """
        Rejected = 6
        """ 7 撤单请求已发送，但不确定当前状态 """
        PendingCancel = 7

class OrderSide(IntEnum):
        """买入"""
        Buy = ord('B')
        """卖出"""
        Sell = ord('S')

class Offset(IntEnum):
        """未知"""
        UnKnow = 0
        """开仓""" 
        Open = 1
        """平仓 """ 
        Close = 2
        """ 平今 """
        CloseToday = 3
        """ 平昨 """
        CloseYesterday = 4

class Exchange(IntEnum):
        """未知"""
        UnKnow = 0
        """上交所"""
        SHSE = 1
        """深交所"""
        SZSE = 2
        """中金所"""
        CFFEX = 3
        """上期所"""
        SHFE = 4
        """大商所"""
        DCE = 5
        """郑商所"""
        CZCE = 6
        """港交所"""
        HKSE = 7
        """纳斯达克"""
        NASDAQ = 8
        """纽约证券交易所"""
        NYSE = 9
        """全美证券交易所"""
        AMEX = 10
        """新三板"""
        SBSE = 11
        """伦敦商品交易所"""
        LME = 12
        """马来西亚衍生产品交易所"""
        BMD = 13
        """东京商品交易所"""
        TOCOM = 14
        """上海国际能源交易中心"""
        INE = 15

class ContractType(IntEnum):
        """合约类型"""

        """未知"""
        UnKnow = 0
        """股票"""
        Stock = 1
        """期货"""
        Future = 2
        """期权"""
        Option = 3

class ContDetailType(IntEnum):
        """合约细分类型"""

        """常规合约"""
        Default = 1
        """主连合约"""
        Main = 2
        """指数合约"""
        Index = 3

class Currency(IntEnum):
		"""人民币"""
		CNY = 0
		"""美元"""
		USD = 1
		"""港币"""
		HKD = 2

class PosSide(IntEnum):
        """净持仓"""
        Net = 0
        """多仓"""
        Long = 1
        """空仓"""
        Short = 2