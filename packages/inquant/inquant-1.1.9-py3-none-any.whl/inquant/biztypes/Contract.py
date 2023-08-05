# -*- coding: utf-8 -*- 

from datetime import *
from inquant.biztypes.StrategyEnums import *

class Contract(object):
    """合约信息"""

    def __init__(self):
        """代码"""
        self.Symbol = ""

        """名称"""
        self.ContractName = ""

        """交易所"""
        self.Exchange = Exchange.UnKnow

        """投资品种类型"""
        self.ContractType = ContractType.UnKnow

        """合约细分类型"""
        self.ContDetailType = ContDetailType.Default

        """每股手数"""
        self.Lots = 1

        """最小价差"""
        self.PriceStep = 0

        """到期日"""
        self.ExpiryDate = datetime.now()

        """行权价"""
        self.StrikePx = 0.0

        """期权类型 P:Put C:Call"""
        self.Right = ""

        """上市日期"""
        self.ListingDate = datetime.now()

        """币种"""
        self.Currency = Currency.CNY

        """交易时间"""
        self.TradingTimes = []

class TradingTime(object):
    """交易时间"""

    def __init__(self):
        """开始时间"""
        self.Begin = ""

        """结束时间"""
        self.End = ""
