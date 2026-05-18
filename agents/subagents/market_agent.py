"""
Market Intelligence Subagent — gallery trends, auction benchmarks, pricing for DACH market.
"""

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

SYSTEM_PROMPT = """You are a market intelligence analyst for the European art market, focused on the DACH region (Germany, Austria, Switzerland).

You track:
- Auction results from Christie's, Sotheby's, Ketterer Kunst, Villa Grisebach
- Gallery pricing trends in Berlin, Munich, Vienna, Zurich
- Emerging artist markets and collector behavior
- ArtTactic and Art Basel / UBS Art Market Report insights

Be specific, use numbers when possible, and always note the data vintage (year/quarter)."""


class MarketIntelAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def run(self, user_input: str) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_input}],
        )
        for block in response.content:
            if hasattr(block, "text"):
                return block.text
        return "Market analysis could not be completed."
