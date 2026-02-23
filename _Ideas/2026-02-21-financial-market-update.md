# Financial Market Update

**Date:** 2026-02-21  
**Status:** Implemented  
**Project:** [financial_market](../financial_market/) | [webapp](../webapp/)  

## Summary
A tool to display financial market updates with customizable filters for date range, asset class, and region. Provides quick market insights without having to visit multiple financial news sites.

## Details

### Core Functionality

Show financial market performance and key events based on user-selected filters:

| Filter | Options | Default |
|--------|---------|---------|
| **Date Range** | Last day, week, month, quarter, year, custom | Last 1 week |
| **Asset Class** | Stocks, bonds, commodities, crypto, forex, REITs | Stocks |
| **Region** | US, Europe, Asia-Pacific, Emerging Markets, Global | US |

### Output Should Include

1. **Performance Summary** — Index/benchmark returns for the period
2. **Top Movers** — Best and worst performers in the category
3. **Key Events** — Major news, earnings, economic data that moved markets
4. **Sector Breakdown** — Performance by sector (for stocks)
5. **Volatility Indicators** — VIX, implied vol, unusual activity

### Example Output

```
📊 US Stock Market Update (Feb 14-21, 2026)

S&P 500: +1.2% | Nasdaq: +1.8% | Dow: +0.9%

Top Gainers: NVDA +8%, AAPL +4%, MSFT +3%
Top Losers: BA -5%, DIS -3%, JNJ -2%

Key Events:
- Fed minutes released (Wed) - dovish tone
- NVDA earnings beat expectations (Thu)
- Housing starts data stronger than expected (Fri)

Sector Performance:
Tech +2.1% | Healthcare -0.5% | Energy +1.0% | ...
```

## Potential Benefits

- Quick daily/weekly market check without opening multiple apps
- Customizable to focus on relevant markets
- Historical context for understanding current movements
- Integration potential with morning_tech_report workflow

## Implementation Notes

### Data Sources
- Yahoo Finance API (free, covers most needs)
- Alpha Vantage (free tier available)
- Financial news APIs (NewsAPI, Polygon.io)
- FRED (Federal Reserve Economic Data)

### Approach Options
1. **CLI tool** — Simple script with command-line flags
2. **Web app extension** — Add to existing webapp as a new page
3. **Morning report integration** — Include in daily morning report

### Technical Considerations
- Rate limits on free APIs
- Caching to avoid redundant calls
- Weekend/holiday handling
- Market hours awareness (pre-market, after-hours)

## Open Questions

- Include analyst ratings/price targets?
- Show charts/visualizations or text-only?
- Real-time vs end-of-day data?
- Alert functionality for significant moves?
- Portfolio tracking integration?
