#!/usr/bin/env python3
"""
Easy Life with AI — Web App
A collection of simple AI tools to make life easier.
Uses Groq API for fast AI inference.
"""

import gradio as gr
import random
import requests
import feedparser
import os
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path

# Load .env file if it exists
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    for line in env_file.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"  # Fast and free on Groq

# RSS Feeds for Morning Tech Report
RSS_FEEDS = [
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/", "category": "tech"},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "category": "ai"},
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage", "category": "tech"},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/technology-lab", "category": "tech"},
]

def query_llm(prompt):
    """Query Groq API for fast inference."""
    if not GROQ_API_KEY:
        return "❌ Error: GROQ_API_KEY not set. Get a free key at https://console.groq.com"
    print(f"[DEBUG] Querying Groq with prompt length: {len(prompt)}")
    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1024,
                "temperature": 0.7
            },
            timeout=60
        )
        print(f"[DEBUG] Response status: {response.status_code}")
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"]
        print(f"[DEBUG] Got response length: {len(result)}")
        return result
    except requests.exceptions.Timeout:
        return "❌ Error: Request timed out. Try again."
    except Exception as e:
        print(f"[DEBUG] Error: {e}")
        return f"❌ Error: {str(e)}"

# ============================================
# ELI5 Tool
# ============================================

COMPLEX_TOPICS = [
    "quantum entanglement", "black holes", "DNA replication", "how vaccines work",
    "theory of relativity", "photosynthesis", "the Big Bang", "dark matter",
    "evolution by natural selection", "how airplanes fly",
    "blockchain", "machine learning", "encryption", "how the internet works",
    "cloud computing", "neural networks", "how GPS works", "quantum computing",
    "inflation", "stock market", "supply and demand", "compound interest",
    "cryptocurrency", "the Federal Reserve", "GDP", "index funds",
    "the trolley problem", "cognitive dissonance", "Plato's cave allegory",
    "the butterfly effect", "Occam's razor", "confirmation bias",
    "the Dunning-Kruger effect", "the prisoner's dilemma",
    "how stars are born", "why is the sky blue", "how seasons work",
    "what is gravity", "the speed of light", "time dilation",
    "how muscles grow", "why we dream", "how memory works",
    "the immune system", "how caffeine works", "why we age",
    "how microwaves heat food", "why ice floats", "how touchscreens work",
    "how soap cleans", "how magnets work", "how refrigerators work",
]

def eli5_explain(topic: str, use_random: bool = False):
    """Explain a topic like user is 5 years old."""
    if use_random or not topic.strip():
        topic = random.choice(COMPLEX_TOPICS)
    
    prompt = f"""Explain "{topic}" like I'm 5 years old.

Rules:
- Use simple words a child would understand
- Use a fun analogy or comparison to everyday things
- Keep it to 3-4 short paragraphs
- End with a fun fact
- Be enthusiastic and make it fun!

Start with "Imagine..." or "You know how..." """

    explanation = query_llm(prompt)
    return f"## 🧒 {topic.upper()}\n\n{explanation}"

def eli5_random():
    return eli5_explain("", use_random=True)

def eli5_custom(topic):
    if not topic.strip():
        return "Please enter a topic!"
    return eli5_explain(topic)

# ============================================
# Morning Tech Report
# ============================================

def fetch_tech_news():
    """Fetch articles from RSS feeds."""
    articles = []
    for feed_info in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:5]:
                articles.append({
                    "title": entry.get("title", "No title"),
                    "summary": entry.get("summary", "")[:300],
                    "link": entry.get("link", ""),
                    "source": feed_info["name"],
                    "category": feed_info["category"],
                })
        except Exception as e:
            print(f"Error fetching {feed_info['name']}: {e}")
    return articles

