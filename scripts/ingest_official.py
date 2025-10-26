#!/usr/bin/env python3
"""
Ollama Pulse - Official Sources Ingestion
Polls Ollama blog RSS and /cloud page for official updates

PRIMARY: Uses Ollama web_search API for official announcements
FALLBACK: Direct RSS/scraping if web_search fails
"""
import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path

import feedparser
import requests
from bs4 import BeautifulSoup

from ollama_turbo_client import OllamaTurboClient


def ensure_data_dir():
    """Create data/official directory if it doesn't exist"""
    Path("data/official").mkdir(parents=True, exist_ok=True)


def get_today_filename():
    """Get filename for today's data"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/official/{today}.json"


def fetch_blog_rss():
    """Fetch Ollama blog RSS feed"""
    print("📡 Fetching Ollama blog RSS...")
    try:
        feed = feedparser.parse("https://ollama.com/blog/rss")
        entries = []
        
        for entry in feed.entries[:10]:  # Last 10 posts
            entries.append({
                "title": entry.title,
                "date": entry.published if hasattr(entry, 'published') else datetime.now().isoformat(),
                "summary": entry.summary if hasattr(entry, 'summary') else "",
                "url": entry.link,
                "source": "blog",
                "highlights": extract_highlights(entry.title + " " + (entry.summary if hasattr(entry, 'summary') else ""))
            })
        
        print(f"✅ Found {len(entries)} blog posts")
        return entries
    except Exception as e:
        print(f"❌ Error fetching blog RSS: {e}")
        return []


def fetch_cloud_page():
    """Fetch Ollama /cloud page for model updates"""
    print("📡 Fetching Ollama /cloud page...")
    try:
        response = requests.get("https://ollama.com/cloud", timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract cloud models (look for model names with -cloud suffix)
        text = soup.get_text()
        cloud_models = re.findall(r'([\w\-.:0-9]+-cloud)', text)
        
        if cloud_models:
            entry = {
                "title": "Cloud Models Available",
                "date": datetime.now().isoformat(),
                "summary": f"Found {len(set(cloud_models))} cloud models",
                "url": "https://ollama.com/cloud",
                "source": "cloud_page",
                "highlights": [f"model: {model}" for model in set(cloud_models)]
            }
            print(f"✅ Found {len(set(cloud_models))} cloud models")
            return [entry]
        
        return []
    except Exception as e:
        print(f"❌ Error fetching /cloud page: {e}")
        return []


def extract_highlights(text):
    """Extract key highlights from text using regex"""
    highlights = []
    
    # Model names
    models = re.findall(r'([\w\-]+:\d+[bB](?:-cloud)?)', text)
    highlights.extend([f"model: {m}" for m in models])
    
    # Features
    features = re.findall(r'(multimodal|vision|voice|STT|TTS|web search|API)', text, re.IGNORECASE)
    highlights.extend([f"feature: {f}" for f in features])
    
    # Tools
    tools = re.findall(r'(n8n|Zapier|Make|GitHub|Docker)', text, re.IGNORECASE)
    highlights.extend([f"tool: {t}" for t in tools])
    
    return list(set(highlights))[:10]  # Max 10 highlights


def save_data(entries):
    """Save entries to JSON file"""
    if not entries:
        print("⚠️  No data to save")
        return
    
    filename = get_today_filename()
    
    # Load existing data if file exists
    existing = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            existing = json.load(f)
    
    # Merge and deduplicate by URL
    all_entries = existing + entries
    unique_entries = {e['url']: e for e in all_entries}.values()
    
    # Save
    with open(filename, 'w') as f:
        json.dump(list(unique_entries), f, indent=2)
    
    print(f"💾 Saved {len(unique_entries)} entries to {filename}")


async def fetch_via_web_search():
    """
    PRIMARY: Use Ollama web_search API for official announcements
    """
    print("🔍 PRIMARY: Using Ollama web_search for official updates...")

    try:
        async with OllamaTurboClient() as client:
            # Search for official Ollama announcements
            results = await client.discover_ecosystem_content(
                query="Official Ollama announcements, blog posts, and cloud updates from ollama.com",
                content_type="news",
                max_results=20
            )

            print(f"✅ Web search found {len(results)} official updates")
            return results

    except Exception as e:
        print(f"⚠️  Web search failed: {e}")
        print("   Falling back to direct RSS/scraping...")
        return []


def main():
    """Main ingestion function"""
    print("🚀 Starting official sources ingestion...")
    ensure_data_dir()

    # PRIMARY: Try Ollama web_search first
    web_search_entries = asyncio.run(fetch_via_web_search())

    # FALLBACK: Use direct RSS/scraping if web_search failed or returned few results
    if len(web_search_entries) < 5:
        print("📡 FALLBACK: Using direct RSS/scraping...")
        blog_entries = fetch_blog_rss()
        cloud_entries = fetch_cloud_page()
        fallback_entries = blog_entries + cloud_entries
        all_entries = web_search_entries + fallback_entries
    else:
        print("✅ Web search provided sufficient results, skipping fallback")
        all_entries = web_search_entries

    # Save
    save_data(all_entries)

    print("✅ Official sources ingestion complete!")


if __name__ == "__main__":
    main()

