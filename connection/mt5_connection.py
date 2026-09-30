import MetaTrader5 as mt5


def init_mt5():
    if not mt5.initialize():
        print('MT5 initialization failed')
        return False

    print('MT5 initialization successful')
    return True


def deinit_mt5():
    mt5.shutdown()
    return
