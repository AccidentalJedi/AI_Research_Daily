# 📡 Ollama Pulse

**A Complete, Self-Sustaining Innovation Miner Built on GitHub**

Ollama Pulse is a GitHub-native ecosystem radar that continuously scans the Ollama world for signals, mines patterns, and generates actionable intelligence—all without servers or costs beyond GitHub's free tier.

## 🎯 What It Does

- **Polls 10 Sources**: Ollama blog, Cloud API, GitHub Issues/PRs/Code, Reddit, Hacker News, YouTube, HuggingFace, Newsletters, Bounties, Nostr NIP-23
- **Turbo-Centric Focus**: Every item scored for Ollama Turbo/Cloud relevance (0-1 scale)
- **Mines Deep Insights**: Embeddings + clustering to detect patterns and trends
- **Dynamic Intelligence**: Generates adaptive search queries based on yesterday's patterns
- **EchoVein Persona**: Vein-tapping oracle with 4 adaptive report styles
- **Prophetic Analysis**: Confidence-scored inferences about emerging trends
- **Auto-Deploys**: Publishes to GitHub Pages with rich, actionable reports
- **Zero Maintenance**: Runs forever on GitHub Actions (2,000 free minutes/month)
- **Nostr Integration**: Auto-publishes reports to Nostr network with NIP-23 long-form content

## 🏗️ Architecture

```
ollama_pulse/
├── .github/workflows/
│   ├── ingest.yml          # Hourly ingestion + parallel Turbo-deep job
│   └── daily_report.yml    # Daily EchoVein report generation
├── scripts/
│   ├── ingest_official.py  # Blog RSS, /cloud page
│   ├── ingest_cloud.py     # Deep Ollama Cloud/Turbo models
│   ├── ingest_community.py # Reddit, HN, YouTube, HuggingFace, Newsletters
│   ├── ingest_issues.py    # GitHub Issues/PRs search
│   ├── ingest_tools.py     # n8n, GitHub integrations
│   ├── ingest_bounties.py  # 🆕 Bounty platforms (Bountycaster, etc.)
│   ├── ingest_nostr.py     # 🆕 Nostr NIP-23 long-form content
│   ├── post_to_nostr.py    # 🆕 Auto-publish reports to Nostr
│   ├── aggregate.py        # Turbo-scoring + yield metrics
│   ├── mine_insights.py    # Dynamic queries + pattern detection
│   └── generate_report.py  # EchoVein persona with adaptive tone
├── data/
│   ├── official/           # {date}.json from blog/cloud/API
│   ├── community/          # {date}.json from 6+ social sources
│   ├── tools/              # {date}.json from integrations
│   ├── bounties/           # 🆕 {date}.json from bounty platforms
│   ├── nostr/              # 🆕 {date}.json from Nostr network
│   ├── aggregated/         # {date}.json with turbo_scores
│   └── insights/           # {date}.json + {date}_yield.json
├── assets/
│   ├── kofi-qr.png         # 🆕 Ko-fi donation QR code
│   └── lightning-qr.png    # 🆕 Lightning Network QR code
├── docs/reports/
│   └── pulse-{date}.md     # EchoVein vein-map reports
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/Grumpified-OGGVCT/ollama_pulse.git
cd ollama_pulse
pip install -r requirements.txt
```

### 2. Enable GitHub Actions
- Go to Settings → Actions → General
- Enable "Read and write permissions"

### 3. Enable GitHub Pages
- Go to Settings → Pages
- Source: main branch, Folder: /reports

### 4. Test Locally
```bash
python scripts/ingest_official.py
python scripts/aggregate.py
python scripts/mine_insights.py
python scripts/generate_report.py
```

## 📊 Example Output (EchoVein Style)

**From October 23, 2025:**

