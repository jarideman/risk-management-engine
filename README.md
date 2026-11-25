# Setup

### 1. Create virtual environment
```bash
python -m venv venv
```

### 2. Activate virtual environment
**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
**Windows:**
```bash
copy .env.example .env
```

**Linux / macOS:**
```bash
cp .env.example .env
```

Fill/update the variables in `.env`.

### 5. Run the application
```bash
python main.py
```


## Core
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
- [x] Check sl risk of positions
- [x] Reject the trade if any limit is violated
