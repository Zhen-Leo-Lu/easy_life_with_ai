#!/usr/bin/env python3
"""
AI Feed Module
Aggregates AI content from Reddit, Hacker News, Lobsters, DEV.to, and ArXiv.
Uses RSS feeds - no API keys required!
"""

import feedparser
import re
from datetime import datetime

AI_FEED_SOURCES = [
    {"name": "r/MachineLearning", "url": "https://www.reddit.com/r/MachineLearning/.rss", "icon": "🤖"},
    {"name": "r/artificial", "url": "https://www.reddit.com/r/artificial/.rss", "icon": "🧠"},
    {"name": "r/LocalLLaMA", "url": "https://www.reddit.com/r/LocalLLaMA/.rss", "icon": "🦙"},
    {"name": "Hacker News AI", "url": "https://hnrss.org/newest?q=AI+OR+LLM+OR+GPT+OR+machine+learning", "icon": "📰"},
    {"name": "Lobsters AI", "url": "https://lobste.rs/t/ai.rss", "icon": "🦞"},
    {"name": "DEV.to AI", "url": "https://dev.to/feed/tag/ai", "icon": "👩‍💻"},
    {"name": "ArXiv AI", "url": "http://export.arxiv.org/rss/cs.AI", "icon": "📄"},
]


def extract_score(entry, source_name):
    """Extract popularity score from RSS entry."""
    score = 0
    
    # Reddit: score is in the content
    if "reddit" in source_name.lower() or source_name.startswith("r/"):
        content = entry.get("content", [{}])[0].get("value", "") if entry.get("content") else ""
        content += entry.get("summary", "")
        match = re.search(r'(\d+)\s*(?:points?|upvotes?)', content, re.I)
        if match:
            score = int(match.group(1))
    
    # Hacker News: points in content
    elif "hacker" in source_name.lower() or "hn" in source_name.lower():
        content = entry.get("summary", "")
        match = re.search(r'Points:\s*(\d+)', content)
        if match:
            score = int(match.group(1))
    
    return score


def fetch_ai_feed(sources=None):
    """
    Fetch AI content from RSS sources, sorted by popularity.
    
    Args:
        sources: List of source names to fetch from. If None, uses all sources.
    
    Returns:
        List of posts sorted by score (highest first)
    """
    if sources is None:
        sources = [s["name"] for s in AI_FEED_SOURCES]
    
    source_map = {s["name"]: s for s in AI_FEED_SOURCES}
    all_posts = []
    
    for source_name in sources:
        source = source_map.get(source_name)
        if not source:
            continue
        
        try:
            feed = feedparser.parse(source["url"])
            for entry in feed.entries[:15]:
                published = ""
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d %H:%M")
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6]).strftime("%Y-%m-%d %H:%M")
                
                score = extract_score(entry, source_name)
                title = entry.get("title", "No title")[:100]
                title = title.split(" (Comments)")[0].strip()
                
                all_posts.append({
                    "title": title,
                    "link": entry.get("link", ""),
                    "source": source["name"],
                    "icon": source["icon"],
                    "date": published,
                    "score": score,
                    "summary": entry.get("summary", "")[:300],
                })
        except Exception as e:
            print(f"Error fetching {source['name']}: {e}")
    
    # Sort by score (highest first)
    all_posts.sort(key=lambda x: x["score"], reverse=True)
    return all_posts


def get_top_posts(n=10, sources=None):
    """Get top N posts by popularity."""
    posts = fetch_ai_feed(sources)
    return posts[:n]


def print_feed(posts):
    """Print posts in a readable format."""
    print(f"\n🤖 AI Feed - {len(posts)} posts\n")
    print("-" * 60)
    
    for i, p in enumerate(posts, 1):
        score_str = f"⬆️ {p['score']}" if p['score'] > 0 else ""
        print(f"{i}. [{p['icon']}] {p['title']}")
        print(f"   {p['link']}")
        print(f"   {p['source']} {score_str} {p['date']}")
        print()


if __name__ == "__main__":
    print("Fetching AI Feed...")
    posts = get_top_posts(15)
    print_feed(posts)
