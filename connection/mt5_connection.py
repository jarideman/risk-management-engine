import MetaTrader5 as mt5
from config import SYMBOL

def init_mt5():
    if not mt5.initialize():
        print('MT5 initialization failed')
        return False

    if not mt5.symbol_select(SYMBOL, True):
        print('Symbol not found')
        deinit_mt5()
        return False

    print('MT5 initialization successful')
    return True

def deinit_mt5():
    mt5.shutdown()
    return
