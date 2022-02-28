#!/usr/local/bin/python3.8
# encoding: utf-8
import sys
import ccxt
import time
from pprint import pprint
import os
import logging
import datetime



# 查看交易所,api设置,改成你的API
huobipro = ccxt.huobipro({
    # 'proxies': {
    #         'http':'socks5h://127.0.0.1:7891',
    #         'https':'socks5h://127.0.0.1:7891'
    #         },
    'apiKey': '',
    'secret': '',
})




# # 调试用
dest_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
# # 触发买入价格
# bought_rate = 1.008
# # 停止买入价格
# stop_buy_rate = 1.018
# # 触发卖出价格
# sell_rate = 0.998




year = datetime.date.today().year
month = datetime.date.today().month
day = datetime.date.today().day

# # 参数设置，到23：59分59秒时暂停
# dest_time = datetime.datetime(year=year,month=month,day=day,hour=23,minute=59,second=58)
# end_buy_time = dest_time + datetime.timedelta(minutes=2)
end_buy_time = dest_time + datetime.timedelta(minutes=1)
# 监控的币种清单
coins = ["SOC","LOL","PAI","RUFF","DTA","TOP","YEE","EGT","OGO","TITAN","TNB","EM","SWFTC","UIP","CAN","MXC"] # 0点币
coins1 = ["SOC","LOL","PAI","RUFF","DTA","TOP","YEE","EGT","OGO","TITAN"]
coins2 = ["TNB","EM","SWFTC","UIP","CAN","MXC"]



#
# # 触发买入价格
# bought_rate = 1.02
# # 停止买入价格
# stop_buy_rate = 1.055
# # 触发卖出价格
# sell_rate = 0.998
# 止盈价格
# kill_earn_rate_high = 1.18
# kill_earn_middle = 1.11
# kill_earn_low_drop = 1.08

# 触发买入价格
bought_rate = 1.025
# 停止买入价格
stop_buy_rate = 1.05
# 触发卖出价格
sell_rate = 0.98 
kill_earn_rate_high = 1.011
kill_earn_middle = 1.085
kill_earn_low_drop = 1.06

# 一个仓位多少U
base_money = 10
# 执行几次买入操作,PS买入过的币不会再买
buy_how_many_coin = 1

# 购买日志，放在同目录文件夹下的buglog.txt文件中
buylog = open("buylog.txt",'w')
# 币种的买入价格
buydict = {}
emptylist = []

# generate_trigger_price 控制所有标记点生成操作只执行一次
generate_trigger_price = False
# 未成交的币种清单
not_bought_coins = coins
# 已成交的币种清单
bought_coins = []
# 触发中间价格清单
touch_10_coins = []

