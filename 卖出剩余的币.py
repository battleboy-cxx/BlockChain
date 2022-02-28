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
coin = 'PAI'

# 卖单参数 设置
order_symbol = coin + '/USDT'
order_type = 'market'  # 市价卖出
order_side = 'sell'
order_amount = huobipro.fetch_balance()[coin]['total']  # 读取当前币种有多少持仓，

# 只有有持仓才会去卖（清仓），防止出现无余额的卖单出现
if order_amount > 1:
    take_order = huobipro.create_order(symbol=order_symbol, type=order_type, side=order_side,
                                       amount=order_amount)
    pprint(coin + ' ' + str(int(order_amount))+' usdt ' + '已清仓')
    print('\n\n')
else:
    print('没有持仓')