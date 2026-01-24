import feedparser
import hashlib
from typing import List
from src.models import Headline

def get_fingerprint(title: str, url: str) -> str:
    """Create a unique hash for deduplication."""
    return hashlib.md5(f"{title}|{url}".encode()).hexdigest()

def fetch_feed(url: str, source_name: str) -> List[Headline]:
    print(f"Fetching {source_name} from {url}...")
    try:
        feed = feedparser.parse(url)
        headlines = []
        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", "")
            if not title:
                continue
                
            fingerprint = get_fingerprint(title, link)
            
            headlines.append(Headline(
                source=source_name,
                title=title,
                url=link,
                summary=summary[:500], # Truncate for sanity
                published=entry.get("published", ""),
                fingerprint=fingerprint
            ))
        return headlines
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def fetch_all_feeds(feeds: List[str]) -> List[Headline]:
    all_headlines = []
    for url in feeds:
        # Simple source name extraction
        source_name = url.split("://")[1].split("/")[0]
        # Some special handling for known domains to make it prettier
        if "reuters" in source_name: source_name = "Reuters"
        elif "cnbc" in source_name: source_name = "CNBC"
        elif "bbc" in source_name: source_name = "BBC"
        elif "economist" in source_name: source_name = "Economist"
        
        all_headlines.extend(fetch_feed(url, source_name))
    return all_headlines
