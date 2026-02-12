# Quick Start Guide - Investment Recommendations

## What's New?

Your macro news agent now automatically generates **buy/sell/hold recommendations** for specific stocks based on news analysis!

## Quick Test

Run this to see it in action:
```bash
python test_recommendations.py
```

Expected output:
```
📰 Test Headline:
   Title: Apple reports record quarterly earnings...
   
🤖 Analyzing headline and generating recommendations...

✅ Classification Results:
   Topic: growth
   Relevance: high (Score: 9/10)
   Impact: Bullish Equities
   
💼 Investment Recommendations (1):

   1. BUY: AAPL (Apple Inc.)
      Rationale: Strong earnings beat and raised guidance...
      Timeframe: medium-term
      Risk Level: medium
      Price Target: +5-7% over next 3 months
```

## Using in Production

### 1. Run Normal Agent Cycle
```bash
python -m src.main run
```

This will:
- Fetch latest news
- Classify each item
- **Generate investment recommendations** ← NEW!
- Create report with recommendations section
- Save to `reports/report_YYYYMMDD_HHMMSS.md`

### 2. View Reports
```bash
# List all reports
python -m src.main list

# View specific report
python -m src.main show report_20260212_143022.md
```

## Report Structure

Reports now include a new first section:

```markdown
## Investment Recommendations

### 🟢 BUY Recommendations
- AAPL (Apple Inc.): Strong earnings → medium-term, medium risk
- NVDA (NVIDIA): AI chip demand → long-term, medium risk

### 🔴 SELL Recommendations  
- INTC (Intel): Manufacturing troubles → short-term, high risk

### 🟡 HOLD Recommendations
- META (Meta): Wait for earnings clarity → short-term, medium risk
```

## Understanding Recommendations

Each recommendation includes:

| Field | Description | Example |
|-------|-------------|---------|
| **Ticker** | Stock symbol | AAPL |
| **Company** | Full name | Apple Inc. |
| **Action** | What to do | buy, sell, hold |
| **Rationale** | Why | "Strong earnings beat..." |
| **Timeframe** | When | short/medium/long-term |
| **Risk Level** | How risky | low/medium/high |
| **Price Target** | Expected move | "+5-7% over 3 months" |

## Timeframe Guide

- **Short-term** (days): Quick trades, 1-5 days
- **Medium-term** (weeks): Swing trades, 1-8 weeks  
- **Long-term** (months): Position trades, 1-6+ months

## Risk Levels

- **Low**: Well-established, stable situations
- **Medium**: Normal market conditions, some uncertainty
- **High**: Volatile situations, significant downside risk

## When Recommendations Are Generated

The system generates recommendations when:
- ✅ News mentions specific companies
- ✅ News has material impact on a company
- ✅ There's actionable trading signal

No recommendations means:
- News is too general/macro-level
- No specific companies clearly impacted
- Insufficient information for action

## Integration Ideas

### Portfolio Tracker
Track recommendations over time:
```python
# Pseudo-code
recommendations = load_all_reports()
portfolio = {
    'AAPL': ['buy', 'buy', 'hold'],
    'INTC': ['sell', 'sell']
}
```

### Alert System
Get notified of new recommendations:
```python
# Pseudo-code  
if new_buy_recommendations:
    send_email(recommendations)
```

### Performance Tracking
Monitor recommendation accuracy:
```python
# Pseudo-code
recommendation_date = '2026-02-12'
current_price = get_price('AAPL')
original_price = get_historical_price('AAPL', recommendation_date)
performance = (current_price - original_price) / original_price
```

## API Costs

**No additional cost!** 
- Recommendations generated in same API call as classification
- Uses gpt-4o model (already configured)
- Same ~$0.005-0.01 per classification

## Customization

Want to modify recommendations? Edit these files:

**Model structure:** [src/models.py](src/models.py)
```python
class InvestmentRecommendation(BaseModel):
    # Add your custom fields here
    sector: str = Field(...)
    market_cap: str = Field(...)
```

**Prompt:** [src/classify.py](src/classify.py)
```python
classification_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert... [customize prompt]"),
    ...
])
```

**Report format:** [src/classify.py](src/classify.py) - `generate_report_content()`

## Troubleshooting

### No recommendations in report
- ✅ Normal! Not all news generates stock recommendations
- ✅ System is conservative - only recommends when confident
- ✅ Check if news mentions specific companies

### Wrong ticker symbols
- LLM occasionally makes mistakes
- Consider adding validation against a ticker database
- Price targets are estimates, not guarantees

### Too many/few recommendations
- Adjust by modifying the system prompt
- Add constraints like "max 3 recommendations per item"

## Disclaimer

⚠️ **Important:** 
- Recommendations are AI-generated, not financial advice
- Always do your own research
- Consider your risk tolerance
- Markets are unpredictable
- Past performance doesn't guarantee future results

## Next Steps

1. ✅ Test with sample data: `python test_recommendations.py`
2. ✅ Run full cycle: `python -m src.main run`
3. ✅ Review generated report
4. ✅ Build portfolio tracker (optional)
5. ✅ Add performance monitoring (optional)

## Support

See full documentation:
- [INVESTMENT_RECOMMENDATIONS_SUMMARY.md](INVESTMENT_RECOMMENDATIONS_SUMMARY.md)
- [WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md)
- [README.md](README.md)

---

*Quick Start Guide - February 12, 2026*
