import MetaTrader5 as mt5
import random
from validation.validate_order import validate_order


def run_pipeline():
    order_type = random.choice([
        mt5.ORDER_TYPE_BUY,
        mt5.ORDER_TYPE_SELL,
    ])
        
    request = validate_order(order_type)

    if request:
        place_order(request)
        print("Order placed successfully")
    else:
        print("Invalid order")

    pass


def place_order(order):
    result = mt5.order_send(order)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("order_send failed, retcode={}".format(result.retcode))

        mt5.shutdown()
        quit()
 
    print("Order send successful", result)
    pass
