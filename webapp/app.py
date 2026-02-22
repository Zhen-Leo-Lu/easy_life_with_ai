#!/usr/bin/env python3
"""
Easy Life with AI — Web App
A collection of simple AI tools to make life easier.
"""

import gradio as gr
import random
from huggingface_hub import InferenceClient

# Initialize HuggingFace client (free inference API)
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")

# ============================================
# ELI5 Tool
# ============================================

COMPLEX_TOPICS = [
    # Science
    "quantum entanglement", "black holes", "DNA replication", "how vaccines work",
    "theory of relativity", "photosynthesis", "the Big Bang", "dark matter",
    "evolution by natural selection", "how airplanes fly",
    # Technology
    "blockchain", "machine learning", "encryption", "how the internet works",
    "cloud computing", "neural networks", "how GPS works", "quantum computing",
    # Economics
    "inflation", "stock market", "supply and demand", "compound interest",
    "cryptocurrency", "the Federal Reserve", "GDP", "index funds",
    # Philosophy
    "the trolley problem", "cognitive dissonance", "Plato's cave allegory",
    "the butterfly effect", "Occam's razor", "confirmation bias",
    "the Dunning-Kruger effect", "the prisoner's dilemma",
    # Space
    "how stars are born", "why is the sky blue", "how seasons work",
    "what is gravity", "the speed of light", "time dilation",
    # Health
    "how muscles grow", "why we dream", "how memory works",
    "the immune system", "how caffeine works", "why we age",
    # Everyday
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

    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )
    
    explanation = response.choices[0].message.content
    return f"## 🧒 {topic.upper()}\n\n{explanation}"

def eli5_random():
    """Get a random topic explained."""
    return eli5_explain("", use_random=True)

def eli5_custom(topic):
    """Explain a custom topic."""
    if not topic.strip():
        return "Please enter a topic!"
    return eli5_explain(topic)

# ============================================
# Quick Tools
# ============================================

def email_tone_fixer(email_text):
    """Fix the tone of an email to be professional."""
    if not email_text.strip():
        return "Please paste your email!"
    
    prompt = f"""Rewrite this email to be professional, polite, and clear. 
Keep the same meaning but fix any awkward or aggressive tone.

Original email:
{email_text}

Rewritten email:"""

    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message.content

def gift_idea_generator(person_info):
    """Generate gift ideas based on person description."""
    if not person_info.strip():
        return "Please describe the person!"
    
    prompt = f"""Based on this description, suggest 5 thoughtful gift ideas with brief explanations:

{person_info}

Format each as:
🎁 **Gift Name** ($price range) - Why it's perfect"""

    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.8,
    )
    return response.choices[0].message.content

def recipe_from_fridge(ingredients):
    """Suggest recipes from available ingredients."""
    if not ingredients.strip():
        return "Please list your ingredients!"
    
    prompt = f"""I have these ingredients: {ingredients}

Suggest 3 easy recipes I can make. For each:
🍳 **Recipe Name**
- Ingredients needed (mark if I'm missing any)
- Quick steps (5 or fewer)
- Time to cook"""

    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.8,
    )
    return response.choices[0].message.content

# ============================================
# Build the UI
# ============================================

# Custom CSS for better styling
css = """
.tool-card {
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 20px;
    margin: 10px;
    text-align: center;
    transition: all 0.3s ease;
}
.tool-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.header {
    text-align: center;
    margin-bottom: 20px;
}
"""

with gr.Blocks(title="Easy Life with AI") as app:
    
    # ============================================
    # HOME PAGE
    # ============================================
    with gr.Tab("🏠 Home"):
        gr.Markdown("""
        # 🚀 Easy Life with AI
        
        ### Simple AI tools to make your daily life easier
        
        Choose a tool below to get started:
        """)
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("""
                ### 🧒 ELI5 — Explain Like I'm 5
                Learn complex concepts explained simply.
                Random topics or ask anything!
                
                *Click the ELI5 tab above →*
                """)
            
            with gr.Column():
                gr.Markdown("""
                ### ✉️ Email Tone Fixer
                Turn awkward or angry emails into 
                professional, polite messages.
                
                *Click the Email Fixer tab above →*
                """)
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("""
                ### 🎁 Gift Idea Generator
                Get thoughtful gift suggestions based on
                the person's interests and your budget.
                
                *Click the Gift Ideas tab above →*
                """)
            
            with gr.Column():
                gr.Markdown("""
                ### 🍳 Recipe from Fridge
                Tell us what's in your fridge,
                get instant recipe ideas!
                
                *Click the Recipes tab above →*
                """)
        
        gr.Markdown("""
        ---
        💡 **All tools are free and run on AI.** No login required.
        
        📖 [View Source Code](https://github.com/Zhen-Leo-Lu/easy_life_with_ai)
        """)
    
    # ============================================
    # ELI5 PAGE
    # ============================================
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
    
    # ============================================
    # EMAIL FIXER PAGE
    # ============================================
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
    
    # ============================================
    # GIFT IDEAS PAGE
    # ============================================
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
    
    # ============================================
    # RECIPES PAGE
    # ============================================
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
    app.launch()
