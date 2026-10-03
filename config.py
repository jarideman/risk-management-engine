SLIPPAGE = 10
RISK_PERCENTAGE = 0.001
FREE_MARGIN_THRESHOLD = 200
MAX_POSITIONS = 10
MARGIN_EXPOSURE_THRESHOLD = 0.5
MAX_DAILY_LOSS = -300
MAX_DAILY_PNL = -350

EXPOSURE_GROUPS = {
    "crypto": [
        "BTCUSD",
        "ETHUSD",
        "SOLUSD",
        "XRPUSD",
    ],

    "us_stocks": [
        "AAPL",
        "MSFT",
        "NVDA",
        "TSLA",
    ],

    "indices": [
        "US30",
        "US500",
        "USTEC",
        "GER40",
    ],

    "forex": [
        "EURUSD",
        "GBPUSD",
        "USDJPY",
        "AUDUSD",
    ],
}
MAX_GROUP_EXPOSURE = {
    "crypto": 1.00,
    "us_stocks": 2.00,
    "indices": 1.00,
    "forex": 2.00,
}
MAX_SYMBOL_EXPOSURE = {
    "crypto": 0.50,
    "us_stocks": 0.90,
    "indices": 0.50,
    "forex": 0.90,
}
