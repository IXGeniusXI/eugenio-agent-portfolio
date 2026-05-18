"""
Smart Router — classifies user intent and routes to the correct subagent.
Pattern: LangGraph node that determines which subagent handles the request.
"""

import os
from typing import Literal
from dotenv import load_dotenv
import anthropic

load_dotenv()

IntentType = Literal["art_analysis", "market_intel", "rag_search", "security_audit", "unknown"]

INTENT_SYSTEM_PROMPT = """You are a routing classifier for ArtAI, an AI platform for art galleries.

Classify the user's request into exactly one of these intents:
- art_analysis: valuation, provenance, artist research, artwork description
- market_intel: gallery trends, auction results, pricing benchmarks, competitors
- rag_search: searching knowledge base, documents, past reports, stored data
- security_audit: OWASP compliance, vulnerability check, AI safety review
- unknown: cannot be classified

Respond with ONLY the intent label, nothing else."""


class SmartRouter:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def classify(self, user_input: str) -> IntentType:
        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=20,
            system=INTENT_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_input}],
        )
        intent = response.content[0].text.strip().lower()
        valid = {"art_analysis", "market_intel", "rag_search", "security_audit", "unknown"}
        return intent if intent in valid else "unknown"


if __name__ == "__main__":
    router = SmartRouter()
    tests = [
        "What is the estimated value of this Basquiat painting?",
        "Show me auction trends for contemporary German art in 2025",
        "Search our database for clients who bought sculptures last year",
        "Run OWASP injection test on the gallery recommendation engine",
    ]
    for query in tests:
        intent = router.classify(query)
        print(f"[{intent}] {query}")
