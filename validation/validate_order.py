import MetaTrader5 as mt5
from config import (
    MAX_DAILY_LOSS,
    MAX_POSITIONS,
    MAX_DAILY_PNL,
    MARGIN_EXPOSURE_THRESHOLD,
    RISK_PERCENTAGE,
    FREE_MARGIN_THRESHOLD,
    SLIPPAGE,
    EXPOSURE_GROUPS,
    MAX_SYMBOL_EXPOSURE,
    MAX_GROUP_EXPOSURE,
    SL_RISK_PERCENTAGE
)
from datetime import datetime, timezone
import math


def validate_order(order):
    if (order.get("order_type") is None or
        not order.get("symbol") or
        not order.get("lot_size") or
        not order.get("entry") or
        not order.get("sl") or
        not order.get("tp")):
        print('Missing required parameters')

        return None

    exposure_group = _get_exposure_group(order["symbol"])

    if (not exposure_group):
        print(f'Symbol: {order["symbol"]} not in exposure groups')

        return None


    global SYMBOL
    SYMBOL = order["symbol"]


    account_info = mt5.account_info()

    if (not _pre_validation_checks(account_info=account_info)):
        return None


    symbol_info = mt5.symbol_info(SYMBOL)

    if (order["lot_size"] < symbol_info.point):
        print('Lot size is to small')

        return None


    if (not _validate_tp_and_sl(entry=order["entry"], take_profit=order["tp"], stop_loss=order["sl"], order_type=order["order_type"], symbol_info=symbol_info)):
        return None


    max_lot_size = _calculate_max_lot_size(entry=order["entry"], stop_loss=order["sl"], order_type=order["order_type"], account_info=account_info, symbol_info=symbol_info)

    if (order["lot_size"] > max_lot_size):
        print('Lot size exceeds maximum lot size')

        return None


    valid_symbol_exposure = _check_symbol_exposure(exposure_group=exposure_group, lot_size=order["lot_size"], order_type=order["order_type"])

    if (not valid_symbol_exposure):
        print(f'Placing order would exceed maximum exposure for: {SYMBOL}')

        return None


    valid_exposure = _check_positions_group_exposure(exposure_group=exposure_group, lot_size=order["lot_size"], order_type=order["order_type"])

    if (not valid_exposure):
        print(f'Placing order would exceed maximum exposure for: {exposure_group}')

        return None


    valid_sl_risk = _check_sl_risk(lot_size=order["lot_size"], entry=order["entry"], stop_loss=order["sl"], order_type=order["order_type"], account_info=account_info)

    if (not valid_sl_risk):
        print("Placing order would exceed maximum SL risk")

        return None

    return {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": order["lot_size"],
        "type": order["order_type"],
        "price": order["entry"],
        "sl": order["sl"],
        "tp": order["tp"],
        "deviation": SLIPPAGE,
        "magic": 123456,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }


def _get_exposure_group(symbol):
    for group, symbols in EXPOSURE_GROUPS.items():
        if symbol in symbols:
            return group

    return None


def _check_symbol_exposure(exposure_group, lot_size, order_type):
    max_symbol_exposure = MAX_SYMBOL_EXPOSURE[exposure_group]

    symbol_positions = mt5.positions_get(symbol=SYMBOL)

    if (not symbol_positions):
        return True


    exposure = 0

    if order_type == mt5.POSITION_TYPE_BUY:
        exposure = lot_size
    elif order_type == mt5.POSITION_TYPE_SELL:
        exposure = -lot_size


    for position in symbol_positions:
        if position.type == mt5.POSITION_TYPE_BUY:
            exposure += position.volume
        elif position.type == mt5.POSITION_TYPE_SELL:
            exposure -= position.volume


    return abs(exposure) < max_symbol_exposure


def _check_positions_group_exposure(exposure_group, lot_size, order_type):
    positions = mt5.positions_get()

    if (not positions):
        return True


    exposure = {}

    if order_type == mt5.POSITION_TYPE_BUY:
        exposure = {
            exposure_group: lot_size
        }   
    elif order_type == mt5.POSITION_TYPE_SELL:
        exposure = {
            exposure_group: -lot_size
        }


    for position in positions:
        group = _get_exposure_group(position.symbol)

        if group not in exposure:
            exposure[group] = 0

        if position.type == mt5.POSITION_TYPE_BUY:
            exposure[group] += position.volume
        elif position.type == mt5.POSITION_TYPE_SELL:
            exposure[group] -= position.volume


    return abs(exposure[exposure_group]) < MAX_GROUP_EXPOSURE[exposure_group]

def _check_sl_risk(lot_size, entry, stop_loss, order_type, account_info):
    max_loss = mt5.order_calc_profit(
        order_type,
        SYMBOL,
        lot_size,
        entry,
        stop_loss
    )

    positions = mt5.positions_get()
    positions_max_loss = 0

    for position in positions:
        if position.sl == 0:
            continue

        loss = mt5.order_calc_profit(
            position.type,
            position.symbol,
            position.volume,
            position.price_open,
            position.sl
        )

        positions_max_loss += abs(loss)


    max_loss_total = positions_max_loss + abs(max_loss)
    sl_risk_money = account_info.balance * SL_RISK_PERCENTAGE

    return max_loss_total < sl_risk_money


def _validate_tp_and_sl(entry, take_profit, stop_loss, order_type, symbol_info):
    minimum_distance = symbol_info.trade_stops_level * symbol_info.point

    if order_type == mt5.ORDER_TYPE_BUY:
        if entry - stop_loss < minimum_distance:
            print('Stop loss too close to entry')
        
            return False

        if take_profit - entry < minimum_distance:
            print('Take profit too close to entry')

            return False

    elif order_type == mt5.ORDER_TYPE_SELL:
        if stop_loss - entry < minimum_distance:
            print('Stop loss too close to entry')

            return False

        if entry - take_profit < minimum_distance:
            print('Take profit too close to entry')

            return False

    return True


def _calculate_max_lot_size(entry, stop_loss, order_type, account_info, symbol_info):
    risk_money = account_info.balance * RISK_PERCENTAGE
    loss_1_lot = abs(
        mt5.order_calc_profit(
            order_type,
            SYMBOL,
            1.0,
            entry,
            stop_loss
        )
    )

    lot_size = risk_money / loss_1_lot
    step = symbol_info.volume_step

    return math.floor(lot_size / step) * step


def _pre_validation_checks(account_info):
    if (not account_info.trade_allowed):
        print('Trading not allowed')

        return False


    if (account_info.margin_free < FREE_MARGIN_THRESHOLD):
        print('Not enough margin free')

        return False


    margin_exposure = account_info.margin / account_info.equity

    if (margin_exposure > MARGIN_EXPOSURE_THRESHOLD):
        print('To much margin exposure')

        return None

    
    open_positions = mt5.positions_total()

    if (open_positions > MAX_POSITIONS):
        print('To much open positions')

        return False


    daily_closed_pnl = _daily_closed_pnl()

    if (daily_closed_pnl < MAX_DAILY_LOSS):
        print('To much daily loss closed')

        return False


    floating_pnl = account_info.equity - account_info.balance
    daily_pnl  = floating_pnl + daily_closed_pnl

    if (daily_pnl  < MAX_DAILY_PNL):
        print('To much daily floatin and pnl loss')

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
