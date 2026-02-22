# Easy Life with AI

Make life easier with AI — a collection of practical AI-powered tools for daily life.

## 🌐 Try It Now

**👉 [Launch Web App](https://huggingface.co/spaces/zhen-leo-lu/easy_life_with_ai)** — No setup required!

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/zhen-leo-lu/easy_life_with_ai)

## 🛠️ Tools

| Tool | What it does |
|------|--------------|
| 🌅 **Morning Tech Report** | AI-curated tech news, trends & predictions |
| 📊 **Market Update** | Financial market updates by date range, asset class & region |
| 🧒 **ELI5** | Complex concepts explained like you're 5 |
| ✉️ **Email Tone Fixer** | Turn awkward emails into professional ones |
| 🎁 **Gift Idea Generator** | Thoughtful gift suggestions |
| 🍳 **Recipe from Fridge** | Meals from your ingredients |

## 💻 Run Locally

### Option 1: CLI Tools (No API key needed!)

Uses **Ollama** — free, runs 100% on your machine.

```bash
# Install Ollama (one-time)
brew install ollama
brew services start ollama
ollama pull llama3.2

# Run Morning Tech Report
cd morning_tech_report
pip install feedparser
python morning_tech_report.py

# Run ELI5
cd eli5
python eli5.py
```

### Option 2: Web App (Local)

Requires a free Groq API key from [console.groq.com](https://console.groq.com)

```bash
cd webapp
pip install -r requirements.txt
echo "GROQ_API_KEY=your-key-here" > .env
python app.py
# Open http://localhost:7860
```

## 🎯 Philosophy

- **Practical** — Solves real daily problems
- **Simple** — One click to use
- **Free** — No subscriptions, local AI option available

## 📁 Project Structure

```
easy_life_with_ai/
├── webapp/                 # Web app (uses Groq API)
├── morning_tech_report/    # CLI (uses local Ollama - no API key!)
├── eli5/                   # CLI (uses local Ollama - no API key!)
├── financial_market/       # Financial market data module (uses Yahoo Finance)
└── Ideas/                  # Idea pipeline
```

## 🤝 Contributing

- Open issues with ideas for new AI life hacks
- Submit PRs for improvements
- Fork and customize for your own needs

## 📄 License

MIT — use it, modify it, share it.
