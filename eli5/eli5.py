#!/usr/bin/env python3
"""
ELI5 — Explain Like I'm 5
Hit the button, learn something new. Random complex concepts explained simply.
"""

import subprocess
import random

COMPLEX_TOPICS = [
    # Science
    "quantum entanglement",
    "black holes",
    "DNA replication",
    "how vaccines work",
    "theory of relativity",
    "photosynthesis",
    "the Big Bang",
    "dark matter",
    "evolution by natural selection",
    "how airplanes fly",
    
    # Technology
    "blockchain",
    "machine learning",
    "encryption",
    "how the internet works",
    "cloud computing",
    "neural networks",
    "how GPS works",
    "quantum computing",
    "how WiFi works",
    "cryptocurrency mining",
    
    # Economics & Society
    "inflation",
    "stock market",
    "supply and demand",
    "compound interest",
    "how banks create money",
    "cryptocurrency",
    "the Federal Reserve",
    "GDP",
    "trade deficits",
    "index funds",
    
    # Philosophy & Psychology
    "the trolley problem",
    "cognitive dissonance",
    "Plato's cave allegory",
    "the butterfly effect",
    "Occam's razor",
    "confirmation bias",
    "the Dunning-Kruger effect",
    "stoicism",
    "existentialism",
    "the prisoner's dilemma",
    
    # Math
    "probability",
    "the Fibonacci sequence",
    "prime numbers",
    "calculus (derivatives)",
    "the Pythagorean theorem",
    "exponential growth",
    "the Monty Hall problem",
    "infinity",
    "the golden ratio",
    "statistics vs probability",
    
    # Space & Universe
    "how stars are born",
    "why is the sky blue",
    "how seasons work",
    "tides and the moon",
    "what is gravity",
    "the speed of light",
    "parallel universes",
    "time dilation",
    "why planets are round",
    "asteroid vs comet vs meteor",
    
    # Health & Body
    "how muscles grow",
    "why we dream",
    "how memory works",
    "the immune system",
    "how caffeine works",
    "what causes cancer",
    "how antidepressants work",
    "the gut-brain connection",
    "why we age",
    "how sleep restores the body",
    
    # Everyday Things
    "how microwaves heat food",
    "why ice floats",
    "how touchscreens work",
    "why we yawn",
    "how soap cleans",
    "why the sky is dark at night",
    "how magnets work",
    "why we get hiccups",
    "how refrigerators work",
    "why we have fingerprints",
]

def explain_eli5(topic):
    """Use Ollama to explain the topic like the user is 5."""
    
    prompt = f"""Explain "{topic}" like I'm 5 years old.

Rules:
- Use simple words a child would understand
- Use a fun analogy or comparison to everyday things
- Keep it to 3-4 short paragraphs
- End with a fun fact or "wow" moment
- Be enthusiastic and make it fun!

Start with: "Imagine..." or "You know how..." """

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout.strip()
    except FileNotFoundError:
        return "Error: Ollama not found. Install from https://ollama.ai"
    except Exception as e:
        return f"Error: {e}"

def main():
    # Pick a random topic
    topic = random.choice(COMPLEX_TOPICS)
    
    print("=" * 50)
    print(f"🧒 ELI5: {topic.upper()}")
    print("=" * 50)
    print()
    
    explanation = explain_eli5(topic)
    print(explanation)
    
    print()
    print("-" * 50)
    print("🔄 Run again for another random concept!")

if __name__ == "__main__":
    main()
