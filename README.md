## Setup
- [x] Setup connection
- [x] Validations whats wrong when order exceeds rules
- [x] All input values manageable in config

## Pre trade validation checks
- [x] Check whether trading is currently allowed
- [x] Check margin requirements with available free margin
- [x] Check maximum total margin exposure
- [x] Check maximum number of open positions
- [x] Check daily loss limit
- [x] Check drawdown limit

## Pre trade risk checks
- [x] Calculate position size
- [x] Check maximum risk per trade, e.g. 0.5% of equity
- [x] Check whether the requested stop-loss and take-profit are valid
- [x] Check maximum exposure per symbol
- [x] Check correlation/exposure across related symbols
- [ ] Check sl risk of positions
- [ ] Reject the trade if any limit is violated