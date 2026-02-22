#!/usr/bin/env python3
"""
Financial Market Update Module
Fetches market data using yfinance and generates summaries.
"""

import yfinance as yf
from datetime import datetime, timedelta
from typing import Optional

# Market indices by region
INDICES = {
    "US": {
        "^GSPC": "S&P 500",
        "^IXIC": "Nasdaq",
        "^DJI": "Dow Jones",
        "^VIX": "VIX",
    },
    "Europe": {
        "^STOXX50E": "Euro Stoxx 50",
        "^FTSE": "FTSE 100",
        "^GDAXI": "DAX",
        "^FCHI": "CAC 40",
    },
    "Asia-Pacific": {
        "^N225": "Nikkei 225",
        "^HSI": "Hang Seng",
        "000001.SS": "Shanghai Composite",
        "^AXJO": "ASX 200",
    },
    "Global": {
        "^GSPC": "S&P 500",
        "^STOXX50E": "Euro Stoxx 50",
        "^N225": "Nikkei 225",
        "^VIX": "VIX",
    },
}

# Sector ETFs (US focused)
SECTOR_ETFS = {
    "XLK": "Technology",
    "XLF": "Financials",
    "XLV": "Healthcare",
    "XLE": "Energy",
    "XLY": "Consumer Disc.",
    "XLP": "Consumer Staples",
    "XLI": "Industrials",
    "XLB": "Materials",
    "XLU": "Utilities",
    "XLRE": "Real Estate",
}

# Asset class tickers
ASSET_CLASSES = {
    "Stocks": {
        "indices": ["^GSPC", "^IXIC", "^DJI"],
        "top_stocks": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "JPM", "V"],
    },
    "Bonds": {
        "indices": ["^TNX", "^TYX", "^FVX"],  # 10Y, 30Y, 5Y Treasury yields
        "etfs": ["TLT", "IEF", "SHY", "AGG", "BND"],
    },
    "Commodities": {
        "indices": ["GC=F", "SI=F", "CL=F", "NG=F"],  # Gold, Silver, Crude Oil, Natural Gas
        "etfs": ["GLD", "SLV", "USO", "UNG"],
    },
    "Crypto": {
        "indices": ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD"],
        "etfs": ["IBIT", "FBTC"],
    },
    "Forex": {
        "indices": ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCNH=X", "DX-Y.NYB"],
        "etfs": ["UUP", "FXE", "FXY"],
    },
}

# Date range options
DATE_RANGES = {
    "1d": ("1 Day", 1),
    "1w": ("1 Week", 7),
    "1m": ("1 Month", 30),
    "3m": ("3 Months", 90),
    "1y": ("1 Year", 365),
}


def get_date_range(range_key: str) -> tuple[datetime, datetime]:
    """Get start and end dates based on range key."""
    end_date = datetime.now()
    days = DATE_RANGES.get(range_key, ("1 Week", 7))[1]
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def calculate_change(data) -> tuple[float, float]:
    """Calculate price change and percentage from historical data."""
    if data is None or len(data) < 2:
        return 0.0, 0.0
    
    start_price = data['Close'].iloc[0]
    end_price = data['Close'].iloc[-1]
    
    if start_price == 0:
        return 0.0, 0.0
    
    change = end_price - start_price
    pct_change = (change / start_price) * 100
    
    return change, pct_change


