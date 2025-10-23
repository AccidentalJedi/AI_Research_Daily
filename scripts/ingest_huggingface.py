#!/usr/bin/env python3
"""
The Lab - HuggingFace Model & Dataset Ingestion
Tracks new model releases, datasets, and their connection to research papers
"""
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import requests

HF_API_BASE = "https://huggingface.co/api"
HF_MODELS_URL = f"{HF_API_BASE}/models"
HF_DATASETS_URL = f"{HF_API_BASE}/datasets"

# Major research organizations on HuggingFace
MAJOR_ORGS = [
    'google', 'microsoft', 'meta-llama', 'mistralai', 'anthropic',
    'openai', 'EleutherAI', 'bigscience', 'facebook', 'nvidia',
    'apple', 'stabilityai', 'allenai', 'huggingface', 'deepmind'
]


def ensure_data_dir():
    """Create data/huggingface directory if it doesn't exist"""
    Path("data/huggingface").mkdir(parents=True, exist_ok=True)


def get_today_filename():
    """Get filename for today's data"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/huggingface/{today}.json"


def fetch_recent_models(limit=100):
    """Fetch recently updated models from HuggingFace"""
    print("🤗 Fetching recent models from HuggingFace...")
    
    try:
        # Get recently updated models, sorted by last modified
        params = {
            'sort': 'lastModified',
            'direction': -1,
            'limit': limit
        }
        
        response = requests.get(HF_MODELS_URL, params=params, timeout=30)
        response.raise_for_status()
        
        models = response.json()
        print(f"📦 Found {len(models)} recent models")
        
        return models
        
    except Exception as e:
        print(f"❌ Error fetching HuggingFace models: {e}")
        return []


def fetch_recent_datasets(limit=50):
    """Fetch recently updated datasets from HuggingFace"""
    print("📊 Fetching recent datasets from HuggingFace...")
    
    try:
        params = {
            'sort': 'lastModified',
            'direction': -1,
            'limit': limit
        }
        
        response = requests.get(HF_DATASETS_URL, params=params, timeout=30)
        response.raise_for_status()
        
        datasets = response.json()
        print(f"📊 Found {len(datasets)} recent datasets")
        
        return datasets
        
    except Exception as e:
        print(f"❌ Error fetching HuggingFace datasets: {e}")
        return []


def extract_model_info(model):
    """Extract relevant information from HuggingFace model"""
    try:
        model_id = model.get('modelId', model.get('id', 'unknown'))
        
        # Check if recently created (within last 3 days)
        created_at = model.get('createdAt', '')
        last_modified = model.get('lastModified', '')
        
        # Parse dates
        try:
            if created_at:
                created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                days_old = (datetime.now(created_date.tzinfo) - created_date).days
            else:
                days_old = 999
        except:
            days_old = 999
        
        return {
            'model_id': model_id,
            'author': model.get('author', 'unknown'),
            'title': model_id,
            'downloads': model.get('downloads', 0),
            'likes': model.get('likes', 0),
            'tags': model.get('tags', []),
            'pipeline_tag': model.get('pipeline_tag', ''),
            'library': model.get('library_name', ''),
            'created_at': created_at,
            'last_modified': last_modified,
            'days_since_creation': days_old,
            'url': f"https://huggingface.co/{model_id}",
            'date': datetime.now().strftime("%Y-%m-%d"),
            'source': 'huggingface_model',
            'type': 'model'
        }
        
    except Exception as e:
        print(f"⚠️  Error parsing model: {e}")
        return None


def extract_dataset_info(dataset):
    """Extract relevant information from HuggingFace dataset"""
    try:
        dataset_id = dataset.get('id', 'unknown')
        
        return {
            'dataset_id': dataset_id,
            'author': dataset.get('author', 'unknown'),
            'title': dataset_id,
            'downloads': dataset.get('downloads', 0),
            'likes': dataset.get('likes', 0),
            'tags': dataset.get('tags', []),
            'created_at': dataset.get('createdAt', ''),
            'last_modified': dataset.get('lastModified', ''),
            'url': f"https://huggingface.co/datasets/{dataset_id}",
            'date': datetime.now().strftime("%Y-%m-%d"),
            'source': 'huggingface_dataset',
            'type': 'dataset'
        }
        
    except Exception as e:
        print(f"⚠️  Error parsing dataset: {e}")
        return None


def calculate_model_relevance(item):
    """Calculate research relevance score for HuggingFace item"""
    score = 0.0
    
    # Check if from major research org
    author = item.get('author', '').lower()
    is_major_org = any(org.lower() in author for org in MAJOR_ORGS)
    
    if is_major_org:
        score += 0.3
    
    # Downloads and likes indicate community interest
    downloads = item.get('downloads', 0)
    likes = item.get('likes', 0)
    
    if downloads > 10000:
        score += 0.2
    elif downloads > 1000:
        score += 0.1
    
    if likes > 100:
        score += 0.2
    elif likes > 20:
        score += 0.1
    
    # Recency matters for research relevance
    days_old = item.get('days_since_creation', 999)
    if days_old <= 1:
        score += 0.3  # Very recent
    elif days_old <= 3:
        score += 0.2
    elif days_old <= 7:
        score += 0.1
    
    # Pipeline/task relevance
    tags = item.get('tags', [])
    pipeline_tag = item.get('pipeline_tag', '')
    
    research_relevant_tasks = [
        'text-generation', 'text-classification', 'question-answering',
        'translation', 'summarization', 'image-classification',
        'object-detection', 'image-generation', 'text-to-image',
        'automatic-speech-recognition', 'audio-classification'
    ]
    
    if pipeline_tag in research_relevant_tasks:
        score += 0.1
    
    # Novel architectures
    novel_terms = ['novel', 'new', 'improved', 'efficient', 'sota', 'state-of-the-art']
    title_lower = item.get('title', '').lower()
    
    if any(term in title_lower for term in novel_terms):
        score += 0.1
    
    return min(score, 1.0)


def filter_and_score_items(items):
    """Filter and score HuggingFace items for research relevance"""
    print("🔍 Scoring items for research relevance...")
    
    scored_items = []
    
    for item in items:
        if item is None:
            continue
        
        relevance_score = calculate_model_relevance(item)
        item['research_score'] = round(relevance_score, 2)
        
        # Only keep items with score >= 0.4
        if item['research_score'] >= 0.4:
            scored_items.append(item)
    
    # Sort by score (highest first)
    scored_items.sort(key=lambda x: x['research_score'], reverse=True)
    
    print(f"✅ Kept {len(scored_items)} relevant items (score ≥ 0.4)")
    print(f"   High relevance (≥0.7): {len([i for i in scored_items if i['research_score'] >= 0.7])}")
    print(f"   Notable (≥0.5): {len([i for i in scored_items if i['research_score'] >= 0.5])}")
    
    return scored_items


def save_items(items):
    """Save items to JSON file"""
    ensure_data_dir()
    filename = get_today_filename()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(items)} items to {filename}")


def main():
    print("🔬 Starting HuggingFace ingestion...")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_items = []
    
    # Fetch models
    models = fetch_recent_models(limit=100)
    for model in models:
        info = extract_model_info(model)
        if info:
            all_items.append(info)
    
    # Small delay
    time.sleep(1)
    
    # Fetch datasets
    datasets = fetch_recent_datasets(limit=50)
    for dataset in datasets:
        info = extract_dataset_info(dataset)
        if info:
            all_items.append(info)
    
    if not all_items:
        print("⚠️  No items fetched")
        return
    
    # Filter and score
    relevant_items = filter_and_score_items(all_items)
    
    # Save
    save_items(relevant_items)
    
    print("✅ HuggingFace ingestion complete!")


if __name__ == "__main__":
    main()
