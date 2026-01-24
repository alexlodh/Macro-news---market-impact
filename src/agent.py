import time
import json
from datetime import datetime
from typing import List
from src.config import settings, DATA_DIR, CONFIG_FILE
from src.fetchers import fetch_all_feeds
from src.storage import Storage
from src.classify import classify_item, generate_report_content, reflect_on_run
from src.models import ClassifiedItem

class MacroAgent:
    def __init__(self):
        self.storage = Storage()

    def run_cycle(self):
        print("--- Starting Agent Cycle ---")
        
        # 1. OBSERVE
        raw_headlines = fetch_all_feeds(settings.feeds)
        print(f"Fetched {len(raw_headlines)} items.")

        # 2. REASON (Dedupe & Classify)
        new_items: List[ClassifiedItem] = []
        
        for h in raw_headlines:
            if self.storage.is_duplicate(h.fingerprint):
                continue
            
            print(f"Classifying: {h.title}")
            classification = classify_item(h)
            
            item = ClassifiedItem(**h.dict(), classification=classification)
            self.storage.save_item(item)
            new_items.append(item)
            
            # Simple rate limit to be nice to API
            # time.sleep(0.5) 

        print(f"Processed {len(new_items)} new unique items.")
        
        meta_path = DATA_DIR / "last_report_meta.json"

        if not new_items:
            # If threshold changed since last report, still generate a new report
            last_threshold = None
            if meta_path.exists():
                try:
                    with open(meta_path, 'r') as mf:
                        meta = json.load(mf)
                        last_threshold = meta.get('threshold')
                except Exception:
                    last_threshold = None

            regenerate = False
            if last_threshold is not None:
                try:
                    if int(last_threshold) != int(settings.relevance_threshold):
                        regenerate = True
                except Exception:
                    regenerate = True
            else:
                # No meta file found — assume we should generate at least once to capture current threshold
                # (This handles first-run or if metadata was removed.)
                regenerate = True

            if regenerate:
                print("No new items, but relevance threshold changed or no prior metadata — regenerating report using recent items.")
                report_items = self.storage.get_recent_items(limit=50)
                # Sort by relevance score
                report_items.sort(key=lambda x: x.classification.relevance_score, reverse=True)
            else:
                print("No new items to report.")
                return
        else:
            report_items = new_items

        # Filter based on threshold for the report
        # We assume items below threshold are effectively filtered out of the "Main Report" 
        # but maybe we keep a few for the "Noise" section if they are close.
        # For this implementation, we simply pass all new items to the report generator,
        # but we iterate them in the prompt, or we sort them.
        # Let's sort by score descending.
        new_items.sort(key=lambda x: x.classification.relevance_score, reverse=True)

        # 3. ACT (Report)
        print("Generating Report...")
        report_content = generate_report_content(report_items)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"report_{timestamp}.md"
        report_path = settings.REPORTS_DIR / report_filename
        
        with open(report_path, "w") as f:
            f.write(f"# Macro Market Impact Report - {timestamp}\n\n")
            f.write(f"**Relevance Threshold used:** {settings.relevance_threshold}\n\n")
            if not report_items:
                f.write("No items available for this report.\n\n")
            f.write(report_content)
            
        print(f"Report saved to {report_path}")

        # Save meta about this report
        try:
            with open(meta_path, 'w') as mf:
                json.dump({"timestamp": timestamp, "threshold": settings.relevance_threshold}, mf)
        except Exception:
            pass

        # 4. REFLECT
        print("Reflecting...")
        reflection = reflect_on_run(report_content, new_items, settings.relevance_threshold)
        
        print(f"Critique: {reflection.critique}")
        if reflection.adjustment_suggestion != 0:
            new_threshold = max(1, min(10, settings.relevance_threshold + reflection.adjustment_suggestion))
            print(f"Adjusting threshold from {settings.relevance_threshold} to {new_threshold}")
            settings.update_threshold(new_threshold)
            
            # Append reflection to report
            with open(report_path, "a") as f:
                f.write(f"\n\n---\n## Agent Reflection\n")
                f.write(f"**Critique:** {reflection.critique}\n")
                f.write(f"**Action:** Adjusted relevance threshold to {new_threshold}\n")
        else:
            print("Threshold remains unchanged.")

    def list_reports(self, days: int = 7):
        # List files in report dir
        files = sorted(settings.REPORTS_DIR.glob("*.md"), reverse=True)
        print(f"Found {len(files)} reports:")
        for f in files:
            print(f"- {f.name}")

    def show_report(self, report_id: str):
        # Try to find file
        path = settings.REPORTS_DIR / report_id
        if not path.exists():
            print("Report NOT found.")
            return
        with open(path, 'r') as f:
            print(f.read())

if __name__ == "__main__":
    agent = MacroAgent()
    agent.run_cycle()
