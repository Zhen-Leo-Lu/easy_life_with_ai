#!/usr/bin/env python3
"""
Easy Life with AI — Web App
A collection of simple AI tools to make life easier.
Uses local Ollama for AI inference.
"""

import gradio as gr
import random
import requests
import feedparser
from datetime import datetime, timedelta

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

# RSS Feeds for Morning Tech Report
RSS_FEEDS = [
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/", "category": "tech"},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "category": "ai"},
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage", "category": "tech"},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/technology-lab", "category": "tech"},
]

def query_ollama(prompt):
    """Query local Ollama instance."""
    print(f"[DEBUG] Querying Ollama with prompt length: {len(prompt)}")
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=120
        )
        print(f"[DEBUG] Response status: {response.status_code}")
        response.raise_for_status()
        result = response.json().get("response", "No response")
        print(f"[DEBUG] Got response length: {len(result)}")
        return result
    except requests.exceptions.ConnectionError:
        print("[DEBUG] Connection error!")
        return "❌ Error: Ollama is not running. Start it with: `brew services start ollama`"
    except requests.exceptions.Timeout:
        print("[DEBUG] Timeout!")
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

    explanation = query_ollama(prompt)
    return f"## 🧒 {topic.upper()}\n\n{explanation}"

def eli5_random():
    return eli5_explain("", use_random=True)

def eli5_custom(topic):
    if not topic.strip():
        return "Please enter a topic!"
    return eli5_explain(topic)

# ============================================
# Quick Tools
# ============================================

def email_tone_fixer(email_text):
    if not email_text.strip():
        return "Please paste your email!"
    
    prompt = f"""Rewrite this email to be professional, polite, and clear. 
Keep the same meaning but fix any awkward or aggressive tone.

Original email:
{email_text}

Rewritten email:"""

    return query_ollama(prompt)

def gift_idea_generator(person_info):
    if not person_info.strip():
        return "Please describe the person!"
    
    prompt = f"""Based on this description, suggest 5 thoughtful gift ideas with brief explanations:

{person_info}

Format each as:
🎁 **Gift Name** ($price range) - Why it's perfect"""

    return query_ollama(prompt)

def recipe_from_fridge(ingredients):
    if not ingredients.strip():
        return "Please list your ingredients!"
    
    prompt = f"""I have these ingredients: {ingredients}

Suggest 3 easy recipes I can make. For each:
🍳 **Recipe Name**
- Ingredients needed (mark if I'm missing any)
- Quick steps (5 or fewer)
- Time to cook"""

    return query_ollama(prompt)

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
    analysis = query_ollama(prompt)
    
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
                ### ✉️ Email Tone Fixer
                Turn awkward or angry emails into 
                professional, polite messages.
                """)
            
            with gr.Column():
                gr.Markdown("""
                ### 🎁 Gift Idea Generator
                Get thoughtful gift suggestions based on
                the person's interests and your budget.
                """)
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("""
                ### 🍳 Recipe from Fridge
                Tell us what's in your fridge,
                get instant recipe ideas!
                """)
            with gr.Column():
                gr.Markdown("")
        
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
    
    # EMAIL FIXER PAGE
    with gr.Tab("✉️ Email Fixer"):
        gr.Markdown("# ✉️ Email Tone Fixer\nTurn awkward emails into professional ones!")
        
        email_input = gr.Textbox(
            label="Paste your email draft",
            placeholder="Paste your email here...",
            lines=8
        )
        fix_btn = gr.Button("✨ Make it Professional", variant="primary")
        output_email = gr.Markdown(label="Fixed Email")
        
        fix_btn.click(fn=email_tone_fixer, inputs=email_input, outputs=output_email)
    
    # GIFT IDEAS PAGE
    with gr.Tab("🎁 Gift Ideas"):
        gr.Markdown("# 🎁 Gift Idea Generator\nThoughtful gifts without the stress!")
        
        gift_input = gr.Textbox(
            label="Describe the person",
            placeholder="e.g., Mom, 60 years old, likes gardening and cooking, budget $50",
            lines=3
        )
        gift_btn = gr.Button("🎁 Get Ideas", variant="primary")
        output_gift = gr.Markdown(label="Gift Suggestions")
        
        gift_btn.click(fn=gift_idea_generator, inputs=gift_input, outputs=output_gift)
    
    # RECIPES PAGE
    with gr.Tab("🍳 Recipes"):
        gr.Markdown("# 🍳 Recipe from Fridge\nWhat's for dinner? Let's find out!")
        
        recipe_input = gr.Textbox(
            label="What's in your fridge?",
            placeholder="e.g., chicken, broccoli, rice, soy sauce, garlic",
            lines=2
        )
        recipe_btn = gr.Button("🍳 Get Recipes", variant="primary")
        output_recipe = gr.Markdown(label="Recipe Ideas")
        
        recipe_btn.click(fn=recipe_from_fridge, inputs=recipe_input, outputs=output_recipe)

# Launch
if __name__ == "__main__":
    print("Starting Easy Life with AI...")
    print("Testing Ollama connection...")
    test = query_ollama("Say hi")
    print(f"Ollama test: {test[:50]}...")
    print("\nLaunching Gradio app...")
    app.launch(server_name="0.0.0.0", server_port=7860, show_error=True)
