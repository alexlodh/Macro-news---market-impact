import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
CONFIG_FILE = DATA_DIR / "config.json"

DEFAULT_FEEDS = [
    "https://www.reutersagency.com/feed/?best-sectors=business-finance&post_type=best", # Business & Finance
    "https://www.reuters.com/finance/economy?format=rss", # Economy
    "https://www.cnbc.com/id/100003114/device/rss/rss.html", # CNBC Top News & Analysis
    "http://feeds.bbci.co.uk/news/business/rss",
    "https://www.investing.com/rss/news_356.rss", # Economy
    "https://www.investing.com/rss/news_95.rss", # Forex
]

class Config:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.db_path = DATA_DIR / "macro_agent.db"
        self.feeds = DEFAULT_FEEDS
        self.relevance_threshold = 7 # Default score to catch 'High' and strong 'Medium' items
        self.REPORTS_DIR = REPORTS_DIR
        self._load_dynamic_config()

    def _load_dynamic_config(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.relevance_threshold = data.get("relevance_threshold", self.relevance_threshold)
            except Exception:
                pass

    def update_threshold(self, new_threshold: int):
        self.relevance_threshold = new_threshold
        with open(CONFIG_FILE, "w") as f:
            json.dump({"relevance_threshold": self.relevance_threshold}, f)

settings = Config()
