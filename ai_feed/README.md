# AI Feed

Aggregates AI content from Reddit, Hacker News, Lobsters, DEV.to, and ArXiv — **no API keys required!**

## Features

- **Multiple sources**: r/MachineLearning, r/LocalLLaMA, r/artificial, Hacker News, Lobsters, DEV.to, ArXiv
- **Sorted by popularity**: Posts with most upvotes/points shown first
- **No authentication**: Uses RSS feeds, completely free

## Usage

```python
from ai_feed import fetch_ai_feed, get_top_posts

# Get top 10 posts from all sources
posts = get_top_posts(10)

# Get posts from specific sources
posts = fetch_ai_feed(sources=["r/MachineLearning", "Hacker News AI"])

# Each post has:
# - title, link, source, icon, date, score, summary
```

## CLI Usage

```bash
python ai_feed.py
```

## Sources

| Source | Content Type |
|--------|--------------|
| r/MachineLearning | Research, papers, discussions |
| r/artificial | General AI news |
| r/LocalLLaMA | Open source models |
| Hacker News AI | Tech discussions |
| Lobsters AI | Quality tech links |
| DEV.to AI | Developer articles |
| ArXiv AI | Research papers |

## Requirements

```
feedparser>=6.0.0
```
