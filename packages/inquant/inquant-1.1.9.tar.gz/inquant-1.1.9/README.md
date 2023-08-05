

inquant future quant api

# -*- coding: utf-8 -*-
from StrategyTemplate import *

class MyStrategy(StrategyTemplate):
    """我的策略"""

    def __init__(self):
        """构造函数"""
        super(MyStrategy,self).__init__()

    def OnTick(self, data):
        """Tick数据处理 注data参数一次只有一条tick数据"""
        print("tickqqqqq",data.Symbol,data.LocalTime,data.Exchange)

        pass

    def OnBar(self, data):
        """Bar数据处理 注data参数一次只有一条bar数据"""
        print("bar",data.Symbol,data.LocalTime,data.Exchange)

        resp10 = strategy.GetLastBar('rb1901',Exchange.SHFE,60,5)

        print(resp10[0].Symbol,resp10[0].LocalTime)
        pass

    def OnOrderChanged(self,order):
        """成交回报处理"""
        pass

    def TaskCallback(self):
        print(datetime.now().time())

if __name__ == '__main__':

    #新建策略
    strategy = MyStrategy()

    #创建定时任务
    strategy.CreateScheduler(strategy.TaskCallback,[90000,161005])

    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,-1)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,0)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,1)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,2)
    contracts = strategy.GetFutContracts('rb',Exchange.SHFE,3)

    strategy.WriteInfo(u"开始初始化策略...")
    #初始化
    ret = strategy.Init("demo.json","d:\\strategylog\\")
    if not ret:
        strategy.WriteError("u初始化策略失败！！！")
        input(u"按任意键退出")
        sys.exit()
    strategy.WriteInfo(u"初始化策略成功")

    strategy.WriteInfo(u"开始启动策略...")
    resp = strategy.Start()
    if not resp:
        strategy.WriteError(u"策略启动失败！！")
        input(u"按任意键退出")
        sys.exit()
    strategy.WriteInfo(u"策略启动成功")

    resp4 = strategy.SendOrder('rb1901',Exchange.SHFE,OrderSide.Buy,4166,1,OrderType.LMT,Offset.Open)
    resp5 = strategy.CancelOrder('7ba0ab1c8319442299c835269f600f3f')

    resp1 = strategy.GetAssetInfo()
    resp2 = strategy.GetOrders()
    resp3 = strategy.GetPositions()
        
    resp6 = strategy.GetOrder('7ba0ab1c8319442299c835269f600f3f')
    resp7 = strategy.GetOpenOrders()
    resp8 = strategy.GetContract('rb1901',Exchange.SHFE)
    resp9 = strategy.GetLastTick('rb1901',Exchange.SHFE,2)
    resp10 = strategy.GetLastBar('rb1901',Exchange.SHFE,300,5)

    input(u"策略执行中，按任意键退出...")
