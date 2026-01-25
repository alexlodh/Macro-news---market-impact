from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from src.models import Headline, Classification, ClassifiedItem
from src.config import settings

# --- Local NLP Setup ---
_LOCAL_NLP = {"spacy": None, "sentiment": None, "initialized": False}

def init_local_nlp():
    """Try to initialize local NER and sentiment pipelines."""
    if _LOCAL_NLP["initialized"]:
        return
    _LOCAL_NLP["initialized"] = True
    
    # 1. SpaCy
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            from spacy.cli import download
            print("Downloading spacy model en_core_web_sm...")
            download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")
        _LOCAL_NLP["spacy"] = nlp
    except Exception as e:
        print(f"Local NLP: SpaCy init failed: {e}")
        _LOCAL_NLP["spacy"] = None

    # 2. Transformers Sentiment
    try:
        from transformers import pipeline
        _LOCAL_NLP["sentiment"] = pipeline(
            "sentiment-analysis", 
            model="distilbert-base-uncased-finetuned-sst-2-english",
            top_k=None # Return all scores to let us find top
        )
    except Exception as e: 
        print(f"Local NLP: Transformers init failed: {e}")
        _LOCAL_NLP["sentiment"] = None

def analyze_with_local_nlp(text: str) -> Dict[str, Any]:
    """Run local NER and sentiment analysis."""
    if not _LOCAL_NLP["initialized"]:
        init_local_nlp()

    result = {"entities": [], "sentiment": None}

    # NER with SpaCy
    nlp = _LOCAL_NLP.get("spacy")
    if nlp:
        try:
            doc = nlp(text)
            # Serialize entities to simple dicts
            result["entities"] = [
                {"text": ent.text, "label": ent.label_} 
                for ent in doc.ents
            ]
        except Exception as e:
            print(f"NER failed: {e}")

    # Sentiment with Transformers
    sent_pipe = _LOCAL_NLP.get("sentiment")
    if sent_pipe:
        try:
            # simple truncation to avoid tokenizer errors on long text
            s = sent_pipe(text[:512]) 
            # Output is often [[{'label': 'POSITIVE', 'score': 0.99}, ...]]
            if isinstance(s, list) and len(s) > 0:
                top = s[0]
                if isinstance(top, list): # handle list of lists
                     top = top[0]
                result["sentiment"] = {
                    "label": top.get("label"), 
                    "score": float(top.get("score", 0.0))
                }
        except Exception as e:
            print(f"Sentiment failed: {e}")

    return result

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o",  # or gpt-4-turbo, gpt-3.5-turbo if cost is concern
    temperature=0,
    api_key=settings.openai_api_key
)

# --- Classification Chain ---
classification_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert macroeconomic analyst. Your job is to analyze news headlines and assess their impact on financial markets (Rates, Equities, FX). You are hawkish/dovish aware."),
    ("human", "Analyze the following headline and provide a structured classification.\n\nSource: {source}\nTitle: {title}\nSummary: {summary}\n")
])

classifier_chain = classification_prompt | llm.with_structured_output(Classification)

def classify_item(headline: Headline) -> Classification:
    # 1. Run Local NLP first (low cost/offline)
    text_for_nlp = f"{headline.title}. {headline.summary}"
    nlp_result = analyze_with_local_nlp(text_for_nlp)
    
    try:
        # 2. Run LLM
        classification = classifier_chain.invoke({
            "source": headline.source,
            "title": headline.title,
            "summary": headline.summary
        })
        
        # 3. Augment with local NLP data
        classification.entities = nlp_result.get("entities")
        classification.sentiment = nlp_result.get("sentiment")
        
        return classification

    except Exception as e:
        print(f"Error classifying {headline.title}: {e}")
        # Fallback empty classification with local data if possible
        return Classification(
            topic="other", stance="neutral", relevance="low", relevance_score=1,
            expected_impact="equities", impact_direction="None", 
            rationale=f"Error in classification: {e}", confidence="low",
            entities=nlp_result.get("entities"),
            sentiment=nlp_result.get("sentiment")
        )

# --- Reporting Chain ---
# We just return a string for the report
report_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior market strategist writing a daily briefing."),
    ("human", """Here is a list of analyzed news items:
{items_text}

Produce a markdown report with these exact sections:
1. “Top 3 items (High relevance)” 
2. “Worth a glance (Medium)”
3. “Noise (Low)”

For each item, include 3–6 bullets covering: what happened, why it matters, expected market impact, and confidence.
Do not make up items. Only use the provided list.
""")
])

reporter_chain = report_prompt | llm

def generate_report_content(items: List[ClassifiedItem]) -> str:
    # Format items into a text block
    items_text = ""
    for idx, item in enumerate(items, 1):
        c = item.classification
        items_text += f"{idx}. [{c.relevance.upper()}] {item.title} ({item.source})\n"
        items_text += f"   Topic: {c.topic}, Impact: {c.impact_direction}\n"
        items_text += f"   Rationale: {c.rationale}\n"
        # Include local NLP outputs if present
        if getattr(c, 'entities', None):
            try:
                ents = ', '.join(f"{e.get('text')}({e.get('label')})" for e in c.entities)
                items_text += f"   Entities: {ents}\n"
            except Exception:
                pass
        if getattr(c, 'sentiment', None):
            try:
                items_text += f"   Sentiment: {c.sentiment.get('label')} (score: {c.sentiment.get('score')})\n"
            except Exception:
                pass
        items_text += "\n"
    
    response = reporter_chain.invoke({"items_text": items_text})
    return response.content

# --- Reflection Chain ---
class ReflectionOutput(BaseModel):
    critique: str = Field(..., description="Self-critique of the report content")
    adjustment_suggestion: int = Field(..., description="Suggested adjustment to relevance threshold (e.g. -1, 0, +1)")

reflection_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a supervisor reviewing a market report."),
    ("human", """Review the following report generated from these input items.
    
Report:
{report_content}

Input Items Count: {input_count}
Current Relevance Threshold: {current_threshold}

Critique the report:
- Did it include redundant items?
- Was any high relevance item missing context?
- Is the signal-to-noise ratio okay?

Suggest a numeric adjustment to the relevance threshold (currently {current_threshold}, scale 1-10).
If there is too much noise, suggest increasing the threshold (e.g. +1).
If important items were missed or the report is too empty, suggest decreasing (e.g. -1).
If good, suggest 0.
""")
])

reflector_chain = reflection_prompt | llm.with_structured_output(ReflectionOutput)

def reflect_on_run(report_content: str, items: List[ClassifiedItem], current_threshold: int) -> ReflectionOutput:
    return reflector_chain.invoke({
        "report_content": report_content,
        "input_count": len(items),
        "current_threshold": current_threshold
    })
