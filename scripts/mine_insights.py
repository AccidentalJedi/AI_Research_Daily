#!/usr/bin/env python3
"""
The Lab - Research Insights Mining
Uses embeddings + clustering to detect research patterns and emerging trends
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.cluster import KMeans
    import numpy as np
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    print("⚠️  sentence-transformers or scikit-learn not available - using fallback mode")
    EMBEDDINGS_AVAILABLE = False


def ensure_data_dir():
    """Create data/insights directory if it doesn't exist"""
    Path("data/insights").mkdir(parents=True, exist_ok=True)


def get_today_filename():
    """Get filename for today's insights"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"data/insights/{today}.json"


def load_aggregated_data():
    """Load today's aggregated data"""
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/aggregated/{today}.json"
    
    if not os.path.exists(filename):
        print(f"❌ No aggregated data found for {today}")
        return []
    
    with open(filename, 'r') as f:
        return json.load(f)


def generate_research_trends(entries):
    """
    Identify emerging research trends based on paper patterns
    """
    print("🔮 Identifying emerging research trends...")
    
    # Count keyword frequencies in research papers
    keyword_counts = {}
    for entry in entries:
        text = (entry.get('title', '') + ' ' + 
                entry.get('summary', '') + ' ' + 
                entry.get('abstract', '')).lower()
        
        # Research-relevant keywords
        keywords = [
            'transformer', 'attention', 'mixture-of-experts', 'moe',
            'multimodal', 'vision', 'language', 'reasoning',
            'efficiency', 'scaling', 'architecture', 'benchmark',
            'generation', 'understanding', 'alignment', 'rlhf',
            'sparse', 'quantization', 'fine-tuning', 'prompt'
        ]
        
        for keyword in keywords:
            if keyword in text:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
    
    # Identify trending research areas
    trends = []
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    
    for keyword, count in sorted_keywords[:5]:  # Top 5 trends
        if count >= 3:  # Threshold for significance
            trends.append({
                'topic': keyword,
                'frequency': count,
                'significance': 'high' if count >= 5 else 'medium'
            })
            print(f"  📈 Trending: '{keyword}' ({count} papers)")
    
    return trends


def detect_patterns_simple(entries):
    """Simple research pattern detection using regex (fallback mode)"""
    print("🔍 Detecting research patterns (simple mode)...")
    
    patterns = {
        "multimodal_research": [],
        "efficient_architectures": [],
        "language_models": [],
        "vision_systems": [],
        "reasoning": [],
        "benchmarks": []
    }
    
    for entry in entries:
        text = (entry.get('title', '') + ' ' + 
                entry.get('summary', '') + ' ' + 
                entry.get('abstract', '')).lower()
        
        if re.search(r'(multimodal|vision.?language|cross-modal)', text):
            patterns["multimodal_research"].append(entry)
        
        if re.search(r'(efficient|sparse|quantization|compression|moe)', text):
            patterns["efficient_architectures"].append(entry)
        
        if re.search(r'(language model|llm|gpt|bert|transformer)', text):
            patterns["language_models"].append(entry)
        
        if re.search(r'(vision|image|visual|cv|object detection)', text):
            patterns["vision_systems"].append(entry)
        
        if re.search(r'(reasoning|logic|inference|problem solving)', text):
            patterns["reasoning"].append(entry)
        
        if re.search(r'(benchmark|evaluation|sota|state-of-the-art)', text):
            patterns["benchmarks"].append(entry)
    
    # Filter patterns with at least 2 items
    significant_patterns = {k: v for k, v in patterns.items() if len(v) >= 2}
    
    print(f"✅ Found {len(significant_patterns)} significant research patterns")
    return significant_patterns


