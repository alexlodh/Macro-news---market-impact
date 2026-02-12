from typing import Optional, List
from pydantic import BaseModel, Field

class Headline(BaseModel):
    source: str
    title: str
    url: str
    summary: str
    published: str
    fingerprint: str  # Unique hash for deduplication

class InvestmentRecommendation(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, MSFT)")
    company_name: str = Field(..., description="Full company name")
    action: str = Field(..., description="buy, sell, or hold")
    rationale: str = Field(..., description="Why this action is recommended based on the news")
    timeframe: str = Field(..., description="short-term (days), medium-term (weeks), or long-term (months)")
    risk_level: str = Field(..., description="low, medium, or high")
    price_target: Optional[str] = Field(default=None, description="Optional price target or percentage move expectation")

class Classification(BaseModel):
    topic: str = Field(..., description="inflation, growth, labour, central banks, fiscal, geopolitics, or other")
    stance: str = Field(..., description="hawkish, dovish, or neutral")
    relevance: str = Field(..., description="high, medium, or low")
    relevance_score: int = Field(..., description="Integer score 1-10 for sorting")
    expected_impact: str = Field(..., description="rates, equities, or FX")
    impact_direction: str = Field(..., description="Brief direction e.g., 'Bullish USD', 'Bearish Equities'")
    rationale: str = Field(..., description="Short explanation of the impact")
    confidence: str = Field(..., description="low, medium, or high")

    # Investment recommendations
    investment_recommendations: Optional[List[InvestmentRecommendation]] = Field(
        default=None, 
        description="Specific stock recommendations based on this news"
    )

    # Local NLP augmentation
    entities: Optional[List[dict]] = Field(default=None, description="Extracted entities via local NLP")
    sentiment: Optional[dict] = Field(default=None, description="Sentiment analysis via local NLP")

class ClassifiedItem(Headline):
    classification: Classification
