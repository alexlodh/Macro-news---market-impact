#!/usr/bin/env python3
"""
Test script to demonstrate investment recommendations feature.
This creates a sample headline and shows how the system now generates
buy/sell/hold recommendations for specific companies.
"""

from src.models import Headline, InvestmentRecommendation
from src.classify import classify_item
from datetime import datetime
import hashlib

def create_test_headline():
    """Create a test headline about company earnings."""
    title = "Apple reports record quarterly earnings, beats expectations on iPhone sales"
    summary = "Apple Inc. announced Q4 earnings that exceeded analyst expectations, driven by strong iPhone 15 sales and growing services revenue. The company also announced a share buyback program and raised forward guidance."
    
    # Create fingerprint for deduplication
    fingerprint = hashlib.md5(f"{title}{summary}".encode()).hexdigest()
    
    return Headline(
        source="Test Financial News",
        title=title,
        url="https://example.com/test",
        summary=summary,
        published=datetime.now().isoformat(),
        fingerprint=fingerprint
    )

def main():
    print("=" * 80)
    print("Testing Investment Recommendations Feature")
    print("=" * 80)
    
    # Create test headline
    headline = create_test_headline()
    print(f"\n📰 Test Headline:")
    print(f"   Title: {headline.title}")
    print(f"   Summary: {headline.summary}")
    
    # Classify the headline (this will call the LLM)
    print("\n🤖 Analyzing headline and generating recommendations...")
    print("   (This may take a few seconds...)")
    
    try:
        classification = classify_item(headline)
        
        print("\n✅ Classification Results:")
        print(f"   Topic: {classification.topic}")
        print(f"   Relevance: {classification.relevance} (Score: {classification.relevance_score}/10)")
        print(f"   Impact: {classification.impact_direction}")
        print(f"   Confidence: {classification.confidence}")
        print(f"   Rationale: {classification.rationale}")
        
        # Display investment recommendations
        if classification.investment_recommendations:
            print(f"\n💼 Investment Recommendations ({len(classification.investment_recommendations)}):")
            print("-" * 80)
            for i, rec in enumerate(classification.investment_recommendations, 1):
                print(f"\n   {i}. {rec.action.upper()}: {rec.ticker} ({rec.company_name})")
                print(f"      Rationale: {rec.rationale}")
                print(f"      Timeframe: {rec.timeframe}")
                print(f"      Risk Level: {rec.risk_level}")
                if rec.price_target:
                    print(f"      Price Target: {rec.price_target}")
        else:
            print("\n💼 Investment Recommendations: None generated for this headline")
        
        # Display NLP analysis if available
        if classification.entities:
            print(f"\n🏷️  Entities Detected: {len(classification.entities)}")
            for ent in classification.entities[:5]:  # Show first 5
                print(f"      - {ent.get('text')} ({ent.get('label')})")
        
        if classification.sentiment:
            print(f"\n😊 Sentiment: {classification.sentiment.get('label')} (confidence: {classification.sentiment.get('score'):.2f})")
        
        print("\n" + "=" * 80)
        print("✅ Test completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error during classification: {e}")
        print("\nMake sure you have:")
        print("  1. OpenAI API key configured in your environment")
        print("  2. Required packages installed (pip install -r requirements.txt)")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