def generate_tech_report():
    """Generate the morning tech report."""
    print("[DEBUG] Fetching tech news...")
    articles = fetch_tech_news()
    
    if not articles:
        return "❌ Error: Could not fetch news. Check your internet connection."
    
    # Prepare article summaries for the prompt
    article_text = "\n".join([
        f"• **{a['title']}** ({a['source']})"
        for a in articles[:15]
    ])
    
    prompt = f"""You are a tech trend analyst. Based on these headlines from today, provide a brief morning briefing:

{article_text}

Format your response as:
## 🔥 Top 3 Signals Today
(Most important developments)

## 📈 Pattern Watch  
(Any emerging trends)

## 💡 Action Item
(One thing to pay attention to)

Keep it concise and actionable."""

    print("[DEBUG] Analyzing with Ollama...")
    analysis = query_llm(prompt)
    
    # Build the report
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = f"""# 🌅 Morning Tech Report
**Generated:** {date_str} | **Articles:** {len(articles)}

---

{analysis}

---

## 📰 Today's Headlines

"""
    # Add headlines by category
    for cat in ["ai", "tech"]:
        cat_articles = [a for a in articles if a["category"] == cat]
        if cat_articles:
            report += f"### {'🤖 AI' if cat == 'ai' else '💻 Tech'}\n"
            for a in cat_articles[:5]:
                report += f"- [{a['title']}]({a['link']}) — {a['source']}\n"
            report += "\n"
    
    return report

# ============================================
# Financial Market Update
# ============================================

# Market indices by region
MARKET_INDICES = {
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

# Sector ETFs
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
ASSET_TICKERS = {
    "Stocks": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "JPM", "V"],
    "Bonds": ["TLT", "IEF", "SHY", "AGG", "BND"],
    "Commodities": ["GC=F", "SI=F", "CL=F", "NG=F", "GLD", "SLV"],
    "Crypto": ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD"],
    "Forex": ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "DX-Y.NYB"],
}

DATE_RANGE_OPTIONS = {
    "1 Day": 1,
    "1 Week": 7,
    "1 Month": 30,
    "3 Months": 90,
    "1 Year": 365,
}

