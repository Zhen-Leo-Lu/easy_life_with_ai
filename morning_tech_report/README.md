# Morning Tech Report

Automated daily tech trend analysis that runs locally using RSS feeds + Ollama.

**Idea:** [Tech Evolution Predictor](../ideas/2026-02-21-tech-evolution-predictor.md)

## Quick Start

```bash
# 1. Install dependencies
pip3 install feedparser

# 2. Make sure Ollama is running with a model
ollama pull llama3.2

# 3. Run it
python3 morning_tech_report.py
```

## Requirements

- **Python 3.8+**
- **Ollama** — Install from [ollama.ai](https://ollama.ai)

## Setup Ollama

```bash
brew install ollama
brew services start ollama
ollama pull llama3.2
```

## Schedule Daily Runs

Add to crontab (`crontab -e`):

```cron
# Run at 7:00 AM every day
0 7 * * * cd /path/to/easy_life_with_ai/morning_tech_report && python3 morning_tech_report.py >> /tmp/morning_report.log 2>&1
```

## Output

Reports are saved to:
- **Downloads**: `~/Downloads/morning-tech-report-YYYY-MM-DD.md`
- **Project**: `../ideas/daily_reports/YYYY-MM-DD-morning-report.md`
