import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from src.config import settings
from src.models import ClassifiedItem, Headline, Classification

class Storage:
    def __init__(self):
        self.conn = sqlite3.connect(str(settings.db_path))
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                fingerprint TEXT PRIMARY KEY,
                source TEXT,
                title TEXT,
                url TEXT,
                summary TEXT,
                published TEXT,
                topic TEXT,
                stance TEXT,
                relevance TEXT,
                relevance_score INTEGER,
                expected_impact TEXT,
                impact_direction TEXT,
                rationale TEXT,
                confidence TEXT,
                fetched_at TIMESTAMP
            )
        ''')
        self.conn.commit()

    def is_duplicate(self, fingerprint: str) -> bool:
        self.cursor.execute("SELECT 1 FROM articles WHERE fingerprint = ?", (fingerprint,))
        return self.cursor.fetchone() is not None

    def save_item(self, item: ClassifiedItem):
        c = item.classification
        self.cursor.execute('''
            INSERT OR REPLACE INTO articles (
                fingerprint, source, title, url, summary, published,
                topic, stance, relevance, relevance_score,
                expected_impact, impact_direction, rationale, confidence,
                fetched_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.fingerprint, item.source, item.title, item.url, item.summary, item.published,
            c.topic, c.stance, c.relevance, c.relevance_score,
            c.expected_impact, c.impact_direction, c.rationale, c.confidence,
            datetime.now()
        ))
        self.conn.commit()

    def get_recent_items(self, limit: int = 50) -> List[ClassifiedItem]:
        # Retrieve recent items for context or history (reconstruct ClassifiedItem objects)
        self.cursor.execute(
            "SELECT fingerprint, source, title, url, summary, published, topic, stance, relevance, relevance_score, expected_impact, impact_direction, rationale, confidence FROM articles ORDER BY fetched_at DESC LIMIT ?",
            (limit,)
        )
        rows = self.cursor.fetchall()
        items: List[ClassifiedItem] = []
        for r in rows:
            (
                fingerprint, source, title, url, summary, published,
                topic, stance, relevance, relevance_score,
                expected_impact, impact_direction, rationale, confidence
            ) = r

            classification = Classification(
                topic=topic or "other",
                stance=stance or "neutral",
                relevance=relevance or "low",
                relevance_score=int(relevance_score or 1),
                expected_impact=expected_impact or "equities",
                impact_direction=impact_direction or "",
                rationale=rationale or "",
                confidence=confidence or "low",
            )

            item = ClassifiedItem(
                source=source,
                title=title,
                url=url,
                summary=summary,
                published=published,
                fingerprint=fingerprint,
                classification=classification,
            )
            items.append(item)
        return items

    def close(self):
        self.conn.close()
