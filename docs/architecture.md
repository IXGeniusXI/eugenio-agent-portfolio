# Multi-Agent Architecture — ArtAI

## Pattern: Orchestrator → Subagent → Reviewer

### Why this pattern?
- **Separation of concerns**: routing, execution, and validation are independent
- **Auditability**: every step is logged and reviewable (OWASP ASI requirement)
- **Scalability**: add new subagents without changing orchestrator logic
- **Safety**: Reviewer acts as a guardrail against hallucinations and injection attacks

### Data Flow

```
User Input
    │
    ▼
[SmartRouter] — claude-haiku (fast, cheap classification)
    │  intent: art_analysis | market_intel | rag_search | security_audit
    ▼
[Subagent] — claude-sonnet (capable, tool use)
    │  structured output via tool_use
    ▼
[Reviewer] — claude-haiku (fast guardrail)
    │  OWASP ASI01 (injection) + ASI02 (data leakage) + relevance check
    ▼
Final Response
```

### Model Selection Strategy

| Node | Model | Reason |
|------|-------|--------|
| SmartRouter | claude-haiku-4-5 | Low latency, classification only, cheap |
| Subagents | claude-sonnet-4-6 | Full capability, tool use, structured output |
| Reviewer | claude-haiku-4-5 | Fast pass/fail check, no generation needed |

### Cost Estimate (per request)
- Haiku: ~$0.0003 (router + reviewer)
- Sonnet: ~$0.003 (subagent)
- **Total: ~$0.003/request** → viable for gallery SaaS at €199+/mês

### OWASP ASI Guardrails Implemented
- **ASI01 — Prompt Injection**: Reviewer scans output for instruction overrides
- **ASI02 — Sensitive Data Exposure**: Reviewer flags private client data in responses
- **ASI04 — Excessive Agency**: Subagents have no write/action tools by default
