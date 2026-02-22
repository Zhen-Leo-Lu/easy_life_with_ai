# Easy Life with AI

Make life easier with AI — a collection of practical AI-powered tools for daily life.

## 🌐 Launch the Web App

```bash
cd webapp
pip install -r requirements.txt
python app.py
# Open http://localhost:7860
```

![Web App](https://img.shields.io/badge/Gradio-Web_App-orange) ![Ollama](https://img.shields.io/badge/Ollama-Local_AI-blue)

## 🛠️ Tools

| Tool | What it does | Web | CLI |
|------|--------------|:---:|:---:|
| 🌅 **Morning Tech Report** | AI-curated tech news, trends & predictions | ✅ | ✅ |
| 🧒 **ELI5** | Complex concepts explained like you're 5 | ✅ | ✅ |
| ✉️ **Email Tone Fixer** | Turn awkward emails into professional ones | ✅ | — |
| 🎁 **Gift Idea Generator** | Thoughtful gift suggestions | ✅ | — |
| 🍳 **Recipe from Fridge** | Meals from your ingredients | ✅ | — |

## ⚡ Quick Start

### Option 1: Web App (All tools in one place)

```bash
# Install dependencies
cd webapp && pip install -r requirements.txt

# Start Ollama (if not running)
brew services start ollama

# Launch
python app.py
```

Open **http://localhost:7860** and start using the tools!

### Option 2: CLI Tools

```bash
# Morning Tech Report
cd morning_tech_report && pip install feedparser && python morning_tech_report.py

# ELI5
cd eli5 && python eli5.py
```

## 📋 Requirements

- **Python 3.8+**
- **Ollama** — Free, local AI. Install from [ollama.ai](https://ollama.ai)
  ```bash
  brew install ollama
  brew services start ollama
  ollama pull llama3.2
  ```

## 🎯 Philosophy

- **Practical** — Solves real daily problems
- **Local-first** — Your data stays on your machine
- **Simple** — One command to run, easy to customize
- **Free** — No API keys, no subscriptions

## 📁 Project Structure

```
easy_life_with_ai/
├── webapp/                 # Web app with all tools
│   ├── app.py
│   └── requirements.txt
├── morning_tech_report/    # CLI: Daily tech news
├── eli5/                   # CLI: Random concept explainer
└── Ideas/                  # Idea pipeline
```

## 🤝 Contributing

- Open issues with ideas for new AI life hacks
- Submit PRs for improvements
- Fork and customize for your own needs

## 📄 License

MIT — use it, modify it, share it.
