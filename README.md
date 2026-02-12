# Macro News Agent

An automated agentic loop that observes macroeconomic headlines, reasons about their market impact using an LLM, generates **investment recommendations** (buy/sell/hold specific companies), and produces a structured impact report. It also reflects on its own output to adjust sensitivity.

## Architecture

- **Observe**: Fetches RSS feeds (Reuters, BBC, Economist, etc.).
- **Reason**: Deduplicates items using SQLite, enriches them with local NLP (NER via SpaCy + Sentiment via Transformers), and classifies them (Impact, Relevance) using `LangChain` + `OpenAI`.
- **Investment Analysis**: Generates specific buy/sell/hold recommendations for companies mentioned or impacted by the news, including ticker symbols, rationale, timeframes, and risk levels.
- **Act**: Generates a markdown report with investment recommendations and news categorized by relevance (High/Med/Low).
- **Reflect**: Critiques the report and auto-adjusts a `relevance_threshold` in `data/config.json`.

## Key Features

✅ **Investment Recommendations**: Automatically generates actionable buy/sell/hold signals for specific stocks based on news analysis  
✅ **Risk Assessment**: Each recommendation includes timeframe (short/medium/long-term) and risk level (low/medium/high)  
✅ **Ticker Symbols**: Precise company identification with stock ticker symbols  
✅ **Price Targets**: Optional price target expectations for recommendations  
✅ **Consolidated View**: Reports group all recommendations by action type (Buy/Sell/Hold) for easy decision-making

## Setup

1. **Prerequisites**: Python 3.11+.
2. **Installation**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment**:
   The project requires an OpenAI API Key. Add your OpenAI key to the .env file
   ```
   OPENAI_API_KEY=sk-...
   ```

## Usage

**1. Run the Agent Cycle:**
Fetches news, classifies new items, generates investment recommendations, creates a report, and reflects.
```bash
python -m src.main run
```

**2. Test Investment Recommendations:**
Run a quick test to see how the system analyzes news and generates buy/sell/hold recommendations:
```bash
python test_recommendations.py
```

**3. List Saved Reports:**
```bash
python -m src.main list
```

**4. Show a Report:**
```bash
python -m src.main show report_YYYYMMDD_HHMMSS.md
```

## Configuration

- **Feeds**: Defined in `src/config.py`.
- **Threshold**: Stored in `data/config.json`. Starts at 7. The agent will adjust this up/down based on whether the reports are too noisy or too empty.

## Testing

Run unit tests:
```bash
python -m unittest discover tests
```

## Extension Steps

- **Add Feeds**: Edit `DEFAULT_FEEDS` in `src/config.py`.
- **Add Economic Calendar**: create a new fetcher in `src/fetchers.py` that scrapes a calendar site or uses an API, returning `Headline` objects with a specific tag.
- **Customize Recommendations**: Modify the `InvestmentRecommendation` model in `src/models.py` to include additional fields like sector, market cap, or technical indicators.
- **Portfolio Integration**: Build a tracker that aggregates recommendations across reports to maintain a model portfolio.

## Investment Recommendation Structure

Each recommendation includes:
- **Ticker**: Stock symbol (e.g., AAPL, MSFT, GOOGL)
- **Company Name**: Full company name
- **Action**: buy, sell, or hold
- **Rationale**: Detailed explanation based on the news impact
- **Timeframe**: short-term (days), medium-term (weeks), or long-term (months)
- **Risk Level**: low, medium, or high
- **Price Target** (optional): Expected price movement or target price

Example recommendation:
```json
{
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "action": "buy",
  "rationale": "Strong earnings beat and raised guidance indicate continued growth momentum",
  "timeframe": "medium-term",
  "risk_level": "medium",
  "price_target": "+5-7% over next 3 months"
}
```
