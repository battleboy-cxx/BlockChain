#!/usr/bin/python3.6
# encoding: utf-8
import sys
import ccxt
import time
from pprint import pprint
import os
import logging
import datetime
import traceback


# 查看交易所,api设置,改成你的API
huobipro = ccxt.huobipro({
    'apiKey': '',
    'secret': '',
})

# api_1
huobipro1 = ccxt.huobipro({
    'apiKey': '',
    'secret': '',
})
# api_2
huobipro2 = ccxt.huobipro({
    'apiKey': '',
    'secret': '',
})

# 获取当天时间
year = datetime.date.today().year
month = datetime.date.today().month
day = datetime.date.today().day
# 调试用
# dest_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
# 设置标记时间，到23：59分59秒时暂停
dest_time = datetime.datetime(year=year,month=month,day=day,hour=23,minute=59,second=59)
end_buy_time = dest_time + datetime.timedelta(minutes=1)

# 监控的币种清单
# 总币种
coins = ["SOC","LOL","PAI","RUFF","DTA","TOP","YEE","EGT","OGO","TITAN","TNB","EM","SWFTC","UIP","CAN","MXC"]   
# api_1
coins1 = ["SOC","LOL","PAI","RUFF","DTA","TOP","YEE","EGT","OGO","TITAN"]                                       
# api_2
coins2 = ["TNB","EM","SWFTC","UIP","CAN","MXC","KCASH","UUU","NHBTC","HC"]


# 触发买入价格
bought_rate = 1.025
# 停止买入价格
stop_buy_rate = 1.07
# 触发卖出价格
sell_rate = 0.995
# 止盈价格
kill_earn_high_rise = 1.14
kill_earn_middle = 1.10
kill_earn_low_drop = 1.07


# 一个仓位多少U
base_money = 50
# 执行几次买入操作,PS买入过的币不会再买
buy_how_many_coin = 2

# 购买日志，放在同目录文件夹下的buglog.txt文件中
buylog = open("buylog.txt",'w')

# 币种的买入价格
buydict = {}

# trigger_price 控制所有标记点生成操作只执行一次,开始未生成标记点，因此为false
trigger_price = False
# 未成交的币种清单,初始值为所有币种
not_bought_coins = coins
# 已成交的币种清单
bought_coins = []
# 触发中间价格清单
touch_middle_sell_point_coins = []

