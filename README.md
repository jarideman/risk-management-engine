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
- [x] Check whether the requested stop-loss and take-profit are valid
- [ ] Check maximum total portfolio exposure
- [ ] Check maximum exposure per symbol
- [ ] Check correlation/exposure across related symbols
- [x] Reject the trade if any limit is violated