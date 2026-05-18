"""
Art Analyzer Subagent — handles valuation, provenance, and artwork analysis for ArtAI.
Uses Claude with tool use for structured art data extraction.
"""

import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()

SYSTEM_PROMPT = """You are an expert art analyst for ArtAI, serving European galleries and auction houses.

You specialize in:
- Artwork valuation (based on artist, period, medium, provenance, condition, comparable sales)
- Provenance research and authentication flags
- Artist market trajectory analysis
- Collection advisory for high-net-worth clients

Always cite your reasoning. If you lack data to give a reliable valuation, say so clearly rather than estimating."""

VALUATION_TOOL = {
    "name": "structure_valuation",
    "description": "Structure an artwork valuation into a standard report format",
    "input_schema": {
        "type": "object",
        "properties": {
            "artist": {"type": "string"},
            "estimated_value_eur": {"type": "string", "description": "e.g. €45,000 – €65,000"},
            "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
            "key_factors": {"type": "array", "items": {"type": "string"}},
            "comparable_sales": {"type": "array", "items": {"type": "string"}},
            "flags": {"type": "array", "items": {"type": "string"}, "description": "Risks or authenticity concerns"},
        },
        "required": ["artist", "estimated_value_eur", "confidence", "key_factors"],
    },
}


class ArtAnalyzerAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def run(self, user_input: str) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=[VALUATION_TOOL],
            messages=[{"role": "user", "content": user_input}],
        )

        for block in response.content:
            if block.type == "tool_use" and block.name == "structure_valuation":
                data = block.input
                lines = [
                    f"**Artist:** {data.get('artist', 'Unknown')}",
                    f"**Estimated Value:** {data.get('estimated_value_eur')}",
                    f"**Confidence:** {data.get('confidence', 'medium').upper()}",
                    "",
                    "**Key Factors:**",
                    *[f"  • {f}" for f in data.get("key_factors", [])],
                ]
                if data.get("comparable_sales"):
                    lines += ["", "**Comparable Sales:**", *[f"  • {s}" for s in data["comparable_sales"]]]
                if data.get("flags"):
                    lines += ["", "**⚠️ Flags:**", *[f"  • {f}" for f in data["flags"]]]
                return "\n".join(lines)

        # Fallback: plain text response
        for block in response.content:
            if hasattr(block, "text"):
                return block.text

        return "Art analysis could not be completed."
