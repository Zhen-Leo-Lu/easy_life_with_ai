# Financial Market Update

A module for fetching and displaying financial market data.

## Features

- **Multiple Date Ranges**: 1 day, 1 week, 1 month, 3 months, 1 year
- **Asset Classes**: Stocks, Bonds, Commodities, Crypto, Forex
- **Regions**: US, Europe, Asia-Pacific, Global
- **Sector Performance**: Technology, Healthcare, Energy, etc.
- **Top Movers**: Best and worst performers

## Usage

```python
from financial_market import generate_market_report

# Generate report with defaults (US Stocks, last week)
report = generate_market_report()

# Customize
report = generate_market_report(
    date_range="1m",      # 1d, 1w, 1m, 3m, 1y
    asset_class="Crypto", # Stocks, Bonds, Commodities, Crypto, Forex
    region="Global"       # US, Europe, Asia-Pacific, Global
)

print(report)
```

## Data Source

Uses [yfinance](https://github.com/ranaroussi/yfinance) to fetch data from Yahoo Finance.

## Requirements

```
yfinance>=0.2.0
```
