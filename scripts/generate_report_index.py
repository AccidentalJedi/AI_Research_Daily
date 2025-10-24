#!/usr/bin/env python3
"""
Generate reports index JSON for the web interface.
This script scans the docs/reports directory and creates an index.json file
that lists all available reports with their metadata.
"""

import os
import json
from pathlib import Path
from datetime import datetime, timezone

def generate_report_index():
    """Generate index.json from reports directory."""
    
    # Get the repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    reports_dir = repo_root / 'docs' / 'reports'
    
    if not reports_dir.exists():
        print(f"Error: Reports directory not found at {reports_dir}")
        return
    
    reports = []
    
    # Scan for markdown reports
    for report_file in reports_dir.glob('*.md'):
        filename = report_file.name
        
        # Parse filename to get type and date
        if filename.startswith('lab-'):
            report_type = 'lab'
            date = filename.replace('lab-', '').replace('.md', '')
        elif filename.startswith('pulse-'):
            report_type = 'pulse'
            date = filename.replace('pulse-', '').replace('.md', '')
        else:
            # Skip files that don't match the pattern
            continue
        
        # Read first few lines to get title and description
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                title = filename.replace('.md', '')
                description = ''
                
                # Extract title from markdown (skip front matter)
                in_frontmatter = False
                for i, line in enumerate(lines):
                    if i == 0 and line.strip() == '---':
                        in_frontmatter = True
                        continue
                    if in_frontmatter and line.strip() == '---':
                        in_frontmatter = False
                        continue
                    if in_frontmatter:
                        continue
                        
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break
                
                # Extract first meaningful paragraph as description
                for i, line in enumerate(lines):
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('---') and \
                       not line.startswith('layout:') and not line.startswith('title:') and \
                       len(line) > 30:
                        description = line[:200] + ('...' if len(line) > 200 else '')
                        break
        except Exception as e:
            print(f"Warning: Error reading {filename}: {e}")
            title = filename.replace('.md', '')
            description = f"{report_type.title()} report for {date}"
        
        reports.append({
            'file': filename,
            'type': report_type,
            'date': date,
            'title': title,
            'description': description
        })
    
    # Sort by date descending (newest first)
    reports.sort(key=lambda x: x['date'], reverse=True)
    
    # Create output JSON
    output = {
        'reports': reports,
        'updated': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'),
        'count': len(reports)
    }
    
    # Write to index.json
    output_file = reports_dir / 'index.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated report index with {len(reports)} reports")
    print(f"   Output: {output_file}")
    print(f"   Updated: {output['updated']}")
    
    # Print summary
    lab_count = sum(1 for r in reports if r['type'] == 'lab')
    pulse_count = sum(1 for r in reports if r['type'] == 'pulse')
    print(f"   Lab reports: {lab_count}")
    print(f"   Pulse reports: {pulse_count}")
    
    return output

if __name__ == '__main__':
    generate_report_index()