print('目标时间：' + str(dest_time))
print('当前时间：' + str(datetime.datetime.now()))
while True:
    # 每隔一秒请求一次服务器价格
    time.sleep(0.01)

    # 标记时间为每日的23:59:59秒
    delta = dest_time - datetime.datetime.now()
    delta_end_buy_time = end_buy_time - datetime.datetime.now()
    # 到生成标记的时间
    if delta < datetime.timedelta(microseconds=1) and generate_trigger_price == False:
        trigger_buy_price = {} # 买入标记点
        trigger_stop_buy = {} # 停止买入标记点
        trigger_sell_price = {} # 卖出标记点
        trigger_kill_earn_low = {}  # 止盈标记点 10%出一半仓位
        trigger_kill_earn_low_drop = {}  # 止盈标记点 如果涨到12再回落到7%出全仓
        trigger_kill_earn_high = {} # 止盈标记点  18%出全仓

        print("买入、止损标记点已生成")
        for coin in coins:
            present_name = coin+"_Last"
            present_price = huobipro.fetch_ticker(coin + '/USDT')['last'] #爬取每个币现在的价格
            time.sleep(0.01)
            trigger_buy_price[coin] = present_price*bought_rate
            trigger_stop_buy[coin] = present_price*stop_buy_rate
            trigger_sell_price[coin] = present_price*sell_rate
            trigger_kill_earn_low[coin] = present_price*kill_earn_middle
            trigger_kill_earn_high[coin] = present_price*kill_earn_rate_high
            trigger_kill_earn_low_drop[coin] = present_price*kill_earn_low_drop

        pprint('停止买入价格：')
        pprint(trigger_stop_buy)
        pprint('卖出价格：')
        pprint(trigger_sell_price)
        # pprint('止盈价格：')
        # pprint('middle:' + kill_earn_middle)
        # pprint('high:' + trigger_kill_earn_high)
        # pprint('回落止损:' + trigger_kill_earn_low_drop)


        generate_trigger_price = True # 生成标记点的操作只执行一次

        print('\n\n\n')
        print("持续监控中....")


    # 未到标记点生成时间，查询各币种价格，或者已经生成了标记点，监控买入卖出
    elif delta > datetime.timedelta(microseconds=1) or generate_trigger_price == True:
        if not generate_trigger_price:
            # 未生成标的价格
            for coin in coins:
                present_name = coin+"_Last"
                present_price = huobipro.fetch_ticker(coin + '/USDT')['last']
                time.sleep(0.01)
                print(present_name+': \t最新价格:'+str(present_price) + '\n\t\t 买入价格'+ str("{:.5f}".format(present_price*1.02)) + '\n\t\t止损价格'+ str("{:.5f}".format(present_price*0.98)))
            print('\n\n\n')
        else:
            # 已经生成了标记点，监控每个币种是否到达触发价格，达到标的价格的时候触发买入委托
            for coin in not_bought_coins:
                if delta_end_buy_time < datetime.timedelta(microseconds=1) and bought_coins == emptylist:

                    dest_time = dest_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
                    end_buy_time = dest_time + datetime.timedelta(minutes=1)
                    print("到点，开始下一轮检测")
                    print("买入、止损标记点已生成")
                    for coin in not_bought_coins:
                        present_name = coin + "_Last"
                        present_price = huobipro.fetch_ticker(coin + '/USDT')['last']  # 爬取每个币现在的价格
                        time.sleep(0.01)
                        trigger_buy_price[coin] = present_price * bought_rate
                        trigger_stop_buy[coin] = present_price * stop_buy_rate
                        trigger_sell_price[coin] = present_price * sell_rate
                        trigger_kill_earn_low[coin] = present_price * kill_earn_middle
                        trigger_kill_earn_high[coin] = present_price * kill_earn_rate_high
                        trigger_kill_earn_low_drop[coin] = present_price * kill_earn_low_drop

                    pprint('停止买入价格：')
                    pprint(trigger_stop_buy)
                    pprint('卖出价格：')
                    pprint(trigger_sell_price)
                    break

                present_price = huobipro.fetch_ticker(coin + '/USDT')['last']
                # 如果当前价格大于等于1.02的买入价格就触发买入
                if present_price >= trigger_buy_price[coin] and buy_how_many_coin > 0:
                    # 写买入日志
                    print('write')
                    buylog.write(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')+' ' +coin + ' '+ str(present_price)+'\n')
                    buydict[coin] = present_price # 每个币种的买入价格
                    pprint(buydict)

                    if coin in coins1:
                        huobipro = ccxt.huobipro({
                            'apiKey': '',
                            'secret': '',
                        })
                    elif coin in coins2:
                        huobipro = ccxt.huobipro({
                            'apiKey': '',
                            'secret': '',
                        })


                    # 买单参数 设置
                    order_symbol = coin + '/USDT' #循环监控币种 当前币种为coin在coins列表中
                    order_type = 'ioc' #达到触发价格
                    order_side = 'buy'
                    order_price = trigger_stop_buy[coin]
                    order_amount = base_money/order_price  # 订单交易额(USDT)为一个仓位
                    # params = {
                    #     'timeInForce': 'gtc'
                    # }

                    # 买入订单下单
                    take_order = huobipro.create_order(symbol=order_symbol, type=order_type, price=order_price , side=order_side, amount=order_amount)
                    pprint(huobipro.fetch_order(id=take_order['id']))



                    pprint('达到2%触发价格，已买入: ' + coin + ' ' + str(order_amount) )
                    pprint('现价' + str(present_price))
                    # pprint('buy_order:' + str(take_order['status']))
                    # 买入就将买入币种减1
                    print('\n\n')
                    buy_how_many_coin = buy_how_many_coin - 1
                    bought_coins.append(coin)
                    not_bought_coins.remove(coin)

            # 卖出循环监控
            for coin in bought_coins:
                present_price = huobipro.fetch_ticker(coin + '/USDT')['last']
                # 如果买入了，结果回落导致当前价格小于等于止损价格(0.995)就触发卖出止损
                if present_price <= trigger_sell_price[coin]:

                    if coin in coins1:
                        huobipro = ccxt.huobipro({
                            'apiKey': '',
                            'secret': '',
                        })
                    elif coin in coins2:
                        huobipro = ccxt.huobipro({
                            'apiKey': '',
                            'secret': '',
                        })

                    # 卖单参数 设置
                    order_symbol = coin + '/USDT'
                    order_type = 'market'#市价卖出
                    order_side = 'sell'
                    order_amount = huobipro.fetch_balance()[coin]['total']  #读取当前币种有多少持仓，


                    # 只有有持仓才会去卖（清仓），防止出现无余额的卖单出现
                    if order_amount > 1:
                        take_order = huobipro.create_order(symbol=order_symbol, type=order_type, side=order_side,
                                                           amount=order_amount)
                        pprint(coin + ' ' + str(int(order_amount*present_price)) + ' usdt ' + '买入币出现回落，已清仓')
                        print('\n\n')
                        bought_coins.remove(coin)
                        not_bought_coins.append(coin)
                    else:
                        print('没有持仓' + order_symbol)


                # 如果到达中间止盈点，就卖出一半
                # 卖单参数 设置
                if present_price >= trigger_kill_earn_low[coin] and (coin not in touch_10_coins):
                    if coin in coins1:
                        huobipro = ccxt.huobipro({
                            'apiKey': '',
                            'secret': '',
                        })
                    elif coin in coins2:
                        huobipro = ccxt.huobipro({
                            'apiKey': '',
                            'secret': '',
                        })

                    order_symbol = coin + '/USDT'
                    order_type = 'market'  # 市价卖出
                    order_side = 'sell'
                    order_amount = huobipro.fetch_balance()[coin]['total']*0.5  # 读取当前币种有多少持仓，
                    # 12%出一半
                    # 只有有持仓才会去卖（清仓），防止出现无余额的卖单出现
                    if order_amount > 1:
                        take_order = huobipro.create_order(symbol=order_symbol, type=order_type, side=order_side,
                                                           amount=order_amount)
                        pprint(coin + ' ' + str(int(order_amount*present_price)) + ' usdt '+'已触发中间价格，卖出一半: ')
                        touch_10_coins.append(coin)

                    else:
                        print('没有持仓' + order_symbol)



                # 如果到达止盈点18% 就全卖出
                # 卖单参数 设置
                if present_price >= trigger_kill_earn_high[coin] and (coin in touch_10_coins):
                    if coin in coins1:
                        huobipro = ccxt.huobipro({
                            'apiKey': '',
                            'secret': '',
                        })
                    elif coin in coins2:
                        huobipro = ccxt.huobipro({
                            'apiKey': '',
                            'secret': '',
                        })

                    order_symbol = coin + '/USDT'
                    order_type = 'market'  # 市价卖出
                    order_side = 'sell'
                    order_amount = huobipro.fetch_balance()[coin]['total']  # 读取当前币种有多少持仓，

                    # 只有有持仓才会去卖（清仓），防止出现无余额的卖单出现
                    if order_amount > 1:
                        take_order = huobipro.create_order(symbol=order_symbol, type=order_type, side=order_side,
                                                           amount=order_amount)
                        pprint(coin + ' ' + str(int(order_amount*present_price)) + ' usdt ' + '到达20%止盈点，清仓: ')
                        bought_coins.remove(coin)
                        touch_10_coins.remove(coin)
                        not_bought_coins.append(coin)
                    else:
                        print('没有持仓' + order_symbol)


                # 如果涨到12之后又回落到6%以下就清仓
                if present_price <= trigger_kill_earn_low_drop[coin] and (coin in touch_10_coins):
                    if coin in coins1:
                        huobipro = ccxt.huobipro({
                            'apiKey': '',
                            'secret': '',
                        })
                    elif coin in coins2:
                        huobipro = ccxt.huobipro({
                            'apiKey': '',
                            'secret': '',
                        })

                    order_symbol = coin + '/USDT'
                    order_type = 'market'  # 市价卖出
                    order_side = 'sell'
                    order_amount = huobipro.fetch_balance()[coin]['total']  # 读取当前币种有多少持仓，

                    # 只有有持仓才会去卖（清仓），防止出现无余额的卖单出现
                    if order_amount > 1:
                        take_order = huobipro.create_order(symbol=order_symbol, type=order_type, side=order_side,
                                                           amount=order_amount)
                        pprint(coin + ' ' + str(int(order_amount*present_price)) + ' usdt ' + '又跌到6%，清仓: ')
                        print('\n\n')
                        bought_coins.remove(coin)
                        touch_10_coins.remove(coin)
                        not_bought_coins.append(coin)
                    else:
                        print('没有持仓' + order_symbol)



