# 🚀 The Lab Deployment Guide

Complete step-by-step guide to deploy The Lab - AI Research Daily to GitHub.

## 📋 Prerequisites

- GitHub account
- Git installed locally
- Python 3.11+ installed
- Repository: https://github.com/AccidentalJedi/AI_Research_Daily

## 🔧 Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/AccidentalJedi/AI_Research_Daily.git
cd AI_Research_Daily

# Install Python dependencies
pip install -r requirements.txt
```

## 📁 Step 2: Repository Structure

The Lab uses this structure:

```
AI_Research_Daily/
├── README.md
├── THE_LAB_DESIGN_DOCUMENT.md
├── DEPLOYMENT_GUIDE.md
├── requirements.txt
├── .github/
│   └── workflows/
│       ├── ingest.yml
│       └── daily_report.yml
├── scripts/
│   ├── ingest_arxiv.py
│   ├── ingest_huggingface.py
│   ├── ingest_paperswithcode.py
│   ├── aggregate.py
│   ├── mine_insights.py
│   └── generate_report.py
├── data/
│   ├── arxiv/.gitkeep
│   ├── huggingface/.gitkeep
│   ├── paperswithcode/.gitkeep
│   ├── aggregated/.gitkeep
│   └── insights/.gitkeep
└── docs/
    └── reports/
```

## 🔑 Step 3: Configure GitHub

### Enable GitHub Actions

1. Go to Repository Settings → Actions → General
2. Under "Workflow permissions", select:
   - ✅ Read and write permissions
   - ✅ Allow GitHub Actions to create and approve pull requests
3. Click "Save"

### Enable GitHub Pages

1. Go to Repository Settings → Pages
2. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/docs**
3. Click "Save"

## 📦 Step 4: Create .gitkeep Files

```bash
# Create empty .gitkeep files to preserve directory structure
touch data/arxiv/.gitkeep
touch data/huggingface/.gitkeep
touch data/paperswithcode/.gitkeep
touch data/aggregated/.gitkeep
touch data/insights/.gitkeep
touch docs/reports/.gitkeep
```

## 🚀 Step 5: Initial Commit and Push

```bash
# Add all files
git add .

# Commit
git commit -m "Initial The Lab setup - AI research intelligence platform"

# Push to GitHub
git push origin main
```

## ✅ Step 6: Test Workflow

### Manual Trigger

1. Go to Repository → Actions tab
2. Click "The Lab Research Ingestion" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait for completion (~3-5 minutes)

### Verify Output

1. Check the Actions tab for green checkmark
2. Navigate to the `data/` directory
3. Verify JSON files were created in:
   - `data/arxiv/`
   - `data/huggingface/`
   - `data/paperswithcode/`
   - `data/aggregated/`
   - `data/insights/`
4. Check `docs/reports/` for generated Markdown

## 🌐 Step 7: Verify GitHub Pages

1. Wait 2-3 minutes for Pages to deploy
2. Visit: https://accidentaljedi.github.io/AI_Research_Daily
3. You should see The Lab research intelligence reports!

## 🧪 Step 8: Test Locally

```bash
# Test the complete pipeline locally
python scripts/ingest_arxiv.py
python scripts/ingest_huggingface.py
python scripts/ingest_paperswithcode.py
python scripts/aggregate.py
python scripts/mine_insights.py
python scripts/generate_report.py

# Check generated files
ls -la data/aggregated/
ls -la data/insights/
ls -la docs/reports/
```

## 📅 Step 9: Verify Automation

The workflows run automatically:

**Research Ingestion**: Every 6 hours
```yaml
schedule:
  - cron: '0 */6 * * *'
```

**Daily Report**: Daily at 4 PM Central Time
```yaml
schedule:
  - cron: '0 21 * * *'   # 16:00 CDT
  - cron: '0 22 * * *'   # 16:00 CST
```

**Next run**: Check Actions tab at scheduled times

## 🐛 Troubleshooting

### Workflow Fails

1. Check Actions tab for error logs
2. Common issues:
   - Missing dependencies → Check requirements.txt
   - Permission denied → Verify workflow permissions
   - API rate limits → Add delays in scripts

### GitHub Pages Not Updating

1. Check Settings → Pages is enabled
2. Verify `/reports` folder has content
3. Wait 2-3 minutes for deployment
4. Check Actions tab for "pages build and deployment" workflow

### No Data Generated

1. Run scripts locally first:
   ```bash
   python scripts/ingest_arxiv.py
   python scripts/ingest_huggingface.py
   python scripts/aggregate.py
   python scripts/mine_insights.py
   python scripts/generate_report.py
   ```
2. Check for errors
3. Verify internet connection
4. Check API rate limits (especially for Papers with Code)

## 📊 Monitoring

### Check Workflow Status

```bash
# View latest workflow run
gh run list --repo AccidentalJedi/AI_Research_Daily

# View workflow logs
gh run view --repo AccidentalJedi/AI_Research_Daily
```

### Check Data Growth

```bash
# Count JSON files
find data -name "*.json" | wc -l

# View latest report
cat docs/reports/lab-$(date +%Y-%m-%d).md
```

## 🎉 Success Criteria

- ✅ Repository has all files
- ✅ GitHub Actions enabled with write permissions
- ✅ GitHub Pages enabled and deployed
- ✅ Workflows run successfully (green checkmark)
- ✅ Research data files generated in `data/` folders
- ✅ Reports generated in `docs/reports/`
- ✅ GitHub Pages shows reports at https://accidentaljedi.github.io/AI_Research_Daily
- ✅ The Scholar persona is consistent across reports
- ✅ arXiv, HuggingFace, Papers with Code data being collected

## 🔄 Ongoing Maintenance

### Update Scripts

```bash
# Edit scripts locally
nano scripts/ingest_arxiv.py

# Test locally
python scripts/ingest_arxiv.py

# Commit and push
git add scripts/
git commit -m "Update research ingestion logic"
git push
```

### Monitor Usage

- GitHub Actions: 2,000 free minutes/month
- Research ingestion: ~8 min/run × 4 runs/day = 32 min/day
- Daily report: ~3 min/run × 1 run/day = 3 min/day
- Monthly: ~1,050 minutes (well within limit)

### Add New Sources

1. Create new ingestion script in `scripts/`
2. Update `.github/workflows/ingest.yml` to call it
3. Test locally
4. Commit and push

## 📚 Resources

- **Repository**: https://github.com/AccidentalJedi/AI_Research_Daily
- **GitHub Pages**: https://accidentaljedi.github.io/AI_Research_Daily
- **Design Document**: [THE_LAB_DESIGN_DOCUMENT.md](THE_LAB_DESIGN_DOCUMENT.md)
- **arXiv API**: https://arxiv.org/help/api
- **HuggingFace API**: https://huggingface.co/docs/hub/api
- **Papers with Code API**: https://paperswithcode.com/api/v1/docs/
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **GitHub Pages Docs**: https://docs.github.com/en/pages

---

**Last Updated**: 2025-10-23  
**Status**: Production-Ready  
**Estimated Setup Time**: 20-30 minutes

