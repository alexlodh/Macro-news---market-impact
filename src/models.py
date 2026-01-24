from typing import Optional, List
from pydantic import BaseModel, Field

class Headline(BaseModel):
    source: str
    title: str
    url: str
    summary: str
    published: str
    fingerprint: str  # Unique hash for deduplication

class Classification(BaseModel):
    topic: str = Field(..., description="inflation, growth, labour, central banks, fiscal, geopolitics, or other")
    stance: str = Field(..., description="hawkish, dovish, or neutral")
    relevance: str = Field(..., description="high, medium, or low")
    relevance_score: int = Field(..., description="Integer score 1-10 for sorting")
    expected_impact: str = Field(..., description="rates, equities, or FX")
    impact_direction: str = Field(..., description="Brief direction e.g., 'Bullish USD', 'Bearish Equities'")
    rationale: str = Field(..., description="Short explanation of the impact")
    confidence: str = Field(..., description="low, medium, or high")

class ClassifiedItem(Headline):
    classification: Classification