print('目标时间：' + str(dest_time))
print('当前时间：' + str(datetime.datetime.now()))
try:
    while True:
        # 请求一次服务器价格
        time.sleep(0.01)

        # 标记时间为每日的23:59:59秒
        delta = dest_time - datetime.datetime.now()
        delta_end_buy_time = end_buy_time - datetime.datetime.now()
        # 到生成标记的时间
        if delta < datetime.timedelta(microseconds=1) and trigger_price == False:
            trigger_buy_price = {} # 买入标记点
            trigger_stop_buy = {} # 停止买入标记点
            trigger_sell_price = {} # 止损标记点
            trigger_kill_earn_middle = {}  # 止盈标记点 中间
            trigger_kill_earn_low = {}  # 止盈标记点 低位
            trigger_kill_earn_high = {} # 止盈标记点 高位

            print("买入、止损标记点已生成")
            for coin in coins:
                # 请求每个币现在的价格
                time.sleep(0.01)
                present_price = huobipro.fetch_ticker(coin + '/USDT')['last'] 
                trigger_buy_price[coin] = present_price*bought_rate
                trigger_stop_buy[coin] = present_price*stop_buy_rate
                trigger_sell_price[coin] = present_price*sell_rate
                trigger_kill_earn_middle[coin] = present_price*kill_earn_middle
                trigger_kill_earn_high[coin] = present_price*kill_earn_high_rise
                trigger_kill_earn_low[coin] = present_price*kill_earn_low_drop

            trigger_price = True # 生成标记点的操作只执行一次

            print('\n')
            print("持续监控中....")


    # 未到标记点生成时间，查询各币种价格，或者已经生成了标记点，监控买入卖出
        elif delta > datetime.timedelta(microseconds=1) or trigger_price == True:
            if not trigger_price:
                # 未生成标的价格
                for coin in coins:
                    present_name = coin+"_Last"
                    present_price = huobipro.fetch_ticker(coin + '/USDT')['last']
                    time.sleep(0.01)
                    
                # print('\n\n\n')
            else:
                # 已经生成了标记点，监控每个币种是否到达触发价格，达到标的价格的时候触发买入委托
                for coin in not_bought_coins:
                    if delta_end_buy_time < datetime.timedelta(microseconds=1):
                        
                        # 到每日的12:01如果还没买入就暂停买入
                        break

                    present_price = huobipro.fetch_ticker(coin + '/USDT')['last']
                    # 如果当前价格大于等于1.02的买入价格就触发买入
                    if present_price >= trigger_buy_price[coin] and buy_how_many_coin > 0:
                        # 写买入日志
                        buylog.write(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')+' ' +coin + ' '+ str(present_price)+'\n')
                        buydict[coin] = present_price # 每个币种的买入价格
                        pprint(buydict)

                        if coin in coins1:
                            huobipro = huobipro1
                        elif coin in coins2:
                            huobipro = huobipro2

                        # 买单参数 设置
                        order_symbol = coin + '/USDT' #循环监控币种 当前币种为coin在coins列表中
                        order_type = 'ioc' #达到触发价格
                        order_side = 'buy'
                        order_price = trigger_stop_buy[coin]
                        order_amount = base_money/order_price  # 订单交易额(USDT)为一个仓位
                        

                        # 买入订单下单
                        take_order = huobipro.create_order(symbol=order_symbol, type=order_type, price=order_price , side=order_side, amount=order_amount)
                        

                        pprint('达到2%触发价格，已买入: ' + coin + ' ' + str(order_amount) )
                        pprint('现价' + str(present_price))

                        # 买入就将买入币种减1
                        print('\n\n')
                        buy_how_many_coin = buy_how_many_coin - 1
                        bought_coins.append(coin)
                        not_bought_coins.remove(coin)

                # 卖出循环监控
                for coin in bought_coins:
                    present_price = huobipro.fetch_ticker(coin + '/USDT')['last']
                    # 如果买入了，结果回落导致当前价格小于等于止损价格就触发市价卖出止损
                    if present_price <= trigger_sell_price[coin]:

                        if coin in coins1:
                            huobipro = huobipro1
                        elif coin in coins2:
                            huobipro = huobipro2

                        # 卖单参数 设置
                        order_symbol = coin + '/USDT'
                        order_type = 'market'#市价卖出
                        order_side = 'sell'
                        order_amount = huobipro.fetch_balance()[coin]['total']  #读取当前币种有多少持仓，


                        # 判断有无持仓，有持仓才执行卖操作
                        if order_amount > 1:
                            take_order = huobipro.create_order(symbol=order_symbol, type=order_type, side=order_side,
                                                           amount=order_amount)
                            pprint(coin + ' ' + str(int(order_amount*present_price)) + ' usdt ' + '买入币出现回落止损，已清仓')
                            pprint('现价' + str(present_price))
                            print('\n\n')
                            bought_coins.remove(coin)
                            exit(0)
                        else:
                            print('没有持仓' + order_symbol)


                    # 如果到达中间止盈点，就卖出一半
                    if present_price >= trigger_kill_earn_middle[coin] and (coin not in touch_middle_sell_point_coins):

                        if coin in coins1:
                            huobipro = huobipro1
                        elif coin in coins2:
                            huobipro = huobipro2

                        order_symbol = coin + '/USDT'
                        order_type = 'limit'  # 限价卖出
                        order_side = 'sell'
                        order_price = trigger_kill_earn_middle[coin]
                        order_amount = huobipro.fetch_balance()[coin]['total']*0.5  # 读取当前币种有多少持仓，
                        # middle出一半
                        # 判断有无持仓，有持仓才执行卖操作
                        if order_amount > 1:
                            take_order = huobipro.create_order(symbol=order_symbol, type=order_type, price=order_price , side=order_side, amount=order_amount)
                            pprint(coin + ' ' + str(int(order_amount*present_price)) + ' usdt '+'已触发中间价格，卖出一半: ')
                            touch_middle_sell_point_coins.append(coin)
                        else:
                            print('没有持仓' + order_symbol)



                    # 如果到达止盈点high 就全卖出
                    # 卖单参数 设置
                    if present_price >= trigger_kill_earn_high[coin] and (coin in touch_middle_sell_point_coins):
                        
                        if coin in coins1:
                            huobipro = huobipro1
                        elif coin in coins2:
                            huobipro = huobipro2

                        order_symbol = coin + '/USDT'
                        order_type = 'limit'  # 限价卖出
                        order_side = 'sell'
                        order_price = trigger_kill_earn_high[coin]
                        order_amount = huobipro.fetch_balance()[coin]['total']  # 读取当前币种有多少持仓，

                        # 判断有无持仓，有持仓才执行卖操作
                        if order_amount > 1:
                            take_order = huobipro.create_order(symbol=order_symbol, type=order_type, price=order_price , side=order_side, amount=order_amount)
                            pprint(coin + ' ' + str(int(order_amount*present_price)) + ' usdt ' + '到达高止盈点，清仓: ')
                            pprint('现价' + str(present_price))
                            bought_coins.remove(coin)
                            touch_middle_sell_point_coins.remove(coin)
                            exit(0)
                        else:
                            print('没有持仓' + order_symbol)


                    # 如果涨到middle然后跌到low以下就清仓
                    if present_price <= trigger_kill_earn_low[coin] and (coin in touch_middle_sell_point_coins):
                        
                        if coin in coins1:
                            huobipro = huobipro1
                        elif coin in coins2:
                            huobipro = huobipro2

                        order_symbol = coin + '/USDT'
                        order_type = 'market'  # 市价卖出
                        order_side = 'sell'
                        order_amount = huobipro.fetch_balance()[coin]['total']  # 读取当前币种有多少持仓，

                        # 判断有无持仓，有持仓才执行卖操作
                        if order_amount > 1:
                            take_order = huobipro.create_order(symbol=order_symbol, type=order_type, side=order_side,
                                                           amount=order_amount)
                            pprint(coin + ' ' + str(int(order_amount*present_price)) + ' usdt ' + '到达低止盈点，清仓: ')
                            print('\n\n')
                            bought_coins.remove(coin)
                            touch_middle_sell_point_coins.remove(coin)
                            exit(0)
                        else:
                            print('没有持仓' + order_symbol)
except:
        print(traceback.format_exc())


