## Setup
- [x] Setup connection

## Pre trade validation checks
- [x] Check whether trading is currently allowed
- [x] Check margin requirements with available free margin
- [x] Check maximum number of open positions
- [x] Check daily loss limit
- [x] Check drawdown limit

## Pre trade risk checks
- [x] Calculate position size
- [x] Check maximum risk per trade, e.g. 0.5% of equity
- [x] Check whether the requested stop-loss and take-profit are valid
- [X] Check maximum exposure per symbol
- [ ] Check maximum total portfolio exposure
- [ ] Check correlation/exposure across related symbols
- [ ] Reject the trade if any limit is violated