def detect_patterns_ml(entries):
    """Advanced pattern detection using embeddings + clustering"""
    print("🔍 Detecting patterns (ML mode)...")
    
    # Extract text for embedding
    texts = [e.get('title', '') + ' ' + e.get('summary', '') for e in entries]
    
    # Generate embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts)
    
    # Cluster (3-5 clusters based on data size)
    n_clusters = min(5, max(3, len(entries) // 10))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)
    
    # Group by cluster
    clusters = {}
    for i, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(entries[i])
    
    # Tag clusters with research themes
    tagged_patterns = {}
    for cluster_id, cluster_entries in clusters.items():
        # Analyze cluster content
        combined_text = ' '.join([
            e.get('title', '') + ' ' + 
            e.get('summary', '') + ' ' + 
            e.get('abstract', '') 
            for e in cluster_entries
        ]).lower()
        
        # Determine research theme
        if 'multimodal' in combined_text or 'vision' in combined_text:
            theme = "multimodal_research"
        elif 'efficient' in combined_text or 'sparse' in combined_text:
            theme = "efficient_architectures"
        elif 'reasoning' in combined_text or 'logic' in combined_text:
            theme = "reasoning_systems"
        elif 'benchmark' in combined_text or 'evaluation' in combined_text:
            theme = "benchmarks"
        elif 'language' in combined_text or 'llm' in combined_text:
            theme = "language_models"
        else:
            theme = f"emerging_topic_{cluster_id}"
        
        tagged_patterns[theme] = cluster_entries
    
    print(f"✅ Found {len(tagged_patterns)} ML-detected research patterns")
    return tagged_patterns


def infer_research_implications(patterns):
    """Infer research implications and predict impact"""
    print("💡 Inferring research implications...")
    
    inferences = []
    
    for pattern_name, entries in patterns.items():
        # Density rule: >3 papers = emerging research direction
        if len(entries) >= 3:
            clean_name = pattern_name.replace('_', ' ').title()
            
            # High-impact prediction for strong signals
            if len(entries) >= 5:
                inferences.append({
                    "pattern": pattern_name,
                    "observation": f"{len(entries)} independent papers",
                    "inference": f"Strong convergence in {clean_name} - expect production adoption within 6-12 months",
                    "confidence": "high"
                })
            else:
                inferences.append({
                    "pattern": pattern_name,
                    "observation": f"{len(entries)} related papers",
                    "inference": f"Emerging interest in {clean_name} - monitor for breakthrough results",
                    "confidence": "medium"
                })
        
        # Specific research area insights
        if "multimodal" in pattern_name:
            inferences.append({
                "pattern": pattern_name,
                "observation": "Multiple multimodal papers",
                "inference": "Integration of vision and language models reaching maturity - production-ready systems likely within 6 months",
                "confidence": "high"
            })
        
        if "efficient" in pattern_name:
            inferences.append({
                "pattern": pattern_name,
                "observation": "Focus on efficiency improvements",
                "inference": "Resource constraints driving innovation - expect deployment on edge devices and mobile",
                "confidence": "medium"
            })
        
        if "reasoning" in pattern_name:
            inferences.append({
                "pattern": pattern_name,
                "observation": "Reasoning capabilities being explored",
                "inference": "Moving beyond pattern matching toward genuine reasoning - still 12-24 months from practical impact",
                "confidence": "medium"
            })
    
    print(f"✅ Generated {len(inferences)} research implications")
    return inferences


def save_insights(patterns, inferences, trends=None):
    """Save research insights to JSON"""
    filename = get_today_filename()
    
    insights = {
        "date": datetime.now().isoformat(),
        "patterns": {k: [{"title": e.get('title'), "url": e.get('url')} for e in v] for k, v in patterns.items()},
        "inferences": inferences,
        "research_trends": trends or [],
        "stats": {
            "total_patterns": len(patterns),
            "total_inferences": len(inferences),
            "total_papers": sum(len(v) for v in patterns.values())
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(insights, f, indent=2)
    
    print(f"💾 Saved research insights to {filename}")


def main():
    """Main mining function"""
    print("🚀 Starting insights mining...")
    ensure_data_dir()
    
    # Load data
    entries = load_aggregated_data()
    if not entries:
        print("⚠️  No data to mine")
        return
    
    print(f"📊 Mining {len(entries)} entries...")
    
    # Identify research trends
    trends = generate_research_trends(entries)
    
    # Detect patterns
    if EMBEDDINGS_AVAILABLE and len(entries) >= 10:
        patterns = detect_patterns_ml(entries)
    else:
        patterns = detect_patterns_simple(entries)
    
    # Infer research implications
    inferences = infer_research_implications(patterns)
    
    # Save
    save_insights(patterns, inferences, trends)
    
    print("✅ Research insights mining complete!")


if __name__ == "__main__":
    main()

