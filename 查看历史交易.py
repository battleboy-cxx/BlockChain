import ccxt
import pprint

# 查看交易所,api设置,改成你的API
huobipro = ccxt.huobipro({
    'apiKey': '',
    'secret': '',
})

history_trade = huobipro.fetch_my_trades(since=1618848000)

for i in range(0,10):
    history_trade_symbol = huobipro.fetch_my_trades()[i]['symbol']
    history_trade_price = huobipro.fetch_my_trades()[i]['price']
    history_trade_side = huobipro.fetch_my_trades()[i]['side']
    history_trade_amount = huobipro.fetch_my_trades()[i]['amount']
    print(history_trade_symbol)
    print(history_trade_price)
    print(history_trade_amount)
    print(history_trade_side)
    print(history_trade_price*history_trade_amount)
    print('\n')