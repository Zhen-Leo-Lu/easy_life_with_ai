# Easy Life with AI

Make life easier with AI — a collection of practical AI-powered tools for daily life.

## 🌐 Try It Online

**[Launch Web App →](./webapp/)** — Run locally or deploy to Hugging Face Spaces for free!

```bash
cd webapp && pip install -r requirements.txt && python app.py
# Open http://localhost:7860
```

## What's Inside

| Tool | Description | Web | CLI |
|------|-------------|-----|-----|
| 🧒 **ELI5** | Complex concepts explained simply | ✅ | ✅ |
| ✉️ **Email Fixer** | Turn awkward emails into professional ones | ✅ | — |
| 🎁 **Gift Ideas** | Thoughtful gift suggestions | ✅ | — |
| 🍳 **Recipes** | What to cook with your ingredients | ✅ | — |
| 📰 **Morning Tech Report** | AI-curated tech news & predictions | — | ✅ |

## Philosophy

This repo is about turning AI from a buzzword into something that genuinely helps your daily life. Each project is:

- **Practical** — Solves a real problem
- **Local-first** — Runs on your machine, respects your privacy
- **Simple** — Easy to set up and customize

## Getting Started

### Morning Tech Report

Get a daily AI-generated briefing of tech news, patterns, and predictions delivered to your Downloads folder.

```bash
cd morning_tech_report
pip3 install feedparser
python3 morning_tech_report.py
```

**Requirements:** [Ollama](https://ollama.ai) (free, runs locally)

[Full setup guide →](./morning_tech_report/README.md)

## Ideas Pipeline

Have an idea for making life easier with AI? The `ideas/` folder tracks concepts from spark to shipped project.

```
ideas/
├── 2026-02-21-tech-evolution-predictor.md  → morning_tech_report/
└── (your next idea here)
```

## Contributing

Feel free to:
- Open issues with ideas for new AI life hacks
- Submit PRs for improvements
- Fork and customize for your own needs

## License

MIT — use it, modify it, share it.
