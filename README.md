# Eugenio Santiago — AI Agent Portfolio

**AI Agent Architect & Security Consultant · Berlin, DE**

> Multi-agent systems, MCP servers, n8n enterprise workflows, and AI security — built for the DACH market.

---

## Architecture: Orchestrator → Subagent → Reviewer

```
User Request
     │
     ▼
Smart Router (intent classification)
     │
     ├──► Art Analyzer Agent    (ArtAI: valuation, provenance, market)
     ├──► Market Intel Agent    (trends, pricing, gallery data)
     ├──► RAG Agent             (Supabase + pgvector knowledge base)
     └──► Security Audit Agent  (OWASP ASI compliance checks)
              │
              ▼
         Reviewer Agent (validates output quality + OWASP guardrails)
              │
              ▼
         Final Response
```

## Projects

| Project | Stack | Status |
|---------|-------|--------|
| [ArtAI Multi-Agent Platform](case-studies/01-artai-multi-agent.md) | Claude API + LangGraph + n8n + Docker | Active |
| [n8n Smart Router](case-studies/02-n8n-smart-router.md) | n8n + Claude + Supabase | Active |
| [AI Security Audit Template](case-studies/03-ai-security-audit.md) | OWASP ASI + DeepTeam + Python | Active |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add ANTHROPIC_API_KEY to .env
python agents/smart_router.py
```

## Certifications
- Anthropic CCA-F (in progress)
- CAISP — Certified AI Security Professional (in progress)
- IBM AI Engineering Professional (in progress)

---

*Sprint: 15–30 May 2026 · Go-live: 1 July 2026*
