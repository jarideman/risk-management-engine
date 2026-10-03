import MetaTrader5 as mt5
import random
from validation.validate_order import validate_order
from connection.mt5_connection import deinit_mt5


def run_pipeline():
    symbol = "BTCUSD"
    lot_size = 0.01
    order_type = random.choice([
        mt5.ORDER_TYPE_BUY,
        mt5.ORDER_TYPE_SELL,
    ])

    if not mt5.symbol_select(symbol, True):
        print(f'Symbol: {symbol} not found')

        deinit_mt5()
        
        return False

    symbol_info = mt5.symbol_info(symbol)

    entry = symbol_info.ask if order_type == mt5.ORDER_TYPE_BUY else symbol_info.bid

    if order_type == mt5.ORDER_TYPE_BUY:
        sl = entry - 100
        tp = entry + 100
    else:
        sl = entry + 100
        tp = entry - 100

    order = {
        "order_type": order_type,
        "symbol": symbol,
        "lot_size": lot_size,
        "entry": entry,
        "sl": sl,
        "tp": tp,
    }

    request = validate_order(order=order)

    if request:
        _place_order(request)
    else:
        print("Order does not meet requirements")

    pass


def _place_order(order: dict):
    result = mt5.order_send(order)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"order_send failed, retcode={result.retcode}")

        mt5.shutdown()
        quit()
 
    print("Order send successful", result)
    pass