```markdown
# 🩸 Ollama Pulse – 2025-10-23
## Vein Rush: High-Density Pattern Surge

*EchoVein here, your vein-tapping oracle excavating Ollama's hidden arteries...*

**Today's Vibe**: Vein Rush — The ecosystem is pulsing with fresh blood.

### 🔬 Vein Analysis: Quick Stats
- **Total Ore Mined**: 50 items tracked
- **High-Purity Veins**: 35 Turbo-focused items (score ≥0.7)
- **Pattern Arteries**: 5 detected
- **Prophetic Insights**: 8 inferences drawn

### 🎯 Official Veins: What Ollama Team Pumped Out
| Date | Vein Strike | Source | Turbo Score | Dig In |
|------|-------------|--------|-------------|--------|
| 2025-10-23 | Cloud Model: gpt-oss-120b-cloud | cloud_api | 0.9 | [⛏️](link) |

### 📈 Vein Pattern Mapping
🩸 **Vein Bulging**: 5 Voice Integration Signals — 2x Use-Case Explosion Incoming?

### 🔔 Prophetic Veins: What This Means
🩸 **Vein Oracle: Cloud Models**
- **Surface Reading**: 5 items detected
- **Vein Prophecy**: Emerging trend - scale to 2x more use-cases
- **Confidence Vein**: HIGH (🩸)
- **EchoVein's Take**: This vein's *throbbing* — trust the flow.

### Today's Vein Yield
- **Total Items Scanned**: 150
- **High-Relevance Veins**: 50
- **Quality Ratio**: 0.33

*Built by vein-tappers, for vein-tappers. Dig deeper. Ship harder.* ⛏️🩸
```

## 🆕 New Features: Expanded Sourcing & EchoVein

### 🎯 Turbo-Centric Intelligence
Every item gets a **relevance score** (0-1) based on Ollama Turbo/Cloud keywords:
- **≥0.7** = High-purity ore (featured prominently)
- **≥0.5** = Medium relevance
- **≥0.3** = Included in aggregation
- **<0.3** = Filtered out

**Scoring factors**: turbo, cloud, -cloud suffix, voice/STT/TTS, multimodal, API integrations, model names

### 🩸 EchoVein Persona (4 Adaptive Modes)

Reports automatically adapt tone based on daily patterns:

1. **Vein Rush** (🩸) - High-density surge (3+ voice/multimodal items)
   - *Electric, prophetic, hyped about the flow*
   
2. **Artery Audit** (⚙️) - Steady maintenance (incremental tools/fixes)
   - *Grounded, practical, appreciative of "essential grime"*
   
3. **Fork Phantom** (🤖) - Niche oddities (zero-star experimental hacks)
   - *Playful, probing, unpacking weirdness with "what if" veins*
   
4. **Deep Vein Throb** (📍) - Slow days (aggregated trends)
   - *Reflective, prospector mode, weekly artery forecasting*

### 📡 Expanded Sources (10 Total)

**Official Sources:**
- Ollama Blog RSS
- /cloud page scraping
- Cloud API for Turbo models

**Community Sources:**
- Reddit r/ollama
- GitHub Issues/PRs search
- GitHub Code search (via Actions)
- Hacker News (Algolia API)
- YouTube videos (RSS)
- HuggingFace discussions
- Newsletters (RSS)

**Bounty & Decentralized Sources:**
- 🆕 Bounty platforms (Bountycaster, etc.)
- 🆕 Nostr NIP-23 long-form content

### 🔮 Dynamic Intelligence

- **Pattern-Based Queries**: System generates new search queries based on yesterday's trends
- **Yield Metrics**: Tracks quality ratio (high-relevance/total items)
- **Confidence Scoring**: All inferences labeled HIGH/MEDIUM/LOW
- **Vein Commentary**: Contextual analysis for significant patterns (≥5 items)

## 🔗 Integration with Ollama Proxy

Access via: `http://127.0.0.1:8081/admin/pulse`

## 🌐 Nostr Integration

