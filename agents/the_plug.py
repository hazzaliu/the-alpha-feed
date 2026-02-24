"""
The Plug — news fetcher.
Pulls headlines from NewsAPI + RSS feeds, filters for US equities and crypto,
deduplicates against Supabase, and returns a clean list of headline dicts.
"""

import feedparser
import httpx
from datetime import datetime, timezone
from config import NEWSAPI_KEY, RSS_FEEDS, NEWSAPI_QUERIES
from db.supabase_client import is_headline_seen, mark_headline_seen

MAX_HEADLINES = 15

EQUITY_KEYWORDS = [
    "stock", "stocks", "equity", "equities", "s&p", "nasdaq", "dow", "nyse",
    "earnings", "ipo", "fed", "federal reserve", "interest rate", "inflation",
    "cpi", "gdp", "recession", "market", "wall street", "shares", "dividend",
    "sec", "etf", "index", "bull", "bear", "rally", "selloff", "sell-off",
]

CRYPTO_KEYWORDS = [
    "bitcoin", "btc", "ethereum", "eth", "crypto", "cryptocurrency", "blockchain",
    "defi", "nft", "altcoin", "solana", "binance", "coinbase", "stablecoin",
    "usdt", "usdc", "web3", "token", "wallet", "exchange", "mining",
]

RELEVANT_KEYWORDS = EQUITY_KEYWORDS + CRYPTO_KEYWORDS


def _is_relevant(title: str, description: str = "") -> bool:
    text = (title + " " + description).lower()
    return any(kw in text for kw in RELEVANT_KEYWORDS)


def _fetch_newsapi() -> list[dict]:
    headlines = []
    for query in NEWSAPI_QUERIES:
        try:
            resp = httpx.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": query,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": 5,
                    "apiKey": NEWSAPI_KEY,
                },
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
            for article in data.get("articles", []):
                url = article.get("url", "")
                title = article.get("title", "")
                description = article.get("description", "") or ""
                source = article.get("source", {}).get("name", "NewsAPI")
                if url and title and _is_relevant(title, description):
                    headlines.append({
                        "title": title,
                        "description": description,
                        "url": url,
                        "source": source,
                        "published_at": article.get("publishedAt", ""),
                    })
        except Exception as e:
            print(f"[The Plug] NewsAPI error for query '{query}': {e}")
    return headlines


def _fetch_rss() -> list[dict]:
    headlines = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:
                title = entry.get("title", "")
                description = entry.get("summary", "") or ""
                url = entry.get("link", "")
                source = feed.feed.get("title", feed_url)
                published = entry.get("published", "")
                if url and title and _is_relevant(title, description):
                    headlines.append({
                        "title": title,
                        "description": description,
                        "url": url,
                        "source": source,
                        "published_at": published,
                    })
        except Exception as e:
            print(f"[The Plug] RSS error for {feed_url}: {e}")
    return headlines


def _deduplicate(headlines: list[dict]) -> list[dict]:
    seen_urls: set[str] = set()
    unique = []
    for h in headlines:
        url = h["url"]
        if url in seen_urls:
            continue
        seen_urls.add(url)
        if is_headline_seen(url):
            continue
        unique.append(h)
    return unique


def _rank(headlines: list[dict]) -> list[dict]:
    crypto_hits = []
    equity_hits = []
    for h in headlines:
        text = (h["title"] + " " + h.get("description", "")).lower()
        if any(kw in text for kw in CRYPTO_KEYWORDS):
            crypto_hits.append(h)
        else:
            equity_hits.append(h)
    combined = equity_hits + crypto_hits
    return combined[:MAX_HEADLINES]


def run() -> list[dict]:
    """
    Fetch, filter, deduplicate, and rank headlines.
    Marks returned headlines as seen in Supabase.
    Returns a list of headline dicts ready for That Girl.
    """
    print("[The Plug] Fetching news...")
    all_headlines = _fetch_newsapi() + _fetch_rss()
    unique = _deduplicate(all_headlines)
    ranked = _rank(unique)

    for h in ranked:
        try:
            mark_headline_seen(h["url"], h["title"])
        except Exception as e:
            print(f"[The Plug] Failed to mark headline seen: {e}")

    print(f"[The Plug] Returning {len(ranked)} fresh headlines.")
    return ranked
