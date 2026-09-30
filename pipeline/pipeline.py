import MetaTrader5 as mt5
import random
from validation.validate_order import validate_order
from connection.mt5_connection import deinit_mt5


def run_pipeline():
    symbol = "BTCUSD"

    order_type = random.choice([
        mt5.ORDER_TYPE_BUY,
        mt5.ORDER_TYPE_SELL,
    ])

    if not mt5.symbol_select(symbol, True):
        print('Symbol not found')
        deinit_mt5()
        return False
        
    request = validate_order(order_type, symbol)

    if request:
        _place_order(request)
    else:
        print("Order does not meet requirements")

    pass


def _place_order(order):
    result = mt5.order_send(order)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("order_send failed, retcode={}".format(result.retcode))

        mt5.shutdown()
        quit()
 
    print("Order send successful", result)
    pass
