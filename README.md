# Easy Life with AI

Make life easier with AI — a collection of practical AI-powered tools for daily life.

## 🌐 Try It Now

**👉 [Launch Web App](https://huggingface.co/spaces/leodoggy/easy_life_with_ai)** — No setup required!

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/leodoggy/easy_life_with_ai)
[![Gradio](https://img.shields.io/badge/Gradio-Web_App-orange)](https://huggingface.co/spaces/leodoggy/easy_life_with_ai)

## 🛠️ Tools

| Tool | What it does |
|------|--------------|
| 🌅 **Morning Tech Report** | AI-curated tech news, trends & predictions |
| 🧒 **ELI5** | Complex concepts explained like you're 5 |
| ✉️ **Email Tone Fixer** | Turn awkward emails into professional ones |
| 🎁 **Gift Idea Generator** | Thoughtful gift suggestions |
| 🍳 **Recipe from Fridge** | Meals from your ingredients |

## 💻 Run Locally

Want to run it on your own machine? 

```bash
# Clone the repo
git clone https://github.com/Zhen-Leo-Lu/easy_life_with_ai.git
cd easy_life_with_ai/webapp

# Install dependencies
pip install -r requirements.txt

# Set your Groq API key (free at https://console.groq.com)
echo "GROQ_API_KEY=your-key-here" > .env

# Launch
python app.py
# Open http://localhost:7860
```

### CLI Tools (with local Ollama)

```bash
# Morning Tech Report (requires Ollama)
cd morning_tech_report && pip install feedparser && python morning_tech_report.py

# ELI5 (requires Ollama)
cd eli5 && python eli5.py
```

## 🎯 Philosophy

- **Practical** — Solves real daily problems
- **Simple** — One click to use, easy to customize
- **Free** — No subscriptions required

## 📁 Project Structure

```
easy_life_with_ai/
├── webapp/                 # Web app (Groq API)
├── morning_tech_report/    # CLI: Daily tech news (Ollama)
├── eli5/                   # CLI: Random concept explainer (Ollama)
└── Ideas/                  # Idea pipeline
```

## 🤝 Contributing

- Open issues with ideas for new AI life hacks
- Submit PRs for improvements
- Fork and customize for your own needs

## 📄 License

MIT — use it, modify it, share it.
