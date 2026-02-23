# Weather Forecast

**Date:** 2026-02-21  
**Status:** Implemented  
**Project:** [webapp](../webapp/)  

## Summary
A weather tool showing forecasts, severe weather warnings, and practical tips for a selected area. Default location: NYC.

## Details

### Core Features

| Feature | Description |
|---------|-------------|
| **15-Day Forecast** | Temperature trend, precipitation, conditions for next 15 days |
| **Severe Weather Alerts** | Pull warnings from news/weather APIs when storms, heat waves, etc. are expected |
| **Weather Tips** | AI-generated practical advice based on upcoming conditions |

### Default Settings
- **Location:** New York City (NYC)
- **Units:** Fahrenheit (with option for Celsius)

### Example Output

```
🌤️ NYC Weather Forecast

📅 15-Day Trend
| Date | High | Low | Conditions |
|------|------|-----|------------|
| Feb 22 | 45°F | 32°F | ☀️ Sunny |
| Feb 23 | 48°F | 35°F | ⛅ Partly Cloudy |
| Feb 24 | 42°F | 28°F | 🌧️ Rain |
| ... | ... | ... | ... |

⚠️ Severe Weather Alerts
- Winter Storm Warning: Feb 26-27, 4-8 inches of snow expected

💡 Weather Tips
- Rain expected Tuesday - bring an umbrella
- Temperatures dropping mid-week - layer up
- Good hiking weather this weekend before the storm
```

## Potential Benefits

- Quick daily weather check without opening multiple apps
- Proactive severe weather awareness
- Actionable tips (what to wear, outdoor activity planning)
- Integration with morning routine/tech report

## Implementation Notes

### Data Sources
- **Open-Meteo** (free, no API key required) - forecasts
- **National Weather Service API** (free) - US alerts
- **OpenWeatherMap** (free tier) - alternative
- **News APIs** - severe weather news

### Approach Options
1. **Webapp tab** — Add to existing Easy Life with AI app
2. **Morning report integration** — Include weather in daily briefing
3. **Standalone CLI** — Quick terminal weather check

### Technical Considerations
- Geocoding for location search (city name → coordinates)
- Caching to reduce API calls
- Timezone handling for forecasts
- Icon/emoji mapping for conditions

## Open Questions

- Support multiple saved locations?
- Include hourly breakdown for today?
- Air quality index (AQI)?
- UV index for outdoor activities?
- Integration with calendar (outdoor event warnings)?
