# Updated System Workflow with Investment Recommendations

```
┌─────────────────────────────────────────────────────────────────┐
│                      MACRO NEWS AGENT                            │
│                   (Enhanced with Investment Recommendations)     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────┐
│  1. OBSERVE │  Fetch RSS Feeds (Reuters, BBC, Economist, etc.)
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  2. DEDUPLICATE     │  Check fingerprint against SQLite DB
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  3. LOCAL NLP       │  SpaCy NER + Transformers Sentiment
└──────┬──────────────┘
       │
       ▼
┌───────────────────────────────────────────────────────────────┐
│  4. LLM CLASSIFICATION & INVESTMENT ANALYSIS                  │
│                                                                │
│  Input: Headline + Summary                                     │
│                                                                │
│  Outputs:                                                      │
│  ├─ Market Classification                                      │
│  │  ├─ Topic (inflation, growth, central banks, etc.)         │
│  │  ├─ Stance (hawkish/dovish/neutral)                        │
│  │  ├─ Relevance Score (1-10)                                 │
│  │  ├─ Expected Impact (rates/equities/FX)                    │
│  │  └─ Impact Direction & Rationale                           │
│  │                                                             │
│  └─ Investment Recommendations ★ NEW ★                         │
│     ├─ Ticker Symbol (AAPL, MSFT, etc.)                       │
│     ├─ Company Name                                            │
│     ├─ Action (buy/sell/hold)                                  │
│     ├─ Rationale (based on news impact)                        │
│     ├─ Timeframe (short/medium/long-term)                      │
│     ├─ Risk Level (low/medium/high)                            │
│     └─ Price Target (optional)                                 │
└───────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  5. STORE                                                     │
│                                                                │
│  Save to SQLite:                                               │
│  - Headline                                                    │
│  - Classification                                              │
│  - Investment Recommendations (JSON)                           │
│  - NLP entities & sentiment                                    │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  6. GENERATE REPORT                                           │
│                                                                │
│  Markdown Report Structure:                                    │
│                                                                │
│  ┌──────────────────────────────────────────┐                │
│  │ 📊 Investment Recommendations ★ NEW ★   │                │
│  │                                           │                │
│  │  🟢 BUY:                                 │                │
│  │  • AAPL: Strong earnings, +5-7% target  │                │
│  │  • NVDA: AI chip demand, long-term      │                │
│  │                                           │                │
│  │  🔴 SELL:                                │                │
│  │  • INTC: Manufacturing issues, -10%     │                │
│  │                                           │                │
│  │  🟡 HOLD:                                │                │
│  │  • META: Wait for earnings clarity      │                │
│  └──────────────────────────────────────────┘                │
│  ┌──────────────────────────────────────────┐                │
│  │ Top 3 Items (High Relevance)            │                │
│  └──────────────────────────────────────────┘                │
│  ┌──────────────────────────────────────────┐                │
│  │ Worth a Glance (Medium)                  │                │
│  └──────────────────────────────────────────┘                │
│  ┌──────────────────────────────────────────┐                │
│  │ Noise (Low)                              │                │
│  └──────────────────────────────────────────┘                │
└──────┬──────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  7. REFLECT                                                   │
│                                                                │
│  LLM analyzes report quality:                                  │
│  - Too much noise?                                             │
│  - Missing important items?                                    │
│  - Signal-to-noise ratio OK?                                   │
│  - Recommendation quality?  ★ NEW CONSIDERATION ★             │
│                                                                │
│  Adjust relevance threshold (±1) if needed                     │
│  Save adjustment to data/config.json                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  OUTPUT FILES                                                 │
│                                                                │
│  ├─ reports/report_YYYYMMDD_HHMMSS.md                         │
│  │  └─ Includes investment recommendations section            │
│  │                                                             │
│  ├─ data/headlines.db (SQLite)                                │
│  │  └─ Stores all classifications & recommendations           │
│  │                                                             │
│  └─ data/config.json                                           │
│     └─ Updated relevance threshold                             │
└─────────────────────────────────────────────────────────────┘
```

## Key Enhancements

### ★ Investment Recommendations
- **Integrated into classification step** - No additional API calls
- **Stock-specific actions** - Clear buy/sell/hold signals
- **Risk-aware** - Includes timeframe and risk assessment
- **Actionable** - Provides rationale and price targets

### Data Flow
1. News → Classification → **Investment Analysis** → Storage
2. All recommendations stored in SQLite as part of classification
3. Reports consolidate recommendations from multiple news items
4. Grouped by action type (Buy/Sell/Hold) for easy scanning

### Example Usage

```bash
# Run full cycle with investment recommendations
python -m src.main run

# Test the feature with a sample headline
python test_recommendations.py

# View generated report with recommendations
python -m src.main show report_20260212_143022.md
```

## Benefits

✅ **Automated Trading Signals** - No manual analysis needed  
✅ **Context-Rich** - Recommendations tied to specific news events  
✅ **Risk-Assessed** - Each recommendation includes risk level  
✅ **Time-Scoped** - Clear timeframe expectations  
✅ **Transparent** - Full rationale provided for each recommendation  
✅ **Consolidated View** - All recommendations in one section  

## Extensibility

The system is designed to be extended:
- Add sector correlation analysis
- Integrate with portfolio management tools
- Track recommendation performance
- Add technical indicators
- Build automated trading system
- Create watchlists from recommendations

---

*Enhanced workflow diagram - February 12, 2026*
