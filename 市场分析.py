import ccxt
import pprint

# 查看交易所,api设置,改成你的API
huobipro = ccxt.huobipro({
    'apiKey': '',
    'secret': '',
})

ticker = huobipro.fetch_ticker('EM/USDT')

pprint(ticker)

