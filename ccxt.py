import ccxt
import time
from pprint import pprint
import os
import logging
import datetime

#查看交易所
huobipro = ccxt.huobipro({
    'apiKey': '',
    'secret': '',
})

# pprint(huobipro.fetch_balance()['OGO'])

order_symbol = 'OGO/USDT'
order_type = 'limit'
order_side = 'buy'
order_amount = 1000
order_price = 0.018

dest_time = datetime.datetime(year=2021,month=4,day=10,hour=23,minute=59,second=50)


print(dest_time)
print(datetime.datetime.now())
while True:
    delta = dest_time - datetime.datetime.now()
    if delta < datetime.timedelta(microseconds=1):
        print("haaahahah")
        break
    time.sleep(0.2)
    OGO_Last = huobipro.fetch_ticker(order_symbol)['last']
    print('OGO 最新价格:'+str(OGO_Last) + '   OGO 买入价格'+ str(OGO_Last*1.02))

logging.info('OGO 最新价格:'+str(OGO_Last) + ' OGO 买入价格'+ str(OGO_Last*1.02))
# take_order = huobipro.create_order(order_symbol,order_type,order_side,order_amount,order_price)













# 获取比特币价格
# symbol = "BTC/USD"
# BTCticker = bitstamp.fetch_ticker(symbol)
# print(BTCticker)

# 最新价格
# BTCsymbol = BTCticker['symbol']
# bid_price = BTCticker['bid']
# datetime = BTCticker['datetime']
# print("交易对：",BTCsymbol)
# print("最新价格：",bid_price)
# print("时间：",datetime)