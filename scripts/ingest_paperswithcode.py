#!/usr/bin/env python3
"""
The Lab - Papers with Code Ingestion
Tracks SOTA changes and benchmark performance
"""
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import requests

PWC_API_BASE = "https://paperswithcode.com/api/v1"


def ensure_data_dir():
    """Create data/paperswithcode directory if it doesn't exist"""
    Path("data/paperswithcode").mkdir(parents=True, exist_ok=True)


def get_today_filename():
    """Get filename for today's data"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/paperswithcode/{today}.json"


def fetch_recent_papers(limit=100):
    """Fetch recently added papers from Papers with Code"""
    print("📊 Fetching recent papers from Papers with Code...")
    
    try:
        # Note: Papers with Code API may have rate limits
        # We'll use a conservative approach
        
        url = f"{PWC_API_BASE}/papers/"
        params = {
            'ordering': '-published',
            'page': 1,
            'items_per_page': limit
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        # Handle rate limiting gracefully
        if response.status_code == 429:
            print("⚠️  Rate limited by Papers with Code API")
            return []
        
        response.raise_for_status()
        data = response.json()
        
        papers = data.get('results', [])
        print(f"📄 Found {len(papers)} recent papers")
        
        return papers
        
    except Exception as e:
        print(f"❌ Error fetching Papers with Code: {e}")
        return []


def fetch_sota_entries(limit=50):
    """Fetch recent SOTA (State of the Art) entries"""
    print("🏆 Fetching recent SOTA entries...")
    
    try:
        url = f"{PWC_API_BASE}/papers/"
        params = {
            'ordering': '-published',
            'page': 1,
            'items_per_page': limit
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 429:
            print("⚠️  Rate limited by Papers with Code API")
            return []
        
        response.raise_for_status()
        data = response.json()
        
        # Filter for papers with SOTA claims
        papers = data.get('results', [])
        sota_papers = []
        
        for paper in papers:
            # Check if paper has tasks (indicating benchmarks)
            if paper.get('tasks') or paper.get('methods'):
                sota_papers.append(paper)
        
        print(f"🏆 Found {len(sota_papers)} papers with benchmark results")
        
        return sota_papers
        
    except Exception as e:
        print(f"❌ Error fetching SOTA entries: {e}")
        return []


def extract_paper_info(paper):
    """Extract relevant information from Papers with Code entry"""
    try:
        paper_id = paper.get('id', 'unknown')
        arxiv_id = paper.get('arxiv_id', '')
        
        return {
            'paper_id': paper_id,
            'arxiv_id': arxiv_id,
            'title': paper.get('title', 'N/A'),
            'abstract': paper.get('abstract', '')[:500],  # Truncate for storage
            'authors': paper.get('authors', []),
            'published': paper.get('published', ''),
            'url_abs': paper.get('url_abs', ''),
            'url_pdf': paper.get('url_pdf', ''),
            'tasks': paper.get('tasks', []),
            'methods': paper.get('methods', []),
            'github_url': paper.get('official_code_url', ''),
            'stars': paper.get('stars', 0),
            'date': datetime.now().strftime("%Y-%m-%d"),
            'source': 'paperswithcode',
            'type': 'benchmark'
        }
        
    except Exception as e:
        print(f"⚠️  Error parsing paper: {e}")
        return None


def calculate_benchmark_relevance(paper):
    """Calculate research relevance score for Papers with Code entry"""
    score = 0.0
    
    # Papers with tasks/methods are more relevant
    tasks = paper.get('tasks', [])
    methods = paper.get('methods', [])
    
    if tasks:
        score += 0.3
    if methods:
        score += 0.2
    
    # GitHub presence indicates implementation
    if paper.get('github_url'):
        score += 0.2
    
    # Stars indicate community interest
    stars = paper.get('stars', 0)
    if stars > 100:
        score += 0.2
    elif stars > 10:
        score += 0.1
    
    # Recent papers are more relevant
    published = paper.get('published', '')
    if published:
        try:
            pub_date = datetime.fromisoformat(published.split('T')[0])
            days_old = (datetime.now() - pub_date).days
            
            if days_old <= 3:
                score += 0.3
            elif days_old <= 7:
                score += 0.2
            elif days_old <= 30:
                score += 0.1
        except:
            pass
    
    return min(score, 1.0)


def filter_and_score_papers(papers):
    """Filter and score papers for research relevance"""
    print("🔍 Scoring papers for research relevance...")
    
    scored_papers = []
    
    for paper in papers:
        if paper is None:
            continue
        
        relevance_score = calculate_benchmark_relevance(paper)
        paper['research_score'] = round(relevance_score, 2)
        
        # Only keep papers with score >= 0.4
        if paper['research_score'] >= 0.4:
            scored_papers.append(paper)
    
    # Sort by score (highest first)
    scored_papers.sort(key=lambda x: x['research_score'], reverse=True)
    
    print(f"✅ Kept {len(scored_papers)} relevant papers (score ≥ 0.4)")
    print(f"   High relevance (≥0.7): {len([p for p in scored_papers if p['research_score'] >= 0.7])}")
    print(f"   Notable (≥0.5): {len([p for p in scored_papers if p['research_score'] >= 0.5])}")
    
    return scored_papers


def save_papers(papers):
    """Save papers to JSON file"""
    ensure_data_dir()
    filename = get_today_filename()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(papers)} papers to {filename}")


def main():
    print("🔬 Starting Papers with Code ingestion...")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_papers = []
    
    # Fetch recent papers
    papers = fetch_recent_papers(limit=50)
    for paper in papers:
        info = extract_paper_info(paper)
        if info:
            all_papers.append(info)
    
    # Small delay to respect rate limits
    time.sleep(2)
    
    # Fetch SOTA entries
    sota_papers = fetch_sota_entries(limit=50)
    for paper in sota_papers:
        info = extract_paper_info(paper)
        if info and info not in all_papers:
            all_papers.append(info)
    
    if not all_papers:
        print("⚠️  No papers fetched (this may be due to API rate limits)")
        # Create empty file to indicate we tried
        save_papers([])
        return
    
    # Filter and score
    relevant_papers = filter_and_score_papers(all_papers)
    
    # Save
    save_papers(relevant_papers)
    
    print("✅ Papers with Code ingestion complete!")
    
    # Note about rate limiting
    print("\n💡 Note: Papers with Code has API rate limits.")
    print("   If you see few results, this is expected.")


if __name__ == "__main__":
    main()