def get_ticker_data(ticker, start_date, end_date):
    """Fetch data for a single ticker."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty or len(hist) < 1:
            return None
        
        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]
        
        if start_price == 0:
            return None
        
        pct_change = ((end_price - start_price) / start_price) * 100
        
        return {
            "ticker": ticker,
            "current": end_price,
            "pct_change": pct_change,
        }
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def format_pct_change(pct):
    """Format percentage change with color indicator."""
    if pct > 0:
        return f"🟢 +{pct:.2f}%"
    elif pct < 0:
        return f"🔴 {pct:.2f}%"
    return f"⚪ {pct:.2f}%"

def generate_market_update(date_range, asset_class, region):
    """Generate financial market update report."""
    print(f"[DEBUG] Generating market update: {date_range}, {asset_class}, {region}")
    
    days = DATE_RANGE_OPTIONS.get(date_range, 7)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    report_parts = []
    
    # Header
    report_parts.append("# 📊 Financial Market Update")
    report_parts.append(f"**Period:** {start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')} ({date_range})")
    report_parts.append(f"**Focus:** {asset_class} | {region}")
    report_parts.append("")
    report_parts.append("---")
    report_parts.append("")
    
    # Market Indices
    report_parts.append("## 📈 Market Indices")
    indices = MARKET_INDICES.get(region, MARKET_INDICES["US"])
    
    index_data = []
    for ticker, name in indices.items():
        data = get_ticker_data(ticker, start_date, end_date)
        if data:
            data["name"] = name
            index_data.append(data)
    
    if index_data:
        report_parts.append("| Index | Current | Change |")
        report_parts.append("|-------|---------|--------|")
        for idx in index_data:
            price_fmt = f"${idx['current']:,.2f}" if idx['current'] > 100 else f"{idx['current']:.2f}"
            report_parts.append(f"| **{idx['name']}** | {price_fmt} | {format_pct_change(idx['pct_change'])} |")
    else:
        report_parts.append("*Unable to fetch index data*")
    
    report_parts.append("")
    
    # Top Movers
    report_parts.append("## 🚀 Top Movers")
    tickers = ASSET_TICKERS.get(asset_class, ASSET_TICKERS["Stocks"])
    
    movers = []
    for ticker in tickers:
        data = get_ticker_data(ticker, start_date, end_date)
        if data:
            movers.append(data)
    
    if movers:
        sorted_movers = sorted(movers, key=lambda x: x["pct_change"], reverse=True)
        
        report_parts.append("### 📈 Top Gainers")
        for m in sorted_movers[:5]:
            report_parts.append(f"- **{m['ticker']}**: {format_pct_change(m['pct_change'])} (${m['current']:.2f})")
        
        report_parts.append("")
        report_parts.append("### 📉 Top Losers")
        for m in sorted_movers[-5:][::-1]:
            report_parts.append(f"- **{m['ticker']}**: {format_pct_change(m['pct_change'])} (${m['current']:.2f})")
    else:
        report_parts.append("*Unable to fetch mover data*")
    
    report_parts.append("")
    
    # Sector Performance (only for US Stocks)
    if asset_class == "Stocks" and region == "US":
        report_parts.append("## 🏭 Sector Performance")
        
        sectors = []
        for ticker, name in SECTOR_ETFS.items():
            data = get_ticker_data(ticker, start_date, end_date)
            if data:
                data["name"] = name
                sectors.append(data)
        
        if sectors:
            sorted_sectors = sorted(sectors, key=lambda x: x["pct_change"], reverse=True)
            report_parts.append("| Sector | Change |")
            report_parts.append("|--------|--------|")
            for s in sorted_sectors:
                report_parts.append(f"| {s['name']} | {format_pct_change(s['pct_change'])} |")
        else:
            report_parts.append("*Unable to fetch sector data*")
    
    report_parts.append("")
    report_parts.append("---")
    report_parts.append(f"*Data from Yahoo Finance | Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    
    return "\n".join(report_parts)

# ============================================
# Weather Forecast
# ============================================

# Preset locations with coordinates
LOCATIONS = {
    "New York City": {"lat": 40.7128, "lon": -74.0060},
    "Los Angeles": {"lat": 34.0522, "lon": -118.2437},
    "Chicago": {"lat": 41.8781, "lon": -87.6298},
    "Houston": {"lat": 29.7604, "lon": -95.3698},
    "Miami": {"lat": 25.7617, "lon": -80.1918},
    "Seattle": {"lat": 47.6062, "lon": -122.3321},
    "Denver": {"lat": 39.7392, "lon": -104.9903},
    "Boston": {"lat": 42.3601, "lon": -71.0589},
    "San Francisco": {"lat": 37.7749, "lon": -122.4194},
    "Atlanta": {"lat": 33.7490, "lon": -84.3880},
}

WEATHER_CODES = {
    0: ("☀️", "Clear sky"),
    1: ("🌤️", "Mainly clear"),
    2: ("⛅", "Partly cloudy"),
    3: ("☁️", "Overcast"),
    45: ("🌫️", "Foggy"),
    48: ("🌫️", "Depositing rime fog"),
    51: ("🌧️", "Light drizzle"),
    53: ("🌧️", "Moderate drizzle"),
    55: ("🌧️", "Dense drizzle"),
    61: ("🌧️", "Slight rain"),
    63: ("🌧️", "Moderate rain"),
    65: ("🌧️", "Heavy rain"),
    66: ("🌨️", "Light freezing rain"),
    67: ("🌨️", "Heavy freezing rain"),
    71: ("🌨️", "Slight snow"),
    73: ("🌨️", "Moderate snow"),
    75: ("❄️", "Heavy snow"),
    77: ("🌨️", "Snow grains"),
    80: ("🌦️", "Slight rain showers"),
    81: ("🌦️", "Moderate rain showers"),
    82: ("⛈️", "Violent rain showers"),
    85: ("🌨️", "Slight snow showers"),
    86: ("🌨️", "Heavy snow showers"),
    95: ("⛈️", "Thunderstorm"),
    96: ("⛈️", "Thunderstorm with slight hail"),
    99: ("⛈️", "Thunderstorm with heavy hail"),
}

def fetch_weather_forecast(lat, lon):
    """Fetch 15-day forecast from Open-Meteo API."""
    try:
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "auto",
            "forecast_days": 15
        }
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

def fetch_weather_alerts(lat, lon):
    """Fetch weather alerts from NWS API (US only)."""
    try:
        url = f"https://api.weather.gov/alerts/active?point={lat},{lon}"
        headers = {"User-Agent": "EasyLifeWithAI/1.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        alerts = []
        for feature in data.get("features", [])[:5]:
            props = feature.get("properties", {})
            alerts.append({
                "event": props.get("event", "Unknown"),
                "headline": props.get("headline", ""),
                "severity": props.get("severity", ""),
                "description": props.get("description", "")[:500],
            })
        return alerts
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return []

def generate_weather_tips(forecast_summary, alerts):
    """Generate AI weather tips based on forecast."""
    alert_text = ""
    if alerts:
        alert_text = f"\nActive alerts: {', '.join([a['event'] for a in alerts])}"
    
    prompt = f"""Based on this weather forecast, give 3-4 brief, practical tips:

