import ccxt
import os
import sys
import time
import pandas as pd

# coding=utf-8



huobi = ccxt.huobipro({
    'apiKey': '填入自己的apiKey',
    'secret': '同上secret',
})

print(huobi.id, huobi.load_markets())
coins = ["BTC","ETH"]


exchange = ccxt.huobipro()
markets = exchange.load_markets()
for coin in coins:
    symbol = coin+'/USDT'
    kldata = exchange.fetch_ohlcv(symbol=symbol, timeframe='1h',since=1633017600000 )
    df_kl = pd.DataFrame(kldata, columns=['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df_kl['DateTime'] = df_kl['DateTime']/1000
    df_kl.to_csv('D:\\Cryptocoin\\' + coin + '.csv', index=0)
