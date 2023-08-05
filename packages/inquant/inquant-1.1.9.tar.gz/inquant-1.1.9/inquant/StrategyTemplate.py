# -*- coding: utf-8 -*-
import threading
import datetime
from time import sleep
import traceback
import os
import sys
from inquant.biztypes import *
import clr
import System

#add current path to prevent python file debug error
currPath = os.path.dirname(__file__)
libpath = os.path.abspath(os.path.join(currPath,"libs"))
sys.path.insert(0,libpath)

#add current path to prevent packaging exe error
libpath = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.insert(0,libpath)

clr.AddReference('InQuant.OpenApi')
import InQuant.OpenApi

class StrategyTemplate(object):
    """
    策略模板
    """
    def __init__(self):
        """构造函数"""
        #策略服务
        self.__strategyService = InQuant.OpenApi.StrategyService()
        self.__strategyService.OnTick += System.Action[InQuant.OpenApi.TickData](self.__OnTick)
        self.__strategyService.OnBar += System.Action[InQuant.OpenApi.BarData](self.__OnBar)
        self.__strategyService.OnOrderChanged += System.Action[InQuant.OpenApi.Order](self.__OnOrderChanged)

    def Init(self, cfgPath,logPath):
        """初始化"""
        if not os.path.isfile(cfgPath):
            cfgPath = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]),cfgPath))
        self.WriteInfo("加载配置文件:" + cfgPath)
        resp = self.__strategyService.Init(cfgPath,logPath)

        #检查返回值
        if not resp:
            return False
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return False
        return True

    def CreateScheduler(self,schedulerFunc,times):
        """创建定时任务
        schedulerFunc : 定时任务回调函数
        times : 定时触发时间，如[90000,161005]，每日9点0分0秒和16点10分5秒触发schedulerFunc"""
        if not schedulerFunc or not times:
            return False
        t = threading.Thread(target=self.__SchedulerCallback,args=(schedulerFunc,times,))
        t.setDaemon(True)
        t.start()

    def __SchedulerCallback(self,schedulerFunc,times):
        """定时任务回调"""
        if not schedulerFunc or not times:
            return

        preExecTime = 0
        while(True):
            try:
                timeStr = datetime.now().strftime('%Y%m%d%H%M%S')
                currTime = int(timeStr)
                if (preExecTime != currTime and currTime % 1000000 in times):
                    self.WriteInfo("run scheduler:" + timeStr)
                    preExecTime = currTime
                    schedulerFunc()
            except Exception as e:
                self.WriteError(str(e),True)
            sleep(0.2)

    def Start(self):
        """启动"""
        resp = self.__strategyService.Start()
        #检查返回值
        if not resp:
            return False
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return False
        return True

    def SendOrder(self, symbol, exchange, orderSide, price, quantity, orderType, offset=Offset.UnKnow, clientOrderID=''):
        """发送委托请求"""
        resp = self.__strategyService.SendOrder(clientOrderID, symbol, exchange, orderSide, price, quantity, orderType, offset)
        
        #检查返回值
        if not resp:
            return False
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return False
        self.WriteInfo(str([symbol, exchange, orderSide, price, quantity, orderType, offset, clientOrderID, resp.ErrorMsg]))
        return True

    def CancelOrder(self,orderID):
        """撤单"""
        resp = self.__strategyService.CancelOrder(orderID)
        
        #检查返回值
        if not resp:
            return False
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return False
        return True

    def GetAssetInfo(self):
        """查询资产信息"""
        resp = self.__strategyService.GetAssetInfo()

        #检查返回值
        if not resp:
            return None
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return None
        if not resp.Data:
            return None
        return self.__ToAssetInfo(resp.Data)
    
    def GetOrder(self,clientOrderID):
        """根据clientOrderID 获取订单详情"""
        resp = self.__strategyService.GetOrder(clientOrderID)
        
        #检查返回值
        if not resp:
            return None
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return None
        if not resp.Data:
            return None
        return self.__ToOrder(resp.Data)

    def GetOpenOrders(self):
        """获取打开的订单"""
        resp = self.__strategyService.GetOpenOrders()

        #检查返回值
        if not resp:
            return None
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return None
        if not resp.Data:
            return list()

        #格式化
        orderlist = list()
        for item in resp.Data:
            order = self.__ToOrder(item)
            orderlist.append(order)
        return orderlist

    def GetOrders(self):
        """获取当日委托"""
        resp = self.__strategyService.GetOrders()
        
        #检查返回值
        if not resp:
            return None
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return None
        if not resp.Data:
            return list()

        #格式化
        orderlist = list()
        for item in resp.Data:
            order = self.__ToOrder(item)
            orderlist.append(order)
        return orderlist

    def GetPositions(self):
        """查询当前持仓"""
        resp = self.__strategyService.GetPositions()

        #检查返回值
        if not resp:
            return None
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return None
        if not resp.Data:
            return list()

        #格式化
        posList = list()
        for item in resp.Data:
            pos = self.__ToPosition(item)
            posList.append(pos)
        return posList

    def GetContract(self,symbol, exchange):
        """获取证券基本信息"""
        resp = self.__strategyService.GetContract(symbol, exchange)
        
        #检查返回值
        if not resp:
            return None
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return None
        if not resp.Data:
            return None
        return self.__ToContract(resp.Data)

    def GetFutContracts(self,varietyCode, exchange, futType):
        """根据品种代码获取证券基本信息
        varietyCode : 品种代码
        exchange : 交易所
        contDetailType : 期货合约类型 -1:获取所有合约 0:获取主力合约 1:常规合约 2:主连合约 3:指数合约"""
        resp = self.__strategyService.GetFutContracts(varietyCode, exchange, futType)

        #检查返回值
        if not resp:
            return None
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return None
        if not resp.Data:
            return list()
        #格式化
        contractlist = list()
        for item in resp.Data:
            contract = self.__ToContract(item)
            contractlist.append(contract)
        return contractlist
    
    def GetLastTick(self, symbol, exchange, count=1):
        """获取最近几笔TICK行情"""
        resp = self.__strategyService.GetLastTick(symbol,exchange,count)

        #检查返回值
        if not resp:
            return None
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return None
        if not resp.Data:
            return list()
        #格式化
        ticklist = list()
        for item in resp.Data:
            tick = self.__ToTick(item)
            ticklist.append(tick)
        return ticklist

    def GetLastBar(self, symbol, exchange, barType, count=1):
        """获取最近几笔BAR行情"""
        resp = self.__strategyService.GetLastBar(symbol,exchange,barType,count)

        #检查返回值
        if not resp:
            return None
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return None
        if not resp.Data:
            return list()
        #格式化
        barlist = list()
        for item in resp.Data:
            bar = self.__ToBar(item)
            barlist.append(bar)
        return barlist

    def GetHisBar(self, symbol, exchange, barType, count, startTime=None):
        """获取历史行情数据
        symbol : 品种代码
        exchange : 交易所
        barType : K线类型，以秒为单位（1分钟:60 5分钟:6*60 15分钟:15*60 30分钟:30*60 60分钟:60*60 日:24*60*60 月:30*24*60*60 年:365*24*60*60）
        count : K线数量
        startTime : 起始时间:%Y%m%d%H%M%S """

        if not startTime:
            startTime = int(datetime.now().strftime("%Y%m%d%H%M%S"))
        resp = self.__strategyService.GetHisBar(symbol,exchange,barType,startTime,count)

        #检查返回值
        if not resp:
            return None
        if resp.IsError:
            self.WriteError(resp.ErrorMsg)
            return None
        if not resp.Data:
            return list()
        #格式化
        barlist = list()
        for item in resp.Data:
            bar = self.__ToBar(item)
            barlist.append(bar)
        return barlist

    def WriteError(self, log, islogtrace=False):
        """写错误日志"""
        print(log)
        self.__strategyService.WriteLog("strategyError", log)
        if islogtrace:
            tracelog = traceback.format_exc()
            print(tracelog)
            self.__strategyService.WriteLog("strategyError", tracelog)

    def WriteInfo(self, log):
        """写一般日志"""
        print(log)
        self.__strategyService.WriteLog("strategy", log)

    def OnBar(self,bar):
        """当有Bar数据推送来的时候做的处理"""
        pass

    def OnTick(self,tick):
        """当有Tick数据推送来的时候做的处理"""
        pass

    def OnOrderChanged(self,order):
        """当有成交回报推送来的时候做的处理"""
        pass

    def __OnTick(self, tickData): 
        """Net类型转化为Python类型"""
        if tickData == None:
            return
        try:
            tick = self.__ToTick(tickData)
            self.OnTick(tick)
        except Exception as e:
            self.WriteError(str(e),True) 

    def __OnBar(self,barData):
        """Net类型转化为Python类型"""
        if barData == None:
            return
        try:
            bar = self.__ToBar(barData)
            self.OnBar(bar)
        except Exception as e:
            self.WriteError(str(e),True)

    def __OnOrderChanged(self,orderData):
        """Net类型转化为Python类型"""
        if orderData == None:
            return
        try:
            order = self.__ToOrder(orderData)
            self.OnOrderChanged(order)
        except Exception as e:
            self.WriteError(str(e),True)

    def __ToContract(self,data):
        """Net类型转化为Python类型"""
        if not data:
            return None
        contract = Contract()
        contract.Symbol = data.Symbol
        contract.ContractName = data.ContractName
        contract.Exchange = Exchange(data.Exchange)
        contract.ContractType = ContractType(data.ContractType)
        contract.Lots = data.Lots
        contract.PriceStep = data.PriceStep
        contract.ExpiryDate = self.__ToDateTime(data.ExpiryDate)
        contract.StrikePx = data.StrikePx
        contract.Right = data.Right
        contract.ListingDate = self.__ToDateTime(data.ListingDate)
        contract.Currency = Currency(data.Currency)
        contract.ContDetailType = ContDetailType(data.ContDetailType)

        for x in data.TradingTimes:
            tradingTime = TradingTime()
            tradingTime.Begin = x.Begin
            tradingTime.End = x.End
            contract.TradingTimes.append(tradingTime)

        return contract

    def __ToBar(self,data):
        """Net类型转化为Python类型"""
        if not data:
            return None
        bar = BarData()
        bar.BarType = data.BarType
        bar.Exchange = Exchange(data.Exchange)
        bar.HighPx = data.HighPx
        bar.LowPx = data.LowPx
        bar.LastPx = data.LastPx
        bar.LocalTime = self.__ToDateTime(data.LocalTime)
        bar.PreClosePx = data.PreClosePx
        bar.Symbol = data.Symbol
        bar.Volume = data.Volume
        bar.OpenPx = data.OpenPx
        return bar

    def __ToTick(self,data):
        """Net类型转化为Python类型"""
        if not data:
            return None
        tick = TickData()
        tick.Symbol = data.Symbol
        tick.Exchange = Exchange(data.Exchange)
        tick.LocalTime = self.__ToDateTime(data.LocalTime)
        tick.LastPx = data.LastPx
        tick.Volume = data.Volume
        tick.OpenInterest = data.OpenInterest
        tick.OpenPx = data.OpenPx
        tick.HighPx = data.HighPx
        tick.LowPx = data.LowPx
        tick.PreClosePx = data.PreClosePx

        for x in data.Bids:
            unit = LevelUnit()
            unit.Px = x.Px
            unit.Vol = x.Vol
            tick.Bids.append(unit)

        for x in data.Asks:
            unit = LevelUnit()
            unit.Px = x.Px
            unit.Vol = x.Vol
            tick.Asks.append(unit)
        return tick

    def __ToOrder(self,data):
        """Net类型转化为Python类型"""
        if not data:
            return None
        order = Order()
        order.Exchange = Exchange(data.Exchange)
        order.Filled = data.Filled
        order.FilledPx = data.FilledPx
        order.FilledTime = self.__ToDateTime(data.FilledTime)
        order.Note = data.Note
        order.Offset = Offset(data.Offset)
        order.OrderID = data.OrderID
        order.OrderSide = OrderSide(data.OrderSide)
        order.OrderTime = self.__ToDateTime(data.OrderTime)
        order.OrderType = OrderType(data.OrderType)
        order.Price = data.Price
        order.Quantity = data.Quantity
        order.Status = OrderStatus(data.Status)
        order.Symbol = data.Symbol
        order.TradeDate = self.__ToDateTime(data.TradeDate)
        order.StrategyID = data.StrategyID
        return order

    def __ToPosition(self,data):
        """根据clientOrderID 获取订单详情"""
        if not data:
            return None
        pos = Position()
        pos.StrategyID = data.StrategyID
        pos.Symbol = data.Symbol
        pos.Exchange = Exchange(data.Exchange)
        pos.Quantity = data.Quantity
        pos.Frozen = data.Frozen
        pos.CostPx = data.CostPx
        pos.PosSide = PosSide(data.PosSide)
        pos.Margin = data.Margin
        return pos

    def __ToAssetInfo(self,data):
        """根据clientOrderID 获取订单详情"""
        if not data:
            return None
        asset = AssetInfo()
        asset.Currency = Currency(data.Currency)
        asset.StrategyID = data.StrategyID
        asset.TotalAsset = data.TotalAsset
        asset.Available = data.Available
        asset.Margin = data.Margin
        asset.Balance = data.Balance
        return asset

    def __ToDateTime(self,src):
        return src.ToString("yyyy-MM-dd HH:mm:ss")

if __name__ == '__main__':
   
    strategy = StrategyTemplate()
    strategy.Init("demo.json")
    strategy.Start()
