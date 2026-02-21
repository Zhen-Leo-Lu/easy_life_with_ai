#!/usr/bin/env python3
"""
Morning Tech Report Generator
Fetches latest tech news from RSS feeds, analyzes with local LLM, emails report.
"""

import feedparser
import subprocess
import os
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
CONFIG = {
    "ollama": {
        "model": os.getenv("OLLAMA_MODEL", "llama3.2"),  # or mistral, llama3, etc.
    },
    "output_dir": Path(__file__).parent.parent / "ideas" / "daily_reports",
    "downloads_dir": Path.home() / "Downloads",
}

RSS_FEEDS = [
    # AI & Tech News
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/", "category": "tech"},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "category": "ai"},
    {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "category": "ai"},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/technology-lab", "category": "tech"},
    {"name": "Hacker News", "url": "https://hnrss.org/frontpage", "category": "tech"},
    # Research
    {"name": "arXiv AI", "url": "https://rss.arxiv.org/rss/cs.AI", "category": "research"},
    {"name": "arXiv LG", "url": "https://rss.arxiv.org/rss/cs.LG", "category": "research"},
    # Funding & Business
    {"name": "Crunchbase News", "url": "https://news.crunchbase.com/feed/", "category": "funding"},
]

def fetch_feeds(hours_back=24):
    """Fetch articles from RSS feeds published in the last N hours."""
    cutoff = datetime.now() - timedelta(hours=hours_back)
    articles = []
    
    for feed_info in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:10]:  # Limit per feed
                # Parse published date
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])
                
                # Include if recent or if we can't determine date
                if published is None or published > cutoff:
                    articles.append({
                        "title": entry.get("title", "No title"),
                        "summary": entry.get("summary", "")[:500],
                        "link": entry.get("link", ""),
                        "source": feed_info["name"],
                        "category": feed_info["category"],
                        "published": published.isoformat() if published else "Unknown",
                    })
        except Exception as e:
            print(f"Error fetching {feed_info['name']}: {e}")
    
    return articles

def analyze_with_ollama(articles):
    """Use local Ollama to analyze articles and generate insights."""
    
    # Prepare article summaries for the prompt
    article_text = "\n\n".join([
        f"**{a['title']}** ({a['source']}, {a['category']})\n{a['summary']}"
        for a in articles[:30]  # Limit to avoid context overflow
    ])
    
    prompt = f"""You are a tech trend analyst. Analyze these recent tech news articles and provide:

1. **Top 5 Signals Today**: The most important developments with brief explanation
2. **Pattern Watch**: Any patterns emerging that connect to broader tech evolution
3. **Prediction Update**: Based on these signals, any short-term predictions (next 3-6 months)
4. **Action Items**: What should a tech professional pay attention to this week

Articles from the last 24 hours:

{article_text}

Provide a concise, actionable morning briefing. Use markdown formatting."""

    try:
        result = subprocess.run(
            ["ollama", "run", CONFIG["ollama"]["model"]],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: Ollama analysis timed out"
    except FileNotFoundError:
        return "Error: Ollama not found. Install from https://ollama.ai"
    except Exception as e:
        return f"Error running Ollama: {e}"

def generate_report(articles, analysis):
    """Generate the full markdown report."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M")
    
    report = f"""# Morning Tech Report — {date_str}

**Generated:** {time_str}  
**Articles analyzed:** {len(articles)}

---

## AI Analysis

{analysis}

---

## Raw Headlines by Category

### AI & Machine Learning
"""
    
    # Group by category
    for category in ["ai", "tech", "research", "funding"]:
        cat_articles = [a for a in articles if a["category"] == category]
        if cat_articles:
            if category != "ai":
                report += f"\n### {category.title()}\n"
            for a in cat_articles[:8]:
                report += f"- [{a['title']}]({a['link']}) — {a['source']}\n"
    
    report += f"""
---

*Report generated by morning_tech_report.py*
"""
    return report

def save_to_downloads(report, date_str):
    """Save report to Downloads folder."""
    downloads_dir = CONFIG["downloads_dir"]
    downloads_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = downloads_dir / f"morning-tech-report-{date_str}.md"
    filepath.write_text(report)
    print(f"📥 Report saved to {filepath}")
    return filepath

def save_report(report, date_str):
    """Save report to markdown file."""
    output_dir = CONFIG["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = output_dir / f"{date_str}-morning-report.md"
    filepath.write_text(report)
    print(f"Report saved to {filepath}")
    return filepath

def main():
    print(f"🌅 Generating Morning Tech Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("-" * 50)
    
    # Step 1: Fetch RSS feeds
    print("📡 Fetching RSS feeds...")
    articles = fetch_feeds(hours_back=24)
    print(f"   Found {len(articles)} articles")
    
    if not articles:
        print("No articles found. Check your internet connection.")
        return
    
    # Step 2: Analyze with Ollama
    print(f"🧠 Analyzing with Ollama ({CONFIG['ollama']['model']})...")
    analysis = analyze_with_ollama(articles)
    
    # Step 3: Generate report
    print("📝 Generating report...")
    report = generate_report(articles, analysis)
    
    # Step 4: Save to file
    date_str = datetime.now().strftime("%Y-%m-%d")
    save_report(report, date_str)
    
    # Step 5: Save to Downloads
    save_to_downloads(report, date_str)
    
    print("-" * 50)
    print("✅ Done!")

if __name__ == "__main__":
    main()