{forecast_summary}{alert_text}

Format as bullet points. Be specific and actionable (e.g., "Bring umbrella Tuesday" not "Be prepared for rain").
Focus on: what to wear, outdoor activities, travel considerations, health tips."""

    return query_llm(prompt)

def generate_weather_report(location):
    """Generate complete weather report for a location."""
    print(f"[DEBUG] Generating weather for: {location}")
    
    coords = LOCATIONS.get(location, LOCATIONS["New York City"])
    lat, lon = coords["lat"], coords["lon"]
    
    # Fetch forecast
    forecast = fetch_weather_forecast(lat, lon)
    if not forecast:
        return "❌ Error: Could not fetch weather data. Try again."
    
    # Fetch alerts
    alerts = fetch_weather_alerts(lat, lon)
    
    report_parts = []
    
    # Header
    report_parts.append(f"# 🌤️ Weather Forecast: {location}")
    report_parts.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report_parts.append("")
    report_parts.append("---")
    report_parts.append("")
    
    # Alerts section
    if alerts:
        report_parts.append("## ⚠️ Active Weather Alerts")
        for alert in alerts:
            severity_emoji = "🔴" if alert["severity"] in ["Extreme", "Severe"] else "🟡"
            report_parts.append(f"{severity_emoji} **{alert['event']}**")
            if alert["headline"]:
                report_parts.append(f"   {alert['headline']}")
        report_parts.append("")
        report_parts.append("---")
        report_parts.append("")
    
    # 15-day forecast table
    report_parts.append("## 📅 15-Day Forecast")
    report_parts.append("")
    report_parts.append("| Date | Conditions | High | Low | Precip | Wind |")
    report_parts.append("|------|------------|------|-----|--------|------|")
    
    daily = forecast.get("daily", {})
    dates = daily.get("time", [])
    weather_codes = daily.get("weather_code", [])
    temp_max = daily.get("temperature_2m_max", [])
    temp_min = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    precip_prob = daily.get("precipitation_probability_max", [])
    wind = daily.get("wind_speed_10m_max", [])
    
    forecast_summary_lines = []
    for i in range(min(15, len(dates))):
        date_obj = datetime.strptime(dates[i], "%Y-%m-%d")
        date_str = date_obj.strftime("%a %m/%d")
        
        code = weather_codes[i] if i < len(weather_codes) else 0
        emoji, condition = WEATHER_CODES.get(code, ("❓", "Unknown"))
        
        high = f"{temp_max[i]:.0f}°F" if i < len(temp_max) else "N/A"
        low = f"{temp_min[i]:.0f}°F" if i < len(temp_min) else "N/A"
        
        precip_val = precip[i] if i < len(precip) else 0
        prob_val = precip_prob[i] if i < len(precip_prob) else 0
        precip_str = f"{prob_val}%" if prob_val > 0 else "-"
        
        wind_val = f"{wind[i]:.0f} mph" if i < len(wind) else "N/A"
        
        report_parts.append(f"| {date_str} | {emoji} {condition} | {high} | {low} | {precip_str} | {wind_val} |")
        
        # Build summary for AI tips
        if i < 7:
            forecast_summary_lines.append(f"{date_str}: {condition}, High {high}, Low {low}, {prob_val}% precip chance")
    
    report_parts.append("")
    report_parts.append("---")
    report_parts.append("")
    
    # AI Tips
    report_parts.append("## 💡 Weather Tips")
    forecast_summary = "\n".join(forecast_summary_lines)
    tips = generate_weather_tips(forecast_summary, alerts)
    report_parts.append(tips)
    
    report_parts.append("")
    report_parts.append("---")
    report_parts.append(f"*Data from Open-Meteo & NWS | Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    
    return "\n".join(report_parts)

# ============================================
# Build the UI
# ============================================

with gr.Blocks(title="Easy Life with AI") as app:
    
    # HOME PAGE
    with gr.Tab("🏠 Home"):
        gr.Markdown("""
        # 🚀 Easy Life with AI
        
        ### Simple AI tools to make your daily life easier
        
        **Powered by local Ollama** — Your data stays on your machine!
        
        Choose a tool from the tabs above 👆
        """)
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("""
                ### 🌅 Morning Tech Report
                AI-curated tech news, trends, and predictions.
                Start your day informed!
                """)
            
            with gr.Column():
                gr.Markdown("""
                ### 🧒 ELI5 — Explain Like I'm 5
                Learn complex concepts explained simply.
                Click "Surprise Me!" for random topics!
                """)
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("""
                ### 📊 Market Update
                Financial market updates by date range,
                asset class, and region.
                """)
            with gr.Column():
                gr.Markdown("""
                ### 🌤️ Weather Forecast
                15-day forecast, severe weather alerts,
                and practical tips for your area.
                """)
        
        gr.Markdown("""
        ---
        📖 [View Source Code](https://github.com/Zhen-Leo-Lu/easy_life_with_ai)
        """)
    
    # MORNING TECH REPORT PAGE
    with gr.Tab("🌅 Tech Report"):
        gr.Markdown("# 🌅 Morning Tech Report\nAI-curated tech news, trends, and predictions!")
        
        report_btn = gr.Button("📰 Generate Today's Report", variant="primary", size="lg")
        output_report = gr.Markdown(label="Report")
        
        report_btn.click(fn=generate_tech_report, outputs=output_report)
    
    # ELI5 PAGE
    with gr.Tab("🧒 ELI5"):
        gr.Markdown("# 🧒 ELI5 — Explain Like I'm 5\nLearn something new in the simplest way possible!")
        
        with gr.Row():
            random_btn = gr.Button("🎲 Surprise Me!", variant="primary", size="lg")
        
        gr.Markdown("**— OR —**")
        
        with gr.Row():
            topic_input = gr.Textbox(
                label="Enter any topic",
                placeholder="e.g., quantum physics, stock market, why sky is blue...",
                scale=4
            )
            custom_btn = gr.Button("Explain!", variant="secondary")
        
        output_eli5 = gr.Markdown(label="Explanation")
        
        random_btn.click(fn=eli5_random, outputs=output_eli5)
        custom_btn.click(fn=eli5_custom, inputs=topic_input, outputs=output_eli5)
        topic_input.submit(fn=eli5_custom, inputs=topic_input, outputs=output_eli5)
    
    # MARKET UPDATE PAGE
    with gr.Tab("📊 Market"):
        gr.Markdown("# 📊 Financial Market Update\nTrack market performance across asset classes and regions!")
        
        with gr.Row():
            date_range_dd = gr.Dropdown(
                choices=list(DATE_RANGE_OPTIONS.keys()),
                value="1 Week",
                label="Date Range"
            )
            asset_class_dd = gr.Dropdown(
                choices=list(ASSET_TICKERS.keys()),
                value="Stocks",
                label="Asset Class"
            )
            region_dd = gr.Dropdown(
                choices=list(MARKET_INDICES.keys()),
                value="US",
                label="Region"
            )
        
        market_btn = gr.Button("📊 Get Market Update", variant="primary", size="lg")
        output_market = gr.Markdown(label="Market Update")
        
        market_btn.click(
            fn=generate_market_update,
            inputs=[date_range_dd, asset_class_dd, region_dd],
            outputs=output_market
        )
    
    # WEATHER PAGE
    with gr.Tab("🌤️ Weather"):
        gr.Markdown("# 🌤️ Weather Forecast\n15-day forecast with alerts and tips!")
        
        with gr.Row():
            location_dd = gr.Dropdown(
                choices=list(LOCATIONS.keys()),
                value="New York City",
                label="Select Location"
            )
        
        weather_btn = gr.Button("🌤️ Get Weather Forecast", variant="primary", size="lg")
        output_weather = gr.Markdown(label="Weather Forecast")
        
        weather_btn.click(
            fn=generate_weather_report,
            inputs=[location_dd],
            outputs=output_weather
        )

# Launch
if __name__ == "__main__":
    print("Starting Easy Life with AI...")
    print("Testing Groq API connection...")
    test = query_llm("Say hi in 3 words")
    print(f"Groq test: {test[:50]}...")
    print("\nLaunching Gradio app...")
    app.launch(server_name="0.0.0.0", server_port=7860, show_error=True)
