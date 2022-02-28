import ccxt
import time
from pprint import pprint
import os
import logging
import datetime

huobipro = ccxt.huobipro({
    'apiKey': '',
    'secret': '',
})

balance = huobipro.fetch_balance()['total']['USDT']
print(balance)
