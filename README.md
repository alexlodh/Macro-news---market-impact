# Macro News Agent

An automated agentic loop that observes macroeconomic headlines, reasons about their market impact using an LLM, and acts by producing a structured impact report. It also reflects on its own output to adjust sensitivity.

## Architecture

- **Observe**: Fetches RSS feeds (Reuters, BBC, Economist, etc.).
- **Reason**: Deduplicates items using SQLite and classifies them (Topic, Stance, Relevance, Impact) using `LangChain` + `OpenAI` structured output.
- **Act**: Generates a markdown report categorized by relevance (High/Med/Low).
- **Reflect**: Critiques the report and auto-adjusts a `relevance_threshold` in `data/config.json`.

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
Fetches news, classifies new items, generates a report, and reflects.
```bash
python -m src.main run
```

**2. List Saved Reports:**
```bash
python -m src.main list
```

**3. Show a Report:**
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
