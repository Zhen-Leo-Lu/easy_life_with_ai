# Easy Life with AI — Web App

A web interface for all the AI tools in this repo.

## Tools Included

| Tool | Description |
|------|-------------|
| 🧒 **ELI5** | Complex concepts explained simply |
| ✉️ **Email Fixer** | Turn awkward emails into professional ones |
| 🎁 **Gift Ideas** | Thoughtful gift suggestions |
| 🍳 **Recipes** | What to cook with what's in your fridge |

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Then open http://localhost:7860

## Deploy to Hugging Face Spaces

1. Create a new Space at huggingface.co/spaces
2. Select "Gradio" as the SDK
3. Upload `app.py` and `requirements.txt`
4. Done! You'll get a public URL

## Tech Stack

- **Gradio** — Web UI framework
- **Hugging Face Inference** — Free AI API
- **Zephyr-7B** — The LLM powering the tools
