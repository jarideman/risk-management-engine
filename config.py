SLIPPAGE = 10
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
