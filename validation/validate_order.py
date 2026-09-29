import MetaTrader5 as mt5
from config import SLIPPAGE, SYMBOL
from datetime import datetime, timezone
import math


def validate_order(order_type):
    account_info = mt5.account_info()

    if (not _pre_validation_checks(account_info)):
        return None

    symbol_info = mt5.symbol_info(SYMBOL)
    price = symbol_info.ask if order_type == mt5.ORDER_TYPE_BUY else symbol_info.bid

    if order_type == mt5.ORDER_TYPE_BUY:
        sl = price - 100
        tp = price + 100
    else:
        sl = price + 100
        tp = price - 100

    
    if (not _validate_tp_and_sl(price, tp, sl, symbol_info)):
        return None

    lot_size = _calculate_lot_size(price, sl, account_info, symbol_info)

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


def _validate_tp_and_sl(price, take_profit, stop_loss, symbol_info):
    minimum_distance = symbol_info.trade_stops_level * symbol_info.point
    return True


def _calculate_lot_size(price, stop_loss, account_info, symbol_info):
    risk_money = account_info.equity * 0.001
    loss_1_lot = abs(
        mt5.order_calc_profit(
            mt5.ORDER_TYPE_BUY,
            SYMBOL,
            1.0,
            price,
            stop_loss
        )
    )

    lot_size = risk_money / loss_1_lot

    step = symbol_info.volume_step

    return math.floor(lot_size / step) * step

def _pre_validation_checks(account_info):
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
