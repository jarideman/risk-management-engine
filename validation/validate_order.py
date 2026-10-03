import MetaTrader5 as mt5
from config import MAX_DAILY_LOSS, MAX_POSITIONS, MAX_DAILY_PNL, MARGIN_EXPOSURE_THRESHOLD, RISK_PERCENTAGE, FREE_MARGIN_THRESHOLD, SLIPPAGE, EXPOSURE_GROUPS, MAX_GROUP_EXPOSURE
from datetime import datetime, timezone
import math


def validate_order(order_type, symbol, lot_size, entry, sl, tp):
    exposure_group = _get_exposure_group(symbol)

    if (not exposure_group):
        print(f'Symbol: {symbol} not in exposure groups')

        return None


    global SYMBOL
    SYMBOL = symbol


    account_info = mt5.account_info()

    if (not _pre_validation_checks(account_info=account_info)):
        return None


    symbol_info = mt5.symbol_info(SYMBOL)

    if (lot_size < symbol_info.point):
        print('Lot size is to small')

        return None


    if (not _validate_tp_and_sl(entry=entry, take_profit=tp, stop_loss=sl, order_type=order_type, symbol_info=symbol_info)):
        return None


    max_lot_size = _calculate_max_lot_size(entry=entry, stop_loss=sl, account_info=account_info, symbol_info=symbol_info)

    if (lot_size > max_lot_size):
        print('Lot size exceeds maximum lot size')

        return None

    # Check maximum exposure per symbol -> with incoming order, check if exposure exceeds max exposure for symbol
    valid_symbol_exposure = _check_positions_exposure(symbol)

    if (not valid_symbol_exposure):
        print(f'Placing order would exceed maximum exposure for: {symbol}')

        return None

    # Check correlation/exposure across related symbols -> with incoming order, check if exposure exceeds max exposure for group of symbols
    valid_exposure = _check_positions_exposure()

    if (not valid_exposure):
        print(f'Placing order would exceed maximum exposure for: {exposure_group}')

        return None

    # Check sl risk of positions -> with incoming order, check if sl risk of positions exceeds max risk percentage
    valid_sl_risk = _check_sl_risk(symbol, lot_size, sl)

    if (not valid_sl_risk):
        print("Placing order would exceed maximum SL risk")

        return None

    return {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": lot_size,
        "type": order_type,
        "price": entry,
        "sl": sl,
        "tp": tp,
        "deviation": SLIPPAGE,
        "magic": 123456,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }


def _get_exposure_group(symbol):
    for group, symbols in EXPOSURE_GROUPS.items():
        if symbol in symbols:
            return group

    return None


def _check_positions_exposure():
    positions = mt5.positions_get()

    for position in positions:
        print(position)

    result = {}

    for group, symbols in EXPOSURE_GROUPS.items():
        result[group] = sum(
            p.volume # change to exposure
            for p in positions
            if p.symbol in symbols
        )

    print(result)
    return False


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


def _calculate_max_lot_size(entry, stop_loss, account_info, symbol_info):
    risk_money = account_info.equity * RISK_PERCENTAGE
    loss_1_lot = abs(
        mt5.order_calc_profit(
            mt5.ORDER_TYPE_BUY,
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