Ollama Pulse automatically publishes daily reports to the Nostr decentralized network using NIP-23 (long-form content).

**Nostr Account:**
- **npub**: `npub1grumpifiedoggvct...` (EchoVein Oracle)
- **Profile**: Vein-tapping oracle excavating Ollama's hidden arteries

**Features:**
- **Ingestion**: Monitors Nostr for Ollama-related NIP-23 articles via `ingest_nostr.py`
- **Auto-Publishing**: Posts daily EchoVein reports to Nostr via `post_to_nostr.py`
- **Discoverability**: Tagged with `#ollama`, `#ai`, `#echovein` for community reach
- **Decentralized Archive**: Permanent, censorship-resistant report storage

**How It Works:**
1. Daily report generated at 4 PM CT
2. Converted to NIP-23 format (long-form markdown)
3. Published to Nostr relays (wss://relay.damus.io, wss://nos.lol, etc.)
4. Includes donation links (Ko-fi, Lightning) in footer

## 💰 Support the Project

If Ollama Pulse helps you stay ahead of the ecosystem, consider supporting development:

**Ko-fi (Fiat/Card):**
- Link: https://ko-fi.com/grumpified
- QR Code: ![Ko-fi QR](assets/kofi-qr.png)

**Lightning Network (Bitcoin):**
- Address: `lnbc1...` (see QR code)
- QR Code: ![Lightning QR](assets/lightning-qr.png)

**Why Support?**
- Keeps the project maintained and updated
- Funds new data source integrations
- Supports open-source AI tooling

*All donations go directly to maintaining Ollama Pulse and related open-source projects.*

## 🩸 EchoVein Lingo Legend

The EchoVein persona uses unique terminology to describe ecosystem patterns. Here's your decoder ring:

| Term | Meaning | Example |
|------|---------|---------|
| **Vein** | A signal, trend, or data point | "5 voice integration veins detected" |
| **Ore** | Raw data items collected | "50 ore mined today" |
| **High-Purity Vein** | Turbo-relevant item (score ≥0.7) | "35 high-purity veins" |
| **Vein Rush** | High-density pattern surge | "Vein Rush mode activated" |
| **Artery Audit** | Steady maintenance updates | "Artery Audit: incremental fixes" |
| **Fork Phantom** | Niche experimental projects | "Fork Phantom: zero-star oddities" |
| **Deep Vein Throb** | Slow-day aggregated trends | "Deep Vein Throb: weekly forecast" |
| **Vein Bulging** | Emerging pattern (≥5 items) | "Vein Bulging: voice integration" |
| **Vein Oracle** | Prophetic inference | "Vein Oracle: Cloud Models trending" |
| **Vein Prophecy** | Predicted trend direction | "Scale to 2x more use-cases" |
| **Confidence Vein** | Inference confidence level | "HIGH (🩸), MEDIUM (⚙️), LOW (🤖)" |
| **Vein Yield** | Quality ratio metric | "0.33 yield (50/150 items)" |
| **Vein-Tapping** | Mining/extracting insights | "Vein-tapping oracle at work" |
| **Artery** | Major trend pathway | "Pattern arteries detected" |
| **Vein Strike** | Significant discovery | "Vein Strike: new Cloud model" |
| **Throbbing Vein** | High-confidence signal | "This vein's throbbing—trust it" |
| **Vein Map** | Daily report structure | "Today's vein map" |
| **Dig In** | Link to source/details | "[⛏️ Dig In](link)" |

**Tone Indicators:**
- 🩸 = Vein Rush (electric, prophetic)
- ⚙️ = Artery Audit (grounded, practical)
- 🤖 = Fork Phantom (playful, probing)
- 📍 = Deep Vein Throb (reflective, prospector)

## 📄 License

MIT License

---

**Live Dashboard**: https://grumpified-oggvct.github.io/ollama_pulse
**Repository**: https://github.com/Grumpified-OGGVCT/ollama_pulse

