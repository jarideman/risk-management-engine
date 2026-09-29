import MetaTrader5 as mt5
from config import SLIPPAGE, SYMBOL
from datetime import datetime, timezone

def validate_order(order_type):
    if (not _pre_validation_checks()):
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


def _pre_validation_checks():
    account_info = mt5.account_info()

    if (not account_info.trade_allowed):
        return False

    if (account_info.margin_free < 200):
        return False
    
    open_positions = mt5.positions_total()

    if (open_positions > 10):
        return False

    daily_closed_pnl = _daily_closed_pnl()

    if (daily_closed_pnl < -300):
        return False

    floating_pnl = account_info.equity - account_info.balance
    daily_pnl  = floating_pnl + daily_closed_pnl

    if (daily_pnl  < -350):
        return False

    return True


def _daily_closed_pnl():
    tick = mt5.symbol_info_tick(SYMBOL)
    
    server_time = datetime.fromtimestamp(tick.time, tz=timezone.utc)
    start_of_day = server_time.replace(hour=0, minute=0, second=0, microsecond=0)
    
    deals = mt5.history_deals_get(start_of_day, server_time)

    pnl = 0.0

    for deal in deals:
        if deal.entry in (
            mt5.DEAL_ENTRY_OUT,
            mt5.DEAL_ENTRY_OUT_BY,
        ):
            pnl += deal.profit
            pnl += deal.swap
            pnl += deal.commission

    return pnl
