import MetaTrader5 as mt5
from config import SLIPPAGE, SYMBOL


def validate_order(order_type):
    if (not pre_validation_checks()):
        return None

    lot_size = 0.01

    tick = mt5.symbol_info_tick(SYMBOL)

    price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid

    if order_type == mt5.ORDER_TYPE_BUY:
        sl = price - 100
        tp = price + 100
    else:
        sl = price + 100
        tp = price - 100

    return {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": lot_size,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": SLIPPAGE,
        "magic": 123456,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }


def pre_validation_checks():
    # Check whether trading is currently allowed

    # Check maximum number of open positions

    # Check drawdown limit

    # Check daily loss limit

    return True