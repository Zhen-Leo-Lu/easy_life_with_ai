# Easy Life with AI — Web App

A web interface for all the AI tools, powered by Groq (free & fast).

## Run Locally

```bash
# Set your Groq API key
export GROQ_API_KEY="your-api-key-here"

# Install and run
pip install -r requirements.txt
python app.py

# Open http://localhost:7860
```

## Deploy to Hugging Face Spaces

1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select **Gradio** as the SDK
3. Upload `app.py` and `requirements.txt`
4. Add your `GROQ_API_KEY` as a Secret in Settings
5. Done! You'll get a public URL

## Get a Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free)
3. Create an API key
4. Very generous free tier!

## Tools Included

| Tool | Description |
|------|-------------|
| 🌅 **Morning Tech Report** | AI-curated tech news & trends |
| 🧒 **ELI5** | Complex concepts explained simply |
| ✉️ **Email Fixer** | Professional email tone |
| 🎁 **Gift Ideas** | Thoughtful gift suggestions |
| 🍳 **Recipes** | Meals from your ingredients |