def get_ticker_data(ticker: str, start_date: datetime, end_date: datetime) -> dict:
    """Fetch data for a single ticker."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            return None
        
        change, pct_change = calculate_change(hist)
        
        return {
            "ticker": ticker,
            "current": hist['Close'].iloc[-1],
            "change": change,
            "pct_change": pct_change,
            "high": hist['High'].max(),
            "low": hist['Low'].min(),
            "volume": hist['Volume'].sum() if 'Volume' in hist else 0,
        }
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None


def get_market_indices(region: str, start_date: datetime, end_date: datetime) -> list[dict]:
    """Get market indices for a region."""
    indices = INDICES.get(region, INDICES["US"])
    results = []
    
    for ticker, name in indices.items():
        data = get_ticker_data(ticker, start_date, end_date)
        if data:
            data["name"] = name
            results.append(data)
    
    return results


def get_sector_performance(start_date: datetime, end_date: datetime) -> list[dict]:
    """Get sector ETF performance."""
    results = []
    
    for ticker, name in SECTOR_ETFS.items():
        data = get_ticker_data(ticker, start_date, end_date)
        if data:
            data["name"] = name
            results.append(data)
    
    return sorted(results, key=lambda x: x["pct_change"], reverse=True)


def get_top_movers(asset_class: str, start_date: datetime, end_date: datetime, top_n: int = 5) -> tuple[list, list]:
    """Get top gainers and losers for an asset class."""
    tickers = []
    
    if asset_class == "Stocks":
        tickers = ASSET_CLASSES["Stocks"]["top_stocks"]
    elif asset_class in ASSET_CLASSES:
        tickers = ASSET_CLASSES[asset_class].get("indices", []) + ASSET_CLASSES[asset_class].get("etfs", [])
    
    results = []
    for ticker in tickers:
        data = get_ticker_data(ticker, start_date, end_date)
        if data:
            results.append(data)
    
    sorted_results = sorted(results, key=lambda x: x["pct_change"], reverse=True)
    
    gainers = sorted_results[:top_n]
    losers = sorted_results[-top_n:][::-1] if len(sorted_results) > top_n else []
    
    return gainers, losers


def format_change(pct_change: float) -> str:
    """Format percentage change with emoji."""
    if pct_change > 0:
        return f"🟢 +{pct_change:.2f}%"
    elif pct_change < 0:
        return f"🔴 {pct_change:.2f}%"
    else:
        return f"⚪ {pct_change:.2f}%"


def generate_market_report(
    date_range: str = "1w",
    asset_class: str = "Stocks",
    region: str = "US"
) -> str:
    """Generate a market update report."""
    
    start_date, end_date = get_date_range(date_range)
    range_label = DATE_RANGES.get(date_range, ("1 Week", 7))[0]
    
    report_parts = []
    
    # Header
    report_parts.append(f"# 📊 Financial Market Update")
    report_parts.append(f"**Period:** {start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')} ({range_label})")
    report_parts.append(f"**Focus:** {asset_class} | {region}")
    report_parts.append("")
    report_parts.append("---")
    report_parts.append("")
    
    # Market Indices
    report_parts.append("## 📈 Market Indices")
    indices = get_market_indices(region, start_date, end_date)
    
    if indices:
        report_parts.append("| Index | Current | Change |")
        report_parts.append("|-------|---------|--------|")
        for idx in indices:
            price_fmt = f"${idx['current']:,.2f}" if idx['current'] > 100 else f"{idx['current']:.2f}"
            report_parts.append(f"| **{idx['name']}** | {price_fmt} | {format_change(idx['pct_change'])} |")
    else:
        report_parts.append("*Unable to fetch index data*")
    
    report_parts.append("")
    
    # Top Movers
    report_parts.append("## 🚀 Top Movers")
    gainers, losers = get_top_movers(asset_class, start_date, end_date)
    
    if gainers:
        report_parts.append("### 📈 Top Gainers")
        for g in gainers[:5]:
            report_parts.append(f"- **{g['ticker']}**: {format_change(g['pct_change'])} (${g['current']:.2f})")
    
    report_parts.append("")
    
    if losers:
        report_parts.append("### 📉 Top Losers")
        for l in losers[:5]:
            report_parts.append(f"- **{l['ticker']}**: {format_change(l['pct_change'])} (${l['current']:.2f})")
    
    report_parts.append("")
    
    # Sector Performance (only for US Stocks)
    if asset_class == "Stocks" and region == "US":
        report_parts.append("## 🏭 Sector Performance")
        sectors = get_sector_performance(start_date, end_date)
        
        if sectors:
            report_parts.append("| Sector | Change |")
            report_parts.append("|--------|--------|")
            for s in sectors:
                report_parts.append(f"| {s['name']} | {format_change(s['pct_change'])} |")
    
    report_parts.append("")
    report_parts.append("---")
    report_parts.append(f"*Data from Yahoo Finance | Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    
    return "\n".join(report_parts)


if __name__ == "__main__":
    # Test the module
    print(generate_market_report(date_range="1w", asset_class="Stocks", region="US"))
