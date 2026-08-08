import feedparser
import requests
import hashlib
from bs4 import BeautifulSoup
from typing import List, Dict

def fetch_rss_feed(url: str) -> List[Dict]:
    """
    Parse an RSS feed and return a list of items.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    items = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        
        for entry in feed.entries:
            try:
                items.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", "")
                })
            except Exception as e:
                print(f"Error parsing entry: {e}")
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        
    return items

def extract_clean_text(url: str) -> str:
    """
    Scrape the full article body text from a given URL.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.decompose()
            
        # Extract text and collapse whitespace
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return ""

def hash_url(url: str) -> str:
    """
    Create a SHA256 hash of the URL for deduplication.
    """
    return hashlib.sha256(url.encode('utf-8')).hexdigest()
