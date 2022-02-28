import ccxt
import time
from pprint import pprint
import os
import logging
import datetime


# 查看交易所,api设置,改成你的API
huobipro = ccxt.huobipro({
    'apiKey': '',
    'secret': '',
})





# dest_time = datetime.datetime.now() + datetime.timedelta(seconds=5)   # 调试用

# 参数设置，到23：59分59秒时暂停
dest_time = year=2021,month=5,day=9,hour=23,minute=59,second=59
#到 0：05分暂停买入
end_buy_time = year=2021,month=5,day=10,hour=0,minute=4,second=0
# 监控的币种清单
coins = ["TOP","SWFTC","LOL","DTA","OGO","PAI","EM","OCN","FTI","EGT"] # 0点币
# coins = ["RUFF","SOC","TITAN","LOL","OCN"]


# 触发买入价格
bought_rate = 1.021
# 触发卖出价格
sell_rate = 0.998
# 止盈价格
kill_earn_rate_high = 1.18
kill_earn_middle = 1.11
kill_earn_low_drop = 1.07

# 一个仓位多少U
base_money = 200
# 执行几次买入操作,PS买入过的币不会再买
buy_how_many_coin = 1

# 购买日志，放在同目录文件夹下的buglog.txt文件中
buylog = open("buylog.txt",'w')
# 币种的买入价格
buydict = {}

# generate_trigger_price 控制所有标记点生成操作只执行一次
generate_trigger_price = False
# 未成交的币种清单
not_bought_coins = coins
# 已成交的币种清单
bought_coins = []
# 触发中间价格清单
touch_10_coins = []

# 说明文档
"""最后更新 4-11 9:24 pm
    参数在上面设置，
"""

print('目标时间：' + str(dest_time))
print('当前时间：' + str(datetime.datetime.now()))
while True:
    # 每隔一秒请求一次服务器价格
    time.sleep(1)

    # 标记时间为每日的23:59:59秒
    delta = dest_time - datetime.datetime.now()
    delta_end_buy_time = end_buy_time - datetime.datetime.now()
    # 到生成标记的时间
    if delta < datetime.timedelta(microseconds=1) and generate_trigger_price == False:
        trigger_buy_price = {} # 买入标记点
        trigger_sell_price = {} # 卖出标记点
        trigger_kill_earn_low = {}  # 止盈标记点 10%出一半仓位
        trigger_kill_earn_low_drop = {}  # 止盈标记点 如果涨到12再回落到7%出全仓
        trigger_kill_earn_high = {} # 止盈标记点  18%出全仓


        print("买入、止损标记点已生成")
        for coin in coins:
            present_name = coin+"_Last"
            present_price = huobipro.fetch_ticker(coin + '/USDT')['last'] #爬取每个币现在的价格
            time.sleep(0.1)
            trigger_buy_price[coin] = present_price*bought_rate
            trigger_sell_price[coin] = present_price*sell_rate
            trigger_kill_earn_low[coin] = present_price*kill_earn_middle
            trigger_kill_earn_high[coin] = present_price*kill_earn_rate_high
            trigger_kill_earn_low_drop[coin] = present_price*kill_earn_low_drop

        pprint('买入价格：')
        pprint(trigger_buy_price)
        pprint('卖出价格：')
        pprint(trigger_sell_price)
        pprint('止盈价格：')
        # pprint('middle:' + kill_earn_middle)
        # pprint('high:' + trigger_kill_earn_high)
        # pprint('回落止损:' + trigger_kill_earn_low_drop)


        generate_trigger_price = True # 生成标记点的操作只执行一次

        print('\n\n\n')
        print("持续监控中....")


    # 未到标记点生成时间，查询各币种价格，或者已经生成了标记点，监控买入卖出
    elif delta > datetime.timedelta(microseconds=1) or generate_trigger_price == True:
        if not generate_trigger_price:

        else:
            # 已经生成了标记点，监控每个币种是否到达触发价格，达到标的价格的时候触发买入委托

                    # 写买入日志


            # 卖出循环监控
            for coin in bought_coins:
                present_price = huobipro.fetch_ticker(coin + '/USDT')['last']
                # 如果买入了，结果回落导致当前价格小于等于止损价格就触发卖出止损
                if present_price <= trigger_sell_price[coin]:


                    # 只有有持仓才会去卖（清仓），防止出现无余额的卖单出现
                    if order_amount > 1:


                # 如果到达中间止盈点，就卖出一半
                # 卖单参数 设置
                if present_price >= trigger_kill_earn_low[coin] and (coin not in touch_10_coins):

                    # 12%出一半
                    # 只有有持仓才会去卖（清仓），防止出现无余额的卖单出现
                    if order_amount > 1:
                    else:


                # 如果到达止盈点18% 就全卖出
                # 卖单参数 设置
                if present_price >= trigger_kill_earn_high[coin] and (coin in touch_10_coins):


                # 如果涨到12之后又回落到6%以下就清仓
                if present_price <= trigger_kill_earn_low_drop[coin] and (coin in touch_10_coins):

                    # 只有有持仓才会去卖（清仓），防止出现无余额的卖单出现
                    if order_amount > 1:


                    else:
                        print('没有持仓' + order_symbol)


