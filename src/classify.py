from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from src.models import Headline, Classification, ClassifiedItem
from src.config import settings

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
    try:
        return classifier_chain.invoke({
            "source": headline.source,
            "title": headline.title,
            "summary": headline.summary
        })
    except Exception as e:
        print(f"Error classifying {headline.title}: {e}")
        # Fallback empty classification
        return Classification(
            topic="other", stance="neutral", relevance="low", relevance_score=1,
            expected_impact="equities", impact_direction="None", rationale="Error in classification", confidence="low"
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
        items_text += f"{idx}. [{c.relevance.upper()}] {item.title} ({item.source})\n   Topic: {c.topic}, Impact: {c.impact_direction}\n   Rationale: {c.rationale}\n\n"
    
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